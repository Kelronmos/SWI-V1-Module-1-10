#!/usr/bin/env node
/**
 * SWI V4.7 discipline check (lightweight).
 * Does not run TLC. Verifies presence of required formal-track files
 * and refuses to invent sealed status.
 */
const fs = require("fs");
const path = require("path");

const required = [
  "docs/SWI_V4_7_DISCIPLINE.md",
  "verification/tla/v47/SWIWorkflowV47.tla",
  "verification/tla/v47/SWIWorkflowV47.cfg",
  "verification/properties/SWI-WORKFLOW-001.md",
  "verification/properties/SWI-WORKFLOW-002.md",
  "verification/properties/SWI-WORKFLOW-003.md",
  "evidence/swi-v47/claims/SWI-WORKFLOW-001.json",
  "evidence/swi-v47/claims/SWI-FM005-001.json"
];

let ok = true;
for (const rel of required) {
  const p = path.join(process.cwd(), rel);
  if (!fs.existsSync(p)) {
    console.error("[MISSING]", rel);
    ok = false;
  } else {
    console.log("[OK]", rel);
  }
}

if (!ok) {
  console.error("\nSWI V4.7 discipline check FAILED");
  process.exit(1);
}

console.log("\nSWI V4.7 discipline check PASSED (presence only)");
console.log("Non-claim: presence ≠ PROVEN_ON_MODEL ≠ SEALED");
