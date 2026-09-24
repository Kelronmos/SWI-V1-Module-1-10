import { evaluate, TRANSITIONS, CONSTRUCTION, FORMAL, RESIDUAL } from "./status_engine.mjs";
import assert from "node:assert/strict";

let passed = 0, failed = 0;
function test(name, fn) {
  try { fn(); console.log("PASS:", name); passed++; }
  catch (e) { console.error("FAIL:", name, e.message); failed++; }
}

const SEAL_EV = {
  implementation: true, tests: true, replay: true,
  evidence_hash: "h", required_review: true, runtime_correspondence: true
};

test("NULL current rejected", () => {
  assert.equal(evaluate(null, "SEALED", {}).code, "STATUS_VALUE_ABSENT");
});
test("undefined requested rejected", () => {
  assert.equal(evaluate("PROPOSED", undefined, {}).code, "STATUS_VALUE_ABSENT");
});
test("empty string rejected", () => {
  assert.equal(evaluate("", "SEALED", {}).code, "STATUS_VALUE_EMPTY");
});
test("UNKNOWN current rejected", () => {
  assert.equal(evaluate("UNKNOWN", "UNKNOWN", {}).code, "STATUS_VALUE_UNRESOLVED");
});
test("UNKNOWN identity still rejected", () => {
  const r = evaluate("UNKNOWN", "UNKNOWN", {});
  assert.equal(r.decision, "STATUS_PROMOTION_REJECTED");
});
test("UNDEFINED rejected", () => {
  assert.equal(evaluate("UNDEFINED", "PROPOSED", {}).code, "STATUS_VALUE_UNRESOLVED");
});
test("INVALID rejected", () => {
  assert.equal(evaluate("INVALID", "SEALED", {}).code, "STATUS_VALUE_UNRESOLVED");
});
test("arbitrary unknown string rejected", () => {
  assert.equal(evaluate("HACKED", "SEALED", {}).code, "STATUS_VALUE_UNDEFINED");
});

test("construction → formal rejected", () => {
  assert.equal(evaluate("IMPLEMENTED", "PROVEN_ON_MODEL", {
    model_evidence: true, tlc_result: true
  }).code, "SWI-STATUS-CROSS-DOMAIN");
});
test("formal → construction rejected", () => {
  assert.equal(evaluate("PROVEN_ON_MODEL", "SEALED", SEAL_EV).code, "SWI-STATUS-CROSS-DOMAIN");
});
test("residual → construction rejected", () => {
  assert.equal(evaluate("OPEN", "IMPLEMENTED", { implementation: true }).code, "SWI-STATUS-CROSS-DOMAIN");
});
test("residual → formal rejected", () => {
  assert.equal(evaluate("OPEN", "PROVEN_ON_MODEL", {
    model_evidence: true, tlc_result: true
  }).code, "SWI-STATUS-CROSS-DOMAIN");
});

test("PROPOSED → SEALED illegal jump", () => {
  const r = evaluate("PROPOSED", "SEALED", SEAL_EV);
  assert.equal(r.decision, "STATUS_PROMOTION_REJECTED");
  assert.equal(r.code, "SWI-STATUS-ILLEGAL-JUMP");
});
test("SPECIFIED → SEALED illegal jump", () => {
  assert.equal(evaluate("SPECIFIED", "SEALED", SEAL_EV).code, "SWI-STATUS-ILLEGAL-JUMP");
});
test("IMPLEMENTED → SEALED illegal jump", () => {
  assert.equal(evaluate("IMPLEMENTED", "SEALED", SEAL_EV).code, "SWI-STATUS-ILLEGAL-JUMP");
});
test("OPEN → SEALED illegal (cross-domain)", () => {
  assert.equal(evaluate("OPEN", "SEALED", SEAL_EV).code, "SWI-STATUS-CROSS-DOMAIN");
});
test("PROPOSED → IMPLEMENTED illegal jump", () => {
  assert.equal(evaluate("PROPOSED", "IMPLEMENTED", { implementation: true }).code, "SWI-STATUS-ILLEGAL-JUMP");
});
test("TESTED → SEALED illegal jump", () => {
  assert.equal(evaluate("TESTED", "SEALED", SEAL_EV).code, "SWI-STATUS-ILLEGAL-JUMP");
});

test("PROPOSED → MAPPED with mapping ALLOW", () => {
  assert.equal(evaluate("PROPOSED", "MAPPED", { mapping: true }).decision, "ALLOW");
});
test("MAPPED → SPECIFIED with specification ALLOW", () => {
  assert.equal(evaluate("MAPPED", "SPECIFIED", { specification: true }).decision, "ALLOW");
});
test("SPECIFIED → IMPLEMENTED ALLOW", () => {
  assert.equal(evaluate("SPECIFIED", "IMPLEMENTED", { implementation: true }).decision, "ALLOW");
});
test("IMPLEMENTED → TESTED ALLOW", () => {
  assert.equal(evaluate("IMPLEMENTED", "TESTED", { implementation: true, tests: true }).decision, "ALLOW");
});
test("EVIDENCE_HASHED → SEALED with full evidence ALLOW", () => {
  assert.equal(evaluate("EVIDENCE_HASHED", "SEALED", SEAL_EV).decision, "ALLOW");
});
test("EVIDENCE_HASHED → SEALED missing runtime rejected", () => {
  const almost = { ...SEAL_EV }; delete almost.runtime_correspondence;
  const r = evaluate("EVIDENCE_HASHED", "SEALED", almost);
  assert.equal(r.decision, "STATUS_PROMOTION_REJECTED");
  assert.ok(r.missing.includes("runtime_correspondence"));
});

test("NOT_PROVEN → PROVEN_ON_MODEL ALLOW", () => {
  assert.equal(evaluate("NOT_PROVEN", "PROVEN_ON_MODEL", {
    model_evidence: true, tlc_result: "ok"
  }).decision, "ALLOW");
});
test("FALSIFIED → PROVEN_ON_MODEL illegal", () => {
  assert.equal(evaluate("FALSIFIED", "PROVEN_ON_MODEL", {
    model_evidence: true, tlc_result: true
  }).code, "SWI-STATUS-ILLEGAL-JUMP");
});
test("PROVEN_ON_MODEL → PROVEN without refinement rejected", () => {
  const r = evaluate("PROVEN_ON_MODEL", "PROVEN", {
    model_evidence: true, tlc_result: true
  });
  assert.equal(r.decision, "STATUS_PROMOTION_REJECTED");
  assert.ok(r.missing.includes("refinement"));
});
test("PROVEN_ON_MODEL → PROVEN with refinement ALLOW", () => {
  assert.equal(evaluate("PROVEN_ON_MODEL", "PROVEN", {
    model_evidence: true, tlc_result: true,
    runtime_correspondence: "c1", refinement: "r1"
  }).decision, "ALLOW");
});
test("NOT_PROVEN → FALSIFIED with counterexample ALLOW", () => {
  assert.equal(evaluate("NOT_PROVEN", "FALSIFIED", {
    counterexample: "trace-1"
  }).decision, "ALLOW");
});

test("OPEN → CLOSED without evidence rejected", () => {
  assert.equal(evaluate("OPEN", "CLOSED", {}).decision, "STATUS_PROMOTION_REJECTED");
});
test("OPEN → CLOSED with evidence ALLOW", () => {
  assert.equal(evaluate("OPEN", "CLOSED", { closure_evidence: "c" }).decision, "ALLOW");
});

test("Identity ALLOW for known status", () => {
  assert.equal(evaluate("PROVEN_ON_MODEL", "PROVEN_ON_MODEL", {}).decision, "ALLOW");
});

test("empty string evidence rejected", () => {
  assert.equal(evaluate("SPECIFIED", "IMPLEMENTED", { implementation: "" }).decision, "STATUS_PROMOTION_REJECTED");
});
test("empty object evidence rejected", () => {
  assert.equal(evaluate("SPECIFIED", "IMPLEMENTED", { implementation: {} }).decision, "STATUS_PROMOTION_REJECTED");
});
test("object with id accepted", () => {
  assert.equal(evaluate("SPECIFIED", "IMPLEMENTED", { implementation: { id: "i1" } }).decision, "ALLOW");
});
test("evidence not mutated", () => {
  const ev = { implementation: true };
  const c = JSON.stringify(ev);
  evaluate("SPECIFIED", "IMPLEMENTED", ev);
  assert.equal(JSON.stringify(ev), c);
});

test("construction chain fully linked", () => {
  const chain = [
    "PROPOSED", "MAPPED", "SPECIFIED", "IMPLEMENTED", "TESTED",
    "ADVERSARIALLY_TESTED", "REPLAY_VERIFIED", "EVIDENCE_HASHED", "SEALED"
  ];
  for (let i = 0; i < chain.length - 1; i++) {
    assert.ok(TRANSITIONS[chain[i]].includes(chain[i + 1]), `${chain[i]} → ${chain[i+1]}`);
  }
});

test("vocabulary exported", () => {
  assert.ok(CONSTRUCTION.length >= 9);
  assert.ok(FORMAL.length >= 4);
  assert.ok(RESIDUAL.length >= 3);
});

console.log("\n---");
console.log(`Passed: ${passed}`);
console.log(`Failed: ${failed}`);
if (failed > 0) process.exit(1);
