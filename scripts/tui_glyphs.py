"""Codepoints used by popular terminal UIs (coding agents, git/system TUIs, prompts).

Used by the build to fill gaps in misc-fixed 6x13 beyond Powerline/Nerd icons.
Grouped by the tool(s) known to emit them; extend freely.
"""
GROUPS = {
    "claude-code": "❯ ⏺ ⎿ ⏵ ⏸ ⏹ ✻ ✳ ✶ ✷ ✸ ✹ ✺ ✢ ✣ ✤ ✥ ✦ ✧ ✽ ✱ ✲ ∗ ✓ ✔ ✗ ✘ ✖ ✕ ⚠ ℹ ❖ ⧉ ⎇ ⌘ ⌃ ⌥ ⇧ ⇥ ⏎ ↵ ↳ ⤷ ☐ ☑ ☒ ⚡ ✨ ⚙ ✎ ✐ ❮ ❯ ➜ ➤ ▶ ▸ ▹ ▷ ◀ ◂ ◃ ◁ ◆ ◇ ◈ ● ○ ◉ ◯ ◌ ◍ ◎ ★ ☆ ⬥ ⬦ ⬧ ⬨ ⬩ ⬪ ⬫ ■ □ ▪ ▫ ▲ △ ▼ ▽ ▴ ▾ ▵ ▿ ‣ • ◦ … · ⋯ ⋮ ⋱ ∙ ‥ ※ ⁂ ⁎ ⁑ ❘ ❙ ❚",
    "claude-logo": "▐ ▛ █ ▜ ▌ ▝ ▘ ▗ ▖ ▀ ▄ ▙ ▟ ▚ ▞ ░ ▒ ▓",
    "codex-gemini-opencode": "› ‹ » « ▌ ▍ ▎ ▏ ┃ ╹ ╻ ╸ ╺ ▣ ▢ ⊷ ⊶ ⊸ ⊹ ◐ ◑ ◒ ◓ ◜ ◝ ◞ ◟ ◠ ◡ ⬝ ⬞ ∶ ∷",
    "git-tui": "⇡ ⇣ ⇕ ↑ ↓ ← → ↔ ↕ ↗ ↘ ↙ ↖ ⊙ ⊚ ⊛ ⊕ ⊖ ⊗ ⊘ ✚ ✜ ✛ ± ≠ ≈ ≤ ≥ ⇒ ⇐ ⇔ ⟶ ⟵ ⟷ ⤴ ⤵ ↩ ↪ ↺ ↻ ⟳ ⟲ ✂ ✎ ⌫ ⌦ ⏏ ⏪ ⏩ ⏫ ⏬ ⏭ ⏮ ⏯",
    "system-tui": "▁ ▂ ▃ ▄ ▅ ▆ ▇ █ ▉ ▊ ▋ ▌ ▍ ▎ ▏ ⣀ ⣿ ⠁ ⠿ ⏶ ⏷ ⏴ ⏵ ⏻ ⏼ ⏽ ⭘ ⏾ ⌛ ⌚ ☀ ☁ ☂ ☃ ♥ ♦ ♣ ♠ ♪ ♫ ☼ ☾ ✆ ✉ ✈ ☎ ⚑ ⚐ ⚒ ⚓ ⚔ ⚖ ⚗ ⚘ ⚙ ⚛ ⚜ ⚝ ⚞ ⚟",
    "box-drawing-extras": "╭ ╮ ╰ ╯ ╱ ╲ ╳ ┄ ┅ ┆ ┇ ┈ ┉ ┊ ┋ ╌ ╍ ╎ ╏ ═ ║ ╔ ╗ ╚ ╝ ╠ ╣ ╦ ╩ ╬",
    "misc": "✓ ✔ ✗ ✘ ✙ ✞ ✠ ✡ ❍ ❏ ❐ ❑ ❒ ❝ ❞ ❛ ❜ ❨ ❩ ❪ ❫ ❬ ❭ ❮ ❯ ❰ ❱ ❲ ❳ ❴ ❵ ⟨ ⟩ ⟦ ⟧ ⟪ ⟫ ⸢ ⸣ ⸤ ⸥",
}


def codepoints():
    seen = {}
    for group, s in GROUPS.items():
        for ch in s.split():
            for c in ch:
                seen.setdefault(ord(c), group)
    return seen
