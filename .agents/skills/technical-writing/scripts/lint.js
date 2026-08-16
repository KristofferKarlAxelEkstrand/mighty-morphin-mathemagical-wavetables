#!/usr/bin/env node
// Heuristic controlled-language linter for the technical-writing skill.
//
// Advisory only: reports candidate violations per 100 words for the mechanical
// subset of references/controlled-language-rules.md (sentence length,
// semicolons, contractions, a passive-voice heuristic, nominalizations,
// paragraph length, marketing words). It cannot check terminology consistency
// or factual accuracy -- do those by hand against self-check.md.
//
// Usage:
//   node lint.js <file>          # read a file
//   node lint.js -                # read stdin
//   node lint.js --strict <file>  # 20-word sentence ceiling instead of 25
//
// Node only, no npm dependencies -- matches the package's zero-runtime-deps rule.

import fs from "node:fs";
import process from "node:process";

const MARKETING_WORDS = [
  "seamless",
  "seamlessly",
  "powerful",
  "robust",
  "cutting-edge",
  "cutting edge",
  "effortless",
  "effortlessly",
  "revolutionary",
  "utilize",
  "utilizes",
  "utilized",
  "leverage",
  "leverages",
  "leveraged",
  "facilitate",
  "facilitates",
  "world-class",
  "best-in-class",
  "innovative",
  "game-changing",
  "unleash",
  "empower",
  "empowers",
];

const IRREGULAR_PAST_PARTICIPLES = [
  "done",
  "seen",
  "taken",
  "given",
  "written",
  "made",
  "sent",
  "put",
  "read",
  "found",
  "held",
  "known",
  "shown",
  "chosen",
  "spoken",
  "broken",
  "driven",
  "brought",
  "thought",
  "bought",
  "caught",
  "taught",
  "felt",
  "kept",
  "meant",
  "left",
  "built",
  "sold",
  "told",
  "spent",
  "understood",
];

const NOMINALIZATION_VERBS = ["perform", "make", "conduct", "carry out"];
const NOMINALIZATION_SUFFIXES = ["tion", "sion", "ment", "ance", "ence"];

const FENCE_RE = /```[\s\S]*?```/g;
const INLINE_CODE_RE = /`[^`]*`/g;
const FRONTMATTER_RE = /^---\n[\s\S]*?\n---\n/;
const TABLE_ROW_RE = /^\s*\|.*\|\s*$/;
const SENTENCE_SPLIT_RE = /(?<=[.!?])\s+/;
const CONTRACTION_RE = /\b\w+'(t|re|ll|ve|d|m)\b/gi;
const PASSIVE_RE = /\b(is|are|was|were|be|been|being)\s+\w+ed\b/gi;

function stripFrontmatter(text) {
  return text.replace(FRONTMATTER_RE, "");
}

function stripCode(text) {
  return text.replace(FENCE_RE, " ").replace(INLINE_CODE_RE, " ");
}

function stripTableRows(text) {
  return text
    .split("\n")
    .filter((line) => !TABLE_ROW_RE.test(line))
    .join("\n");
}

function splitParagraphs(text) {
  return text
    .split(/\n\s*\n/)
    .map((p) => p.trim())
    .filter(Boolean);
}

function splitSentences(paragraph) {
  const flat = paragraph.split(/\s+/).filter(Boolean).join(" ");
  return flat
    .split(SENTENCE_SPLIT_RE)
    .map((s) => s.trim())
    .filter(Boolean);
}

function countMatches(re, text) {
  const matches = text.match(re);
  return matches ? matches.length : 0;
}

function countPassive(sentence) {
  let hits = countMatches(PASSIVE_RE, sentence);
  for (const word of IRREGULAR_PAST_PARTICIPLES) {
    const pattern = new RegExp(`\\b(is|are|was|were|be|been|being)\\s+${word}\\b`, "gi");
    hits += countMatches(pattern, sentence);
  }
  return hits;
}

function countNominalizations(sentence) {
  let hits = 0;
  const lowered = sentence.toLowerCase();
  for (const verb of NOMINALIZATION_VERBS) {
    for (const suffix of NOMINALIZATION_SUFFIXES) {
      const pattern = new RegExp(`${verb}\\s+(a|an|the)?\\s*\\w*${suffix}\\b`, "g");
      hits += countMatches(pattern, lowered);
    }
  }
  return hits;
}

function countMarketing(text) {
  const lowered = text.toLowerCase();
  return MARKETING_WORDS.reduce((sum, word) => sum + lowered.split(word).length - 1, 0);
}

function lint(text, ceiling) {
  const clean = stripTableRows(stripCode(stripFrontmatter(text)));
  const paragraphs = splitParagraphs(clean);

  let totalWords = 0;
  let longSentences = 0;
  let passiveHits = 0;
  let nominalizationHits = 0;
  let longParagraphs = 0;

  for (const paragraph of paragraphs) {
    const sentences = splitSentences(paragraph);
    if (sentences.length > 6) longParagraphs += 1;
    for (const sentence of sentences) {
      const words = sentence.split(/\s+/).filter(Boolean);
      totalWords += words.length;
      if (words.length > ceiling) longSentences += 1;
      passiveHits += countPassive(sentence);
      nominalizationHits += countNominalizations(sentence);
    }
  }

  const semicolons = (clean.match(/;/g) || []).length;
  const contractions = countMatches(CONTRACTION_RE, clean);
  const marketingHits = countMarketing(clean);

  const totalViolations =
    longSentences +
    semicolons +
    contractions +
    passiveHits +
    nominalizationHits +
    longParagraphs +
    marketingHits;

  const density = totalWords ? (totalViolations / totalWords) * 100 : 0;

  return {
    totalWords,
    longSentences,
    semicolons,
    contractions,
    passiveVoice: passiveHits,
    nominalizations: nominalizationHits,
    longParagraphs,
    marketingWords: marketingHits,
    totalViolations,
    violationsPer100Words: Math.round(density * 100) / 100,
  };
}

function printReport(report, ceiling) {
  console.log(`Sentence length ceiling: ${ceiling} words`);
  console.log(`Total words: ${report.totalWords}`);
  console.log("Violations:");
  console.log(`  long sentences   : ${report.longSentences}`);
  console.log(`  semicolons       : ${report.semicolons}`);
  console.log(`  contractions     : ${report.contractions}`);
  console.log(`  passive voice    : ${report.passiveVoice}`);
  console.log(`  nominalizations  : ${report.nominalizations}`);
  console.log(`  long paragraphs  : ${report.longParagraphs}`);
  console.log(`  marketing words  : ${report.marketingWords}`);
  console.log(`Total violations: ${report.totalViolations}`);
  console.log(`Violations per 100 words: ${report.violationsPer100Words}`);
}

function readStdin() {
  return fs.readFileSync(0, "utf8");
}

function main(argv) {
  const strict = argv.includes("--strict");
  const args = argv.filter((a) => a !== "--strict");
  const ceiling = strict ? 20 : 25;

  if (args.length !== 1) {
    console.error("usage: lint.js [--strict] <file|->");
    return 2;
  }

  const source = args[0];
  let text;
  try {
    text = source === "-" ? readStdin() : fs.readFileSync(source, "utf8");
  } catch (error) {
    console.error(`lint.js: cannot read ${source}: ${error.message}`);
    return 2;
  }

  const report = lint(text, ceiling);
  printReport(report, ceiling);
  return 0;
}

process.exit(main(process.argv.slice(2)));
