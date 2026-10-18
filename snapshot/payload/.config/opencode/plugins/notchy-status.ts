import { mkdir, writeFile } from "node:fs/promises"
import { homedir } from "node:os"
import { dirname, join } from "node:path"

const statusPath = join(homedir(), ".codex", "notchy", "status")
async function publish(status, project) {
  await mkdir(dirname(statusPath), { recursive: true })
  await writeFile(statusPath, status + "\t" + Math.floor(Date.now() / 1000) + "\t" + project + "\n", "utf8")
}

export const NotchyStatusPlugin = async ({ directory }) => ({
  "chat.message": async () => publish("working", directory || process.cwd()),
  event: async ({ event }) => {
    const raw = event?.properties?.status
    const status = typeof raw === "string" ? raw : raw?.type
    if (event?.type === "session.idle" || (event?.type === "session.status" && status === "idle")) {
      await publish("idle", directory || process.cwd())
    } else if (event?.type === "session.status" && status) {
      await publish("working", directory || process.cwd())
    }
  },
})