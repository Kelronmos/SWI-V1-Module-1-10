/**
 * SWI V4.7 Status Engine (closed transition system)
 *
 * Pipeline:
 *   INPUT → null/empty check → unknown check → domain check
 *        → transition matrix → evidence check → ALLOW / REJECT
 *
 * NON-CLAIMS: not production proof, not FM-005 closure, not Universal Gate.
 */

export const CONSTRUCTION = Object.freeze([
  "PROPOSED", "MAPPED", "SPECIFIED", "IMPLEMENTED",
  "TESTED", "ADVERSARIALLY_TESTED", "REPLAY_VERIFIED",
  "EVIDENCE_HASHED", "SEALED"
]);

export const FORMAL = Object.freeze([
  "NOT_PROVEN", "PROVEN_ON_MODEL", "PROVEN", "FALSIFIED", "BOUND_ONLY"
]);

export const RESIDUAL = Object.freeze(["OPEN", "CLOSED", "INAPPLICABLE"]);

const CONSTRUCTION_SET = new Set(CONSTRUCTION);
const FORMAL_SET = new Set(FORMAL);
const RESIDUAL_SET = new Set(RESIDUAL);
const ALL_STATUSES = new Set([...CONSTRUCTION, ...FORMAL, ...RESIDUAL]);

/** Input-boundary tokens that must never enter transition logic as statuses */
const INPUT_BOUNDARY = new Set(["UNKNOWN", "UNDEFINED", "INVALID"]);

function domainOf(status) {
  if (CONSTRUCTION_SET.has(status)) return "construction";
  if (FORMAL_SET.has(status)) return "formal";
  if (RESIDUAL_SET.has(status)) return "residual";
  return null;
}

/**
 * Explicit transition matrix (closed).
 * Only listed edges are legal; everything else is REJECT unless identity.
 */
export const TRANSITIONS = Object.freeze({
  PROPOSED: Object.freeze(["MAPPED"]),
  MAPPED: Object.freeze(["SPECIFIED"]),
  SPECIFIED: Object.freeze(["IMPLEMENTED"]),
  IMPLEMENTED: Object.freeze(["TESTED"]),
  TESTED: Object.freeze(["ADVERSARIALLY_TESTED"]),
  ADVERSARIALLY_TESTED: Object.freeze(["REPLAY_VERIFIED"]),
  REPLAY_VERIFIED: Object.freeze(["EVIDENCE_HASHED"]),
  EVIDENCE_HASHED: Object.freeze(["SEALED"]),
  SEALED: Object.freeze([]),

  NOT_PROVEN: Object.freeze(["PROVEN_ON_MODEL", "BOUND_ONLY", "FALSIFIED"]),
  PROVEN_ON_MODEL: Object.freeze(["PROVEN"]),
  BOUND_ONLY: Object.freeze([]),
  FALSIFIED: Object.freeze([]),
  PROVEN: Object.freeze([]),

  OPEN: Object.freeze(["CLOSED"]),
  CLOSED: Object.freeze([]),
  INAPPLICABLE: Object.freeze([])
});

export const REQUIREMENTS = Object.freeze({
  MAPPED: Object.freeze(["mapping"]),
  SPECIFIED: Object.freeze(["specification"]),
  IMPLEMENTED: Object.freeze(["implementation"]),
  TESTED: Object.freeze(["implementation", "tests"]),
  ADVERSARIALLY_TESTED: Object.freeze(["implementation", "tests", "adversarial_tests"]),
  REPLAY_VERIFIED: Object.freeze(["implementation", "tests", "replay"]),
  EVIDENCE_HASHED: Object.freeze(["implementation", "tests", "replay", "evidence_hash"]),
  SEALED: Object.freeze([
    "implementation", "tests", "replay", "evidence_hash",
    "required_review", "runtime_correspondence"
  ]),
  PROVEN_ON_MODEL: Object.freeze(["model_evidence", "tlc_result"]),
  BOUND_ONLY: Object.freeze(["model_evidence", "bound_declaration"]),
  FALSIFIED: Object.freeze(["counterexample"]),
  PROVEN: Object.freeze([
    "model_evidence", "tlc_result", "runtime_correspondence", "refinement"
  ]),
  CLOSED: Object.freeze(["closure_evidence"])
});

function hasEvidence(evidence, key) {
  if (!evidence || typeof evidence !== "object" || Array.isArray(evidence)) return false;
  const v = evidence[key];
  if (v === true) return true;
  if (typeof v === "string" && v.trim().length > 0) return true;
  if (Array.isArray(v) && v.length > 0 && v.every(x => typeof x === "string" && x.trim().length > 0)) {
    return true;
  }
  if (v && typeof v === "object" && !Array.isArray(v)) {
    if (typeof v.id === "string" && v.id.trim().length > 0) return true;
    if (typeof v.hash === "string" && v.hash.trim().length > 0) return true;
    if (typeof v.sha256 === "string" && v.sha256.trim().length > 0) return true;
  }
  return false;
}

function missingKeys(evidence, keys) {
  return keys.filter(k => !hasEvidence(evidence, k));
}

function isAbsent(v) {
  return v === null || v === undefined;
}

function isEmptyString(v) {
  return typeof v === "string" && v.trim() === "";
}

export function evaluate(current, requested, evidence = {}) {
  if (isAbsent(current) || isAbsent(requested)) {
    return {
      decision: "STATUS_PROMOTION_REJECTED",
      current: isAbsent(current) ? null : current,
      requested: isAbsent(requested) ? null : requested,
      missing: ["current_status", "requested_status"].filter((_, i) =>
        i === 0 ? isAbsent(current) : isAbsent(requested)
      ),
      reason: "Status value absent (NULL)",
      code: "STATUS_VALUE_ABSENT"
    };
  }

  if (isEmptyString(current) || isEmptyString(requested)) {
    return {
      decision: "STATUS_PROMOTION_REJECTED",
      current: isEmptyString(current) ? null : current,
      requested: isEmptyString(requested) ? null : requested,
      missing: [],
      reason: "Status value empty",
      code: "STATUS_VALUE_EMPTY"
    };
  }

  if (INPUT_BOUNDARY.has(current) || INPUT_BOUNDARY.has(requested)) {
    return {
      decision: "STATUS_PROMOTION_REJECTED",
      current,
      requested,
      missing: [],
      reason: "Input-boundary token cannot enter transition graph",
      code: "STATUS_VALUE_UNRESOLVED"
    };
  }

  if (!ALL_STATUSES.has(current)) {
    return {
      decision: "STATUS_PROMOTION_REJECTED",
      current,
      requested,
      missing: [],
      reason: `Unknown current status: ${current}`,
      code: "STATUS_VALUE_UNDEFINED"
    };
  }
  if (!ALL_STATUSES.has(requested)) {
    return {
      decision: "STATUS_PROMOTION_REJECTED",
      current,
      requested,
      missing: [],
      reason: `Unknown requested status: ${requested}`,
      code: "STATUS_VALUE_UNDEFINED"
    };
  }

  if (current === requested) {
    return {
      decision: "ALLOW",
      current,
      requested,
      reason: "No change requested",
      code: "SWI-STATUS-IDENTITY"
    };
  }

  const dCur = domainOf(current);
  const dReq = domainOf(requested);
  if (dCur !== dReq) {
    return {
      decision: "STATUS_PROMOTION_REJECTED",
      current,
      requested,
      missing: [],
      reason: `Cross-domain transition forbidden: ${dCur} → ${dReq}`,
      code: "SWI-STATUS-CROSS-DOMAIN"
    };
  }

  const allowed = TRANSITIONS[current] || [];
  if (!allowed.includes(requested)) {
    return {
      decision: "STATUS_PROMOTION_REJECTED",
      current,
      requested,
      missing: [],
      reason: `Illegal transition: ${current} → ${requested} not in transition matrix`,
      code: "SWI-STATUS-ILLEGAL-JUMP"
    };
  }

  const required = REQUIREMENTS[requested];
  if (required) {
    const missing = missingKeys(evidence, required);
    if (missing.length > 0) {
      return {
        decision: "STATUS_PROMOTION_REJECTED",
        current,
        requested,
        missing: [...missing].sort(),
        reason: `Missing required evidence for ${requested}`,
        code: "SWI-STATUS-MISSING-EVIDENCE"
      };
    }
  }

  return {
    decision: "ALLOW",
    current,
    requested,
    reason: "Transition legal and required evidence present",
    code: "SWI-STATUS-ALLOW"
  };
}

export default {
  evaluate,
  TRANSITIONS,
  REQUIREMENTS,
  CONSTRUCTION,
  FORMAL,
  RESIDUAL
};
