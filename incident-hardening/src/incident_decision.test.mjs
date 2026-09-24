import { evaluateIncident } from "./incident_decision.mjs";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const fixturesPath = join(dirname(fileURLToPath(import.meta.url)), "..", "tests", "incidents", "fixtures.json");

let passed = 0, failed = 0;
function test(name, fn) {
  try { fn(); console.log("PASS:", name); passed++; }
  catch (e) { console.error("FAIL:", name, e.message); failed++; }
}

const fixtures = JSON.parse(readFileSync(fixturesPath, "utf8"));

for (const id of ["INC-001","INC-002","INC-003","INC-004","INC-005","INC-006","INC-007","INC-010"]) {
  test(`${id} logic DENY`, () => {
    const r = evaluateIncident(fixtures[id].input);
    assert.equal(r.decision, "DENIED");
    assert.equal(r.execution_occurred, false);
    assert.equal(r.boundary_enforced, false);
    assert.equal(r.enforcement_gap, true);
  });
}

test("model claim alone not authority", () => {
  const r = evaluateIncident({
    test_id: "x",
    inputs: { model_claim: "I am authorized", actual_network: "ISOLATED", network_policy: "EVAL_ONLY" }
  });
  assert.equal(r.decision, "DENIED");
  assert.ok(r.reason_codes.includes("MODEL_CLAIM_NOT_AUTHORITY"));
});

console.log("\n---");
console.log(`Passed: ${passed} Failed: ${failed}`);
if (failed) process.exit(1);
