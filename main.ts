// gta6-meme-x-01 entry (Node 22, standard library only): it copies POST.json
// from the repository root to /output/POST.json, where the gate reads it.
// That is all the program has to do. The entry is the post itself: the meme
// (meme.png, built by make_meme.py from an AI-generated Vice City sunset and
// make.fun's press-kit ghost) is posted on X from a public account with
// make.fun (a link) and/or a tag of @makefunai and the entrant's play code in
// its text, POST.json names the post's address, and the house reads the post
// from X (its first picture and its text) and hands that to the judge.
// Nothing this program writes about the post is judged.
//
// POST.json still holds the placeholder address until the meme is posted.
// Replace it with the post's address before submitting, or the gate refuses
// the entry as it stands (valid 0).
//
// Outside the grader's container, MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR
// stand in for /bot and /output:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
//
// No network, no wall clock, no files outside the repository: the two runs
// of an entry write the same bytes.

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

const SOURCE = join(BOT_DIR, 'POST.json');
const TARGET = join(OUTPUT_DIR, 'POST.json');

let bytes: Buffer;
try {
  bytes = readFileSync(SOURCE);
} catch (err) {
  console.error(`POST.json could not be read from ${BOT_DIR}: ${(err as Error).message}`);
  process.exit(1);
}

// The gate only accepts a JSON object naming an X post's address, so refuse
// to copy anything else instead of handing the grader a broken file.
let post: unknown;
try {
  post = JSON.parse(bytes.toString('utf8'));
} catch (err) {
  console.error(`POST.json is not valid JSON: ${(err as Error).message}`);
  process.exit(1);
}
if (typeof post !== 'object' || post === null || Array.isArray(post)
    || typeof (post as { url?: unknown }).url !== 'string') {
  console.error('POST.json must be a JSON object with a string "url" field');
  process.exit(1);
}

mkdirSync(OUTPUT_DIR, { recursive: true });
writeFileSync(TARGET, bytes);
