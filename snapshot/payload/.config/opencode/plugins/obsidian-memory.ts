import type { Plugin } from "@opencode-ai/plugin"
import { watch, type FSWatcher } from "node:fs"
import { mkdir, readdir } from "node:fs/promises"
import { basename, join } from "node:path"

const HOME = process.env.HOME ?? "/Users/batimoff"
const VAULT = process.env.OPENCODE_OBSIDIAN_VAULT ?? join(HOME, "Obsidian")
const ROOT = join(VAULT, "OpenCode")
const PROJECTS_ROOT = join(ROOT, "Projects")
const SKILLS_ROOT = join(ROOT, "Skills")
const SKILL_SOURCES = [join(HOME, ".agents", "skills"), join(HOME, ".claude", "skills"), join(HOME, ".config", "opencode", "skills")]
const MAX_PART_LENGTH = 8_000
const MAX_SESSION_LENGTH = 120_000

const writes = new Map<string, Promise<void>>()

function runGit(directory: string, args: string[]): string {
  try {
    const result = Bun.spawnSync(["git", "-C", directory, ...args])
    if (result.exitCode === 0) return result.stdout.toString().trim()
  } catch {
    // The working directory may not be a Git repository.
  }
  return ""
}

function projectIdentity(directory: string) {
  const root = runGit(directory, ["rev-parse", "--show-toplevel"]) || directory
  const remote = runGit(directory, ["remote", "get-url", "origin"])
  const remoteName = remote.replace(/\.git$/, "").split(/[/:]/).pop()
  const name = remoteName || basename(root) || "unknown-project"
  return {
    name,
    slug: slug(name, "unknown-project"),
    root,
    branch: runGit(directory, ["branch", "--show-current"]),
  }
}

function slug(value: string, fallback: string): string {
  const result = value
    .normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-zA-Z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .toLowerCase()
  return result || fallback
}

function stripPrivate(text: string): string {
  return text.replace(/<private>[\s\S]*?<\/private>/gi, "[REDACTED]")
}

function redact(text: string, limit = MAX_PART_LENGTH): string {
  let safe = stripPrivate(String(text ?? ""))
  safe = safe.replace(
    /((?:api[_-]?key|access[_-]?token|refresh[_-]?token|password|passwd|secret|authorization|bearer)\s*[:=]\s*)([^\s,;]+)/gi,
    "$1[REDACTED]",
  )
  safe = safe.replace(/\b(?:sk-[a-zA-Z0-9_-]{16,}|gh[pousr]_[a-zA-Z0-9_]{16,}|AIza[a-zA-Z0-9_-]{20,})\b/g, "[REDACTED]")
  return safe.length > limit ? `${safe.slice(0, limit)}\n\n[…truncated…]` : safe
}

function json(value: unknown, limit = MAX_PART_LENGTH): string {
  try {
    return redact(JSON.stringify(value, null, 2), limit)
  } catch {
    return redact(String(value), limit)
  }
}

function dateStamp(value: number | undefined): string {
  return new Date(value ?? Date.now()).toISOString()
}

function yaml(value: unknown): string {
  return JSON.stringify(String(value ?? "").replace(/\s+/g, " ").trim())
}

function renderPart(part: any): string {
  if (!part) return ""

  if (part.type === "text") return redact(part.text ?? "")

  if (part.type === "tool") {
    const state = part.state ?? {}
    const lines = [`#### Tool: \`${part.tool ?? "unknown"}\` (${state.status ?? "unknown"})`]
    if (state.input) lines.push("\n**Input**\n\n```json\n" + json(state.input) + "\n```")
    if (state.output) lines.push("\n**Output**\n\n```text\n" + redact(state.output) + "\n```")
    if (state.error) lines.push("\n**Error**\n\n```text\n" + redact(state.error) + "\n```")
    return lines.join("\n")
  }

  if (part.type === "retry") {
    return `#### Retry attempt ${part.attempt ?? "?"}\n\n\`\`\`json\n${json(part.error)}\n\`\`\``
  }

  if (part.type === "patch") {
    return `**Patch:** ${(part.files ?? []).map((file: string) => `\`${redact(file, 300)}\``).join(", ")}`
  }

  if (part.type === "subtask") {
    return `#### Subtask (${redact(part.agent ?? "unknown", 200)})\n\n${redact(part.description ?? part.prompt ?? "")}`
  }

  if (part.type === "step-finish") {
    return `**Step finished:** ${redact(part.reason ?? "", 300)} — cost ${part.cost ?? 0}`
  }

  return ""
}

function renderMessage(item: any): string {
  const info = item?.info ?? {}
  const parts = Array.isArray(item?.parts) ? item.parts : []
  const heading = info.role === "user" ? "### User" : "### Assistant"
  const sections: string[] = [heading]

  if (info.error) {
    sections.push("\n**Message error**\n\n```json\n" + json(info.error) + "\n```")
  }

  const rendered = parts.map(renderPart).filter(Boolean)
  if (rendered.length > 0) sections.push(`\n${rendered.join("\n\n")}`)

  if (info.role === "user" && info.summary) {
    const summary = [info.summary.title, info.summary.body].filter(Boolean).join("\n")
    if (summary) sections.push(`\n**Summary**\n\n${redact(summary)}`)
  }

  return sections.join("\n")
}

function queueWrite(key: string, operation: () => Promise<void>): Promise<void> {
  const previous = writes.get(key) ?? Promise.resolve()
  const next = previous.catch(() => undefined).then(operation)
  writes.set(key, next)
  return next.finally(() => {
    if (writes.get(key) === next) writes.delete(key)
  })
}

async function ensureProjectNote(project: ReturnType<typeof projectIdentity>): Promise<void> {
  const projectDir = join(PROJECTS_ROOT, project.slug)
  await mkdir(projectDir, { recursive: true })
  const file = Bun.file(join(projectDir, "_Project.md"))
  if (await file.exists()) return

  await Bun.write(
    file,
    `---\nproject: ${yaml(project.name)}\ndirectory: ${yaml(project.root)}\ncreated: ${yaml(dateStamp())}\n---\n\n# ${project.name}\n\n- **Directory:** \`${project.root}\`\n- **Branch at first capture:** \`${project.branch || "unknown"}\`\n- **Session notes:** [[Sessions]]\n\nThis folder is maintained automatically by OpenCode. Each session note is rewritten at idle so it contains the latest prompts, assistant responses, tool calls, errors, and change statistics.\n`,
  )
}

async function syncSkills(): Promise<void> {
  const skills = new Map<string, { name: string; source: string; content: string }>()

  for (const root of SKILL_SOURCES) {
    try {
      const entries = await readdir(root, { withFileTypes: true })
      for (const entry of entries) {
        if (!entry.isDirectory()) continue
        const source = join(root, entry.name, "SKILL.md")
        const file = Bun.file(source)
        if (!(await file.exists()) || skills.has(entry.name)) continue
        skills.set(entry.name, { name: entry.name, source, content: redact(await file.text(), 100_000) })
      }
    } catch {
      // A skill directory may not exist on every machine.
    }
  }

  await mkdir(SKILLS_ROOT, { recursive: true })
  const index = ["# OpenCode Skills", "", "Synced automatically when OpenCode starts.", ""]
  for (const [name, skill] of [...skills.entries()].sort(([a], [b]) => a.localeCompare(b))) {
    const directory = join(SKILLS_ROOT, slug(name, "skill"))
    await mkdir(directory, { recursive: true })
    await Bun.write(
      join(directory, "SKILL.md"),
      `<!-- Source: ${skill.source} -->\n<!-- Synced: ${dateStamp()} -->\n\n${skill.content}\n`,
    )
    index.push(`- [[${slug(name, "skill")}/SKILL|${name}]] — \`${skill.source}\``)
  }
  await Bun.write(join(SKILLS_ROOT, "_Index.md"), index.join("\n") + "\n")
}

function watchSkillSources(): { close: () => void } {
  const watchers: FSWatcher[] = []
  let timer: ReturnType<typeof setTimeout> | undefined

  for (const root of SKILL_SOURCES) {
    try {
      watchers.push(
        watch(root, () => {
          if (timer) clearTimeout(timer)
          timer = setTimeout(() => {
            void queueWrite("skills", syncSkills)
          }, 500)
        }),
      )
    } catch {
      // A skill directory may not exist on every machine.
    }
  }

  return {
    close: () => {
      if (timer) clearTimeout(timer)
      for (const watcher of watchers) watcher.close()
    },
  }
}

async function persistSession(client: any, sessionID: string, fallbackDirectory: string): Promise<void> {
  if (!sessionID) return

  const [sessionResult, messagesResult, diffResult] = await Promise.allSettled([
    client.session.get({ path: { id: sessionID } }),
    client.session.messages({ path: { id: sessionID }, query: { limit: 1000 } }),
    client.session.diff({ path: { id: sessionID } }),
  ])

  const session = sessionResult.status === "fulfilled" ? sessionResult.value?.data : undefined
  const messages = messagesResult.status === "fulfilled" ? (messagesResult.value?.data ?? []) : []
  const diffs = diffResult.status === "fulfilled" ? (diffResult.value?.data ?? []) : []
  const directory = session?.directory || fallbackDirectory
  const project = projectIdentity(directory)
  await ensureProjectNote(project)

  const projectDir = join(PROJECTS_ROOT, project.slug)
  const sessionFile = join(projectDir, "Sessions", `${slug(sessionID, "session")}.md`)
  await mkdir(join(projectDir, "Sessions"), { recursive: true })

  const errors = [
    ...(session?.error ? [json(session.error)] : []),
    ...messages.flatMap((item: any) => {
      const messageError = item?.info?.error ? [json(item.info.error)] : []
      const partErrors = (item?.parts ?? [])
        .filter((part: any) => part?.type === "tool" && part?.state?.status === "error")
        .map((part: any) => `${part.tool ?? "tool"}: ${redact(part.state.error ?? "unknown error")}`)
      return [...messageError, ...partErrors]
    }),
  ]

  const changeLines = diffs.map((diff: any) =>
    `- \`${redact(diff.file ?? "unknown", 500)}\` — **+${diff.additions ?? 0} / -${diff.deletions ?? 0}**`,
  )
  const conversation = messages.map(renderMessage).filter(Boolean).join("\n\n")
  const content = `---
project: ${yaml(project.name)}
session_id: ${yaml(sessionID)}
directory: ${yaml(project.root)}
branch: ${yaml(project.branch || "unknown")}
title: ${yaml(redact(session?.title || sessionID, 300))}
created: ${yaml(dateStamp(session?.time?.created))}
updated: ${yaml(dateStamp(session?.time?.updated))}
---

# ${redact(session?.title || "OpenCode session", 300)}

## Session

- **Project:** [[../_Project|${project.name}]]
- **Session ID:** \`${sessionID}\`
- **Directory:** \`${project.root}\`
- **Last capture:** ${dateStamp()}

## Changes

${changeLines.length > 0 ? changeLines.join("\n") : "No file diff was reported by OpenCode for this capture."}

## Errors

${errors.length > 0 ? errors.map((error: string) => `- ${error.replace(/\n/g, " ")}`).join("\n") : "No session or tool errors were reported."}

## Conversation and tool activity

${redact(conversation, MAX_SESSION_LENGTH) || "No messages were available when this note was captured."}
`

  await Bun.write(sessionFile, content)
}

export const ObsidianMemory: Plugin = async ({ client, directory }) => {
  await mkdir(PROJECTS_ROOT, { recursive: true })
  await mkdir(SKILLS_ROOT, { recursive: true })
  await syncSkills()
  const skillWatch = watchSkillSources()

  const capture = (sessionID: string) =>
    queueWrite(`session:${sessionID}`, async () => {
      try {
        await persistSession(client, sessionID, directory)
      } catch (error) {
        console.error("[obsidian-memory] capture failed:", error)
      }
    })

  return {
    event: async ({ event }) => {
      if ((event as any).type === "global.disposed") {
        skillWatch.close()
        return
      }

      if (event.type === "session.created") {
        const info = event.properties.info
        await ensureProjectNote(projectIdentity(info.directory || directory))
      }

      if (event.type === "session.idle") {
        await capture(event.properties.sessionID)
      }

      if (event.type === "session.status" && event.properties.status.type === "idle") {
        await capture(event.properties.sessionID)
      }

      if (event.type === "session.compacted") {
        await capture(event.properties.sessionID)
      }

      if (event.type === "session.error" && event.properties.sessionID) {
        await capture(event.properties.sessionID)
      }
    },
  }
}
