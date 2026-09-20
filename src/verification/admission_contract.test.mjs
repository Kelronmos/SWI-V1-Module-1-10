import { assertAdmission, runWithAdmission, AdmissionRequiredError } from "./admission_contract.mjs";
import assert from "node:assert/strict";

let passed = 0, failed = 0;
function test(name, fn) {
  try { fn(); console.log("PASS:", name); passed++; }
  catch (e) { console.error("FAIL:", name, e.message); failed++; }
}

test("missing admission rejects", () => {
  assert.throws(() => assertAdmission(null), AdmissionRequiredError);
});
test("invalid admission rejects", () => {
  assert.throws(() => assertAdmission({ valid: false }), AdmissionRequiredError);
});
test("valid admission allows", () => {
  assert.equal(assertAdmission({ valid: true, id: "A1" }).admitted, true);
});
test("operation not called without admission", () => {
  let called = 0;
  assert.throws(() => runWithAdmission(null, () => { called++; }), AdmissionRequiredError);
  assert.equal(called, 0);
});
test("operation called with valid admission", () => {
  let called = 0;
  const out = runWithAdmission({ valid: true }, () => { called++; return "OK"; });
  assert.equal(called, 1);
  assert.equal(out, "OK");
});
test("TEST_ONLY bypass is explicit", () => {
  assert.equal(assertAdmission(null, { testOnlyBypass: true }).mode, "TEST_ONLY");
});

console.log("\n---");
console.log(`Passed: ${passed} Failed: ${failed}`);
if (failed) process.exit(1);
