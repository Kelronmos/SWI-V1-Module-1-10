import { createExecutionAdapter } from "./execution_adapter.mjs";
import assert from "node:assert/strict";

let passed = 0, failed = 0;
function test(name, fn) {
  try { fn(); console.log("PASS:", name); passed++; }
  catch (e) { console.error("FAIL:", name, e.message); failed++; }
}

test("DENY → operation never invoked, successes=0", () => {
  const adapter = createExecutionAdapter();
  let called = 0;
  const r = adapter.execute("DENY", () => { called++; return "SHOULD_NOT"; });
  assert.equal(r.invoked, false);
  assert.equal(called, 0);
  assert.equal(r.metrics.execution_successes, 0);
  assert.equal(r.metrics.side_effects, 0);
});

test("BLOCK → zero successes", () => {
  const adapter = createExecutionAdapter();
  let called = 0;
  adapter.execute("BLOCK", () => { called++; });
  assert.equal(called, 0);
  assert.equal(adapter.getMetrics().execution_successes, 0);
});

test("ALLOW → operation invoked", () => {
  const adapter = createExecutionAdapter();
  let called = 0;
  const r = adapter.execute("ALLOW", () => { called++; return "OK"; });
  assert.equal(r.invoked, true);
  assert.equal(called, 1);
  assert.equal(r.result, "OK");
});

test("T10-shaped assertion on synthetic adapter", () => {
  const adapter = createExecutionAdapter();
  let called = 0;
  adapter.execute("DENY", () => { called++; });
  const m = adapter.getMetrics();
  assert.equal(called, 0);
  assert.equal(m.execution_successes, 0);
  assert.equal(m.side_effects, 0);
});

console.log("\n---");
console.log(`Passed: ${passed} Failed: ${failed}`);
if (failed) process.exit(1);
console.log("NOTE: synthetic only — SWI-ENFORCEMENT-GAP / T10 still OPEN");
