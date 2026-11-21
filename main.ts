// Entry program for news-image-20261121, second edition (Node 22, stdlib only).
//
// It copies the front-page image for Saturday 21 November 2026 — drawn from
// scratch by draw.py in this repository (the Shenzhen summit leads; the world
// court ruling and the market sell-off sit in a right-hand sidebar; the Kyiv
// barrage and the cancer-pill trial fill the bottom band) — to
// /output/entry.png. The copy is exact, so both runs write identical bytes:
// no network, no randomness, just the committed entry.png, byte for byte.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
const png = readFileSync(join(here, 'entry.png'));
writeFileSync(join(outDir, 'entry.png'), png);
