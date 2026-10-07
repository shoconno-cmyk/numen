# Fonts

Bundled locally so no page requests Google Fonts. Loaded by `@font-face`
in `numen_theme.css` (repo root), the one stylesheet the Story Report,
the walkthrough and the demo cards all use.

| File | Family | Weight | Role | License |
|---|---|---|---|---|
| `fraunces-latin-400-normal.woff2` | Fraunces | 400 | headings, the Numen wordmark | `Fraunces-OFL.txt` |
| `fraunces-latin-500-normal.woff2` | Fraunces | 500 | headings, the Numen wordmark | `Fraunces-OFL.txt` |
| `inter-latin-400-normal.woff2` | Inter | 400 | body text, labels, buttons, captions | `Inter-OFL.txt` |
| `inter-latin-500-normal.woff2` | Inter | 500 | body text, labels, buttons, captions | `Inter-OFL.txt` |
| `inter-latin-600-normal.woff2` | Inter | 600 | bold body text and lead-ins (added 2026-10-06) | `Inter-OFL.txt` |
| `courier-prime-latin-400-normal.woff2` | Courier Prime | 400 | script text only | `CourierPrime-OFL.txt` |

All three families are licensed under the SIL Open Font License 1.1; each
license file is the full OFL text with the family's copyright line.

Script text has no bold weight on purpose: Courier Prime 400 only, as in a
real screenplay.

Source: the Fontsource builds of the Google Fonts releases, version 5.3.0
(`@fontsource/fraunces`, `@fontsource/inter`, `@fontsource/courier-prime`,
`files/<name>.woff2` and `LICENSE`, downloaded from cdn.jsdelivr.net on
2026-10-06). Latin subset only (U+0000-00FF, general punctuation
U+2000-206F and a few others); any character outside it falls back to the
next font in the stack.
