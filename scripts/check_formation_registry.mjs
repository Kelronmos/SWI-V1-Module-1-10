import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const reg = JSON.parse(readFileSync(join(root, "evidence/formation_path_registry.json"), "utf8"));

let failed = 0;
function fail(msg) { console.error("FAIL:", msg); failed++; }
function ok(msg) { console.log("PASS:", msg); }

const ids = new Set(reg.paths.map(p => p.path_id));
for (const req of reg.required_path_ids || []) {
  if (!ids.has(req)) fail(`required path missing: ${req}`);
  else ok(`registered: ${req}`);
}

const open = reg.paths.filter(p => p.status === "OPEN" || p.status === "PARTIAL");
const wired = reg.paths.filter(p => p.status === "WIRED" || p.status === "GATED");
console.log(`SUMMARY registered=${reg.paths.length} open_or_partial=${open.length} wired_or_gated=${wired.length}`);

if (reg.universal_gate === "PROVEN" && open.length > 0) {
  fail("universal_gate cannot be PROVEN while OPEN/PARTIAL paths remain");
} else {
  ok(`universal_gate status honest: ${reg.universal_gate}`);
}

if (reg.fm005 !== "OPEN") fail("fm005 must remain OPEN until evidence closes it");
else ok("fm005 remains OPEN");

if (reg.swi_enforcement_gap !== "OPEN") fail("swi_enforcement_gap must stay OPEN until G3/T10 real enforcement");
else ok("swi_enforcement_gap remains OPEN");

if (failed) { console.error(`\nG1 registry check FAILED (${failed})`); process.exit(1); }
console.log("\nG1 registry check PASSED (inventory integrity only — Gate NOT PROVEN)");
