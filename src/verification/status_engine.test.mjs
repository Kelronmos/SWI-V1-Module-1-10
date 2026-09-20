/**
 * Adversarial / unit tests for SWI V4.7 Status Engine (hardened)
 */

import { evaluate, CONSTRUCTION, FORMAL, RESIDUAL } from "./status_engine.mjs";
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

test("Missing current is rejected", () => {
  const r = evaluate(null, "SEALED", {});
  assert.equal(r.decision, "STATUS_PROMOTION_REJECTED");
  assert.equal(r.code, "SWI-STATUS-MISSING");
});

test("Missing requested is rejected", () => {
  const r = evaluate("PROPOSED", null, {});
  assert.equal(r.decision, "STATUS_PROMOTION_REJECTED");
});

test("Empty-string status is rejected", () => {
  const r = evaluate("", "SEALED", {});
  assert.equal(r.decision, "STATUS_PROMOTION_REJECTED");
});

test("Unknown current status is rejected", () => {
  const r = evaluate("HACKED", "SEALED", {});
  assert.equal(r.decision, "STATUS_PROMOTION_REJECTED");
  assert.equal(r.code, "SWI-STATUS-UNKNOWN-CURRENT");
});

test("Unknown requested status is rejected", () => {
  const r = evaluate("PROPOSED", "SUPER_SEALED", {});
  assert.equal(r.decision, "STATUS_PROMOTION_REJECTED");
  assert.equal(r.code, "SWI-STATUS-UNKNOWN-REQUESTED");
});

test("Construction → formal is rejected", () => {
  const r = evaluate("IMPLEMENTED", "PROVEN_ON_MODEL", {
    model_evidence: true,
    tlc_result: true
  });
  assert.equal(r.decision, "STATUS_PROMOTION_REJECTED");
  assert.equal(r.code, "SWI-STATUS-CROSS-DOMAIN");
});

test("Formal → construction is rejected", () => {
  const r = evaluate("PROVEN_ON_MODEL", "SEALED", {
    implementation: true,
    tests: true,
    replay: true,
    evidence_hash: "abc",
    required_review: true,
    runtime_correspondence: true
  });
  assert.equal(r.decision, "STATUS_PROMOTION_REJECTED");
  assert.ok(
    r.code === "SWI-STATUS-HARD-BLOCK" || r.code === "SWI-STATUS-CROSS-DOMAIN"
  );
});

test("Residual → construction is rejected", () => {
  const r = evaluate("OPEN", "IMPLEMENTED", { implementation: true });
  assert.equal(r.decision, "STATUS_PROMOTION_REJECTED");
  assert.equal(r.code, "SWI-STATUS-CROSS-DOMAIN");
});

test("PROVEN_ON_MODEL → SEALED is hard-blocked", () => {
  const r = evaluate("PROVEN_ON_MODEL", "SEALED", {
    implementation: true,
    tests: true,
    replay: true,
    evidence_hash: "x",
    required_review: true,
    runtime_correspondence: true
  });
  assert.equal(r.decision, "STATUS_PROMOTION_REJECTED");
});

test("FALSIFIED → PROVEN_ON_MODEL is hard-blocked", () => {
  const r = evaluate("FALSIFIED", "PROVEN_ON_MODEL", {
    model_evidence: true,
    tlc_result: true
  });
  assert.equal(r.decision, "STATUS_PROMOTION_REJECTED");
  assert.equal(r.code, "SWI-STATUS-HARD-BLOCK");
});

test("NOT_PROVEN → SEALED is rejected", () => {
  const r = evaluate("NOT_PROVEN", "SEALED", {});
  assert.equal(r.decision, "STATUS_PROMOTION_REJECTED");
});

test("FALSIFIED → PROVEN is hard-blocked", () => {
  const r = evaluate("FALSIFIED", "PROVEN", {
    model_evidence: true,
    tlc_result: true,
    runtime_correspondence: true,
    refinement: true
  });
  assert.equal(r.decision, "STATUS_PROMOTION_REJECTED");
  assert.equal(r.code, "SWI-STATUS-HARD-BLOCK");
});

test("PROVEN_ON_MODEL → PROVEN without refinement is rejected", () => {
  const r = evaluate("PROVEN_ON_MODEL", "PROVEN", {
    model_evidence: true,
    tlc_result: true
  });
  assert.equal(r.decision, "STATUS_PROMOTION_REJECTED");
  assert.ok(r.missing.includes("refinement") || r.missing.includes("runtime_correspondence"));
});

test("PROVEN_ON_MODEL → PROVEN with full refinement evidence is ALLOW", () => {
  const r = evaluate("PROVEN_ON_MODEL", "PROVEN", {
    model_evidence: true,
    tlc_result: true,
    runtime_correspondence: "CORR-001",
    refinement: "REF-001"
  });
  assert.equal(r.decision, "ALLOW");
});

test("OPEN → CLOSED without closure_evidence is rejected", () => {
  const r = evaluate("OPEN", "CLOSED", {});
  assert.equal(r.decision, "STATUS_PROMOTION_REJECTED");
  assert.deepEqual(r.missing, ["closure_evidence"]);
});

test("OPEN → CLOSED with closure_evidence is ALLOW", () => {
  const r = evaluate("OPEN", "CLOSED", { closure_evidence: "SWI-FM005-closure-v1" });
  assert.equal(r.decision, "ALLOW");
});

test("Identity is ALLOW", () => {
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

test("Empty-string evidence is rejected", () => {
  const r = evaluate("SPECIFIED", "IMPLEMENTED", { implementation: "" });
  assert.equal(r.decision, "STATUS_PROMOTION_REJECTED");
});

test("False evidence is rejected", () => {
  const r = evaluate("SPECIFIED", "IMPLEMENTED", { implementation: false });
  assert.equal(r.decision, "STATUS_PROMOTION_REJECTED");
});

test("Empty-array evidence is rejected", () => {
  const r = evaluate("SPECIFIED", "IMPLEMENTED", { implementation: [] });
  assert.equal(r.decision, "STATUS_PROMOTION_REJECTED");
});

test("Empty-object evidence is rejected", () => {
  const r = evaluate("SPECIFIED", "IMPLEMENTED", { implementation: {} });
  assert.equal(r.decision, "STATUS_PROMOTION_REJECTED");
});

test("Object with id field is accepted", () => {
  const r = evaluate("SPECIFIED", "IMPLEMENTED", {
    implementation: { id: "impl-001" }
  });
  assert.equal(r.decision, "ALLOW");
});

test("Unrelated keys do not satisfy missing requirement", () => {
  const r = evaluate("SPECIFIED", "IMPLEMENTED", { unrelated: true });
  assert.equal(r.decision, "STATUS_PROMOTION_REJECTED");
  assert.ok(r.missing.includes("implementation"));
});

test("Extra evidence does not override missing required key", () => {
  const almost = {
    implementation: true,
    tests: true,
    replay: true,
    evidence_hash: "abc",
    required_review: true
  };
  const r = evaluate("EVIDENCE_HASHED", "SEALED", almost);
  assert.equal(r.decision, "STATUS_PROMOTION_REJECTED");
  assert.ok(r.missing.includes("runtime_correspondence"));
});

test("SEALED with full evidence set is ALLOW", () => {
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

test("Evidence object is not mutated", () => {
  const ev = { implementation: true };
  const copy = JSON.stringify(ev);
  evaluate("SPECIFIED", "IMPLEMENTED", ev);
  assert.equal(JSON.stringify(ev), copy);
});

test("Vocabulary sets are exported and non-empty", () => {
  assert.ok(CONSTRUCTION.length >= 9);
  assert.ok(FORMAL.length >= 4);
  assert.ok(RESIDUAL.length >= 3);
});

console.log("\n---");
console.log(`Passed: ${passed}`);
console.log(`Failed: ${failed}`);
if (failed > 0) process.exit(1);
