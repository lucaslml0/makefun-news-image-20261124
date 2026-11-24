// Entry point for the news-image-20261124 bounty.
//
// Copies the front-page image this repository holds (entry.png, drawn
// by draw_entry.py with Pillow) to the output directory the harness
// expects. No network, no randomness: every run writes identical bytes.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));
