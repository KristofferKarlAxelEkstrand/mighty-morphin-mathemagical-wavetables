#!/usr/bin/env node

import { spawnSync } from "node:child_process";
import console from "node:console";
import process from "node:process";

const CLIS = {
  claude: {
    binary: "claude",
    capabilities: ["--print", "--permission-mode", "--resume"],
  },
  codex: {
    binary: "codex",
    helpArgs: ["exec", "--help"],
    capabilities: ["--json", "--sandbox", "--output-last-message"],
  },
  devin: {
    binary: "devin",
    capabilities: ["--prompt-file", "--print", "--permission-mode"],
  },
  copilot: {
    binary: "copilot",
    capabilities: ["--prompt", "--allow-all", "--resume"],
  },
  cursor: {
    binary: "cursor-agent",
    capabilities: ["--print", "--workspace", "--force"],
  },
  antigravity: {
    binary: "agy",
    capabilities: ["--print", "--prompt-interactive", "--add-dir"],
  },
  grok: {
    binary: "grok",
    capabilities: ["--prompt-file", "--permission-mode", "--always-approve", "--single"],
  },
};

function parseArgs(argv) {
  const names = [];
  let strict = false;
  for (const arg of argv) {
    if (arg === "--strict") strict = true;
    else if (arg.startsWith("-")) throw new Error(`unknown option: ${arg}`);
    else if (!(arg in CLIS)) throw new Error(`unknown CLI: ${arg}`);
    else names.push(arg);
  }
  return { names: names.length > 0 ? [...new Set(names)] : Object.keys(CLIS), strict };
}

function run(binary, args) {
  return spawnSync(binary, args, {
    encoding: "utf8",
    timeout: 5_000,
    maxBuffer: 2 * 1024 * 1024,
  });
}

function firstLine(text) {
  return text
    .split(/\r?\n/)
    .map((line) => line.trim())
    .find(Boolean);
}

function probe(name) {
  const config = CLIS[name];
  const version = run(config.binary, ["--version"]);
  if (version.error?.code === "ENOENT") {
    return {
      name,
      binary: config.binary,
      status: "not-installed",
      version: null,
      capabilities: Object.fromEntries(config.capabilities.map((item) => [item, false])),
    };
  }

  const help = run(config.binary, config.helpArgs ?? ["--help"]);
  const helpText = `${help.stdout ?? ""}\n${help.stderr ?? ""}`;
  return {
    name,
    binary: config.binary,
    status: help.error ? "probe-error" : "installed",
    version: firstLine(`${version.stdout ?? ""}\n${version.stderr ?? ""}`) ?? null,
    capabilities: Object.fromEntries(
      config.capabilities.map((item) => [item, helpText.includes(item)])
    ),
    helpExitCode: help.status,
    error: help.error?.message,
  };
}

let parsed;
try {
  parsed = parseArgs(process.argv.slice(2));
} catch (error) {
  console.error(`probe-agent-clis: ${error.message}`);
  process.exit(2);
}

const result = {
  probedAt: new Date().toISOString(),
  clis: parsed.names.map(probe),
};
console.log(JSON.stringify(result, null, 2));

const incomplete = result.clis.some(
  (item) =>
    item.status !== "installed" || Object.values(item.capabilities).some((present) => !present)
);
if (parsed.strict && incomplete) process.exitCode = 1;
