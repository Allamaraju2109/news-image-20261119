// Entry for make.fun's daily news-image bounty: "Sum up 19 November's world news in one image"
// (competition news-image-20261119).
//
// The picture is entry.png, the front page drawn by tools/make_entry.py that sums up the world
// news of Thursday, 19 November 2026. This program only copies those bytes to /output/entry.png,
// so the grader's two runs write byte for byte the same image.
//
// Run it locally with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const entryImage = new URL('./entry.png', import.meta.url);

copyFileSync(entryImage, join(outputDir, 'entry.png'));
