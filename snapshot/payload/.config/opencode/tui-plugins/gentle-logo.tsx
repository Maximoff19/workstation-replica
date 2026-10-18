// @ts-nocheck
/** @jsxImportSource @opentui/solid */
import type { TuiPlugin, TuiThemeCurrent } from "@opencode-ai/plugin/tui"
import { useTerminalDimensions } from "@opentui/solid"
import { createMemo } from "solid-js"

const id = "gentle-logo"

const baconArt = [
  "██████╗  █████╗  ██████╗ ██████╗ ██████╗  ██████╗ ███╗   ██╗",
  "██╔══██╗██╔══██╗██╔════╝██╔════╝██╔═══██╗██╔═══██╗████╗  ██║",
  "██████╔╝███████║██║     ██║     ██║   ██║██║   ██║██╔██╗ ██║",
  "██╔══██╗██╔══██║██║     ██║     ██║   ██║██║   ██║██║╚██╗██║",
  "██║  ██║██║  ██║╚██████╗╚██████╗╚██████╔╝╚██████╔╝██║ ╚████║",
  "╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝",
]

const compactArt = ["✦ Gentle AI ✦"]

const logoColor = "#FFFFFF"

const Logo = (props: { theme: TuiThemeCurrent }) => {
  const dim = useTerminalDimensions()
  const lines = createMemo(() => {
    const term = dim()
    return term.height >= baconArt.length + 6 && term.width >= 60 ? baconArt : compactArt
  })

  return (
    <box flexDirection="column" alignItems="center">
      {lines().map((line) => (
        <text fg={logoColor}>{line}</text>
      ))}
    </box>
  )
}

const tui: TuiPlugin = async (api) => {
  api.slots.register({
    id,
    order: 100,
    slots: {
      home_logo(ctx) {
        return <Logo theme={ctx.theme.current} />
      },
    },
  })
}

const plugin = { id: "gentle-logo", tui }
export default plugin
