// Entry program for news-image-20261121 (Node 22, standard library only).
//
// It writes the front-page image for Saturday 21 November 2026 — drawn by
// draw.py in this repository — to /output/entry.png. The copy is exact, so
// both runs of the program produce identical bytes. No network, no randomness:
// the output is the committed entry.png, byte for byte.
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
