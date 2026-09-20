/**
 * Adversarial / unit tests for SWI V4.7 Status Engine
 * These tests prove both rejection and legal advancement paths.
 */

import { evaluate } from "./status_engine.mjs";
import assert from "node:assert/strict";

let passed = 0;
let failed = 0;

function test(name, fn) {
  try {
    fn();
    console.log("PASS:", name);
    passed++;
  } catch (e) {
    console.error("FAIL:", name);
    console.error(" ", e.message);
    failed++;
  }
}

// --- Hard rejection cases ---

test("PROVEN_ON_MODEL → SEALED is rejected", () => {
  const r = evaluate("PROVEN_ON_MODEL", "SEALED", {});
  assert.equal(r.decision, "STATUS_PROMOTION_REJECTED");
  assert.ok(r.missing.length > 0);
});

test("PROVEN_ON_MODEL → SEALED still rejected even with partial evidence", () => {
  const r = evaluate("PROVEN_ON_MODEL", "SEALED", {
    implementation: true,
    tests: true
  });
  assert.equal(r.decision, "STATUS_PROMOTION_REJECTED");
});

test("FALSIFIED → PROVEN_ON_MODEL is rejected", () => {
  const r = evaluate("FALSIFIED", "PROVEN_ON_MODEL", { model_evidence: true, tlc_result: true });
  assert.equal(r.decision, "STATUS_PROMOTION_REJECTED");
});

test("NOT_PROVEN → SEALED is rejected", () => {
  const r = evaluate("NOT_PROVEN", "SEALED", {});
  assert.equal(r.decision, "STATUS_PROMOTION_REJECTED");
});

test("OPEN residual → CLOSED without closure_evidence is rejected", () => {
  const r = evaluate("OPEN", "CLOSED", {});
  assert.equal(r.decision, "STATUS_PROMOTION_REJECTED");
  assert.deepEqual(r.missing, ["closure_evidence"]);
});

test("PROVEN_ON_MODEL → PROVEN without refinement is rejected", () => {
  const r = evaluate("PROVEN_ON_MODEL", "PROVEN", { model_evidence: true, tlc_result: true });
  assert.equal(r.decision, "STATUS_PROMOTION_REJECTED");
});

// --- Legal advancement cases ---

test("Identity (same status) is ALLOW", () => {
  const r = evaluate("PROVEN_ON_MODEL", "PROVEN_ON_MODEL", {});
  assert.equal(r.decision, "ALLOW");
});

test("SPECIFIED → IMPLEMENTED with implementation evidence is ALLOW", () => {
  const r = evaluate("SPECIFIED", "IMPLEMENTED", { implementation: true });
  assert.equal(r.decision, "ALLOW");
});

test("IMPLEMENTED → TESTED with tests is ALLOW", () => {
  const r = evaluate("IMPLEMENTED", "TESTED", {
    implementation: true,
    tests: true
  });
  assert.equal(r.decision, "ALLOW");
});

test("NOT_PROVEN → PROVEN_ON_MODEL with model evidence is ALLOW", () => {
  const r = evaluate("NOT_PROVEN", "PROVEN_ON_MODEL", {
    model_evidence: true,
    tlc_result: "PROVEN_ON_MODEL"
  });
  assert.equal(r.decision, "ALLOW");
});

test("OPEN → CLOSED with closure_evidence is ALLOW", () => {
  const r = evaluate("OPEN", "CLOSED", { closure_evidence: "SWI-FM005-closure-v1" });
  assert.equal(r.decision, "ALLOW");
});

test("SEALED requires full evidence set", () => {
  const full = {
    implementation: true,
    tests: true,
    replay: true,
    evidence_hash: "abc123",
    required_review: true,
    runtime_correspondence: true
  };
  const r = evaluate("EVIDENCE_HASHED", "SEALED", full);
  assert.equal(r.decision, "ALLOW");
});

test("Missing any seal requirement causes rejection", () => {
  const almost = {
    implementation: true,
    tests: true,
    replay: true,
    evidence_hash: "abc123",
    required_review: true
  };
  const r = evaluate("EVIDENCE_HASHED", "SEALED", almost);
  assert.equal(r.decision, "STATUS_PROMOTION_REJECTED");
  assert.ok(r.missing.includes("runtime_correspondence"));
});

test("Missing current/requested is rejected", () => {
  const r = evaluate(null, "SEALED", {});
  assert.equal(r.decision, "STATUS_PROMOTION_REJECTED");
});

console.log("\n---");
console.log(`Passed: ${passed}`);
console.log(`Failed: ${failed}`);
if (failed > 0) process.exit(1);
