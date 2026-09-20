/**
 * SWI V4.7 Status Engine (hardened)
 * Pure function. Mechanically enforces evidence-boundary rules.
 *
 * NON-CLAIMS:
 * - Does not prove production correctness
 * - Does not close FM-005
 * - Does not establish Universal Gate
 * - Does not invent evidence
 *
 * Tracks (closed, independent):
 *   construction | formal | residual
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

function domainOf(status) {
  if (CONSTRUCTION_SET.has(status)) return "construction";
  if (FORMAL_SET.has(status)) return "formal";
  if (RESIDUAL_SET.has(status)) return "residual";
  return null;
}

/** Required evidence keys for each target status */
export const REQUIREMENTS = Object.freeze({
  MAPPED: Object.freeze(["mapping"]),
  SPECIFIED: Object.freeze(["specification"]),
  IMPLEMENTED: Object.freeze(["implementation"]),
  TESTED: Object.freeze(["implementation", "tests"]),
  ADVERSARIALLY_TESTED: Object.freeze(["implementation", "tests", "adversarial_tests"]),
  REPLAY_VERIFIED: Object.freeze(["implementation", "tests", "replay"]),
  EVIDENCE_HASHED: Object.freeze(["implementation", "tests", "replay", "evidence_hash"]),
  SEALED: Object.freeze([
    "implementation",
    "tests",
    "replay",
    "evidence_hash",
    "required_review",
    "runtime_correspondence"
  ]),
  PROVEN_ON_MODEL: Object.freeze(["model_evidence", "tlc_result"]),
  PROVEN: Object.freeze([
    "model_evidence",
    "tlc_result",
    "runtime_correspondence",
    "refinement"
  ]),
  CLOSED: Object.freeze(["closure_evidence"])
});

/**
 * Unconditional hard blocks.
 * PROVEN_ON_MODEL → PROVEN is NOT listed here; it is governed by REQUIREMENTS.PROVEN
 * (requires runtime_correspondence + refinement). That aligns code with the documented policy.
 */
export const HARD_BLOCKS = Object.freeze([
  Object.freeze({ from: "PROVEN_ON_MODEL", to: "SEALED" }),
  Object.freeze({ from: "FALSIFIED", to: "PROVEN_ON_MODEL" }),
  Object.freeze({ from: "FALSIFIED", to: "PROVEN" }),
  Object.freeze({ from: "NOT_PROVEN", to: "SEALED" }),
  Object.freeze({ from: "FALSIFIED", to: "SEALED" }),
  Object.freeze({ from: "BOUND_ONLY", to: "SEALED" }),
  Object.freeze({ from: "BOUND_ONLY", to: "PROVEN" })
]);

/**
 * Evidence acceptance policy (stricter than original truthy check).
 */
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

/**
 * Evaluate a status promotion request.
 */
export function evaluate(current, requested, evidence = {}) {
  if (current == null || current === "" || requested == null || requested === "") {
    return {
      decision: "STATUS_PROMOTION_REJECTED",
      current: current == null || current === "" ? null : current,
      requested: requested == null || requested === "" ? null : requested,
      missing: ["current_status", "requested_status"].filter((_, i) =>
        i === 0 ? (current == null || current === "") : (requested == null || requested === "")
      ),
      reason: "Both current and requested status are required",
      code: "SWI-STATUS-MISSING"
    };
  }

  if (!ALL_STATUSES.has(current)) {
    return {
      decision: "STATUS_PROMOTION_REJECTED",
      current,
      requested,
      missing: [],
      reason: `Unknown current status: ${current}`,
      code: "SWI-STATUS-UNKNOWN-CURRENT"
    };
  }
  if (!ALL_STATUSES.has(requested)) {
    return {
      decision: "STATUS_PROMOTION_REJECTED",
      current,
      requested,
      missing: [],
      reason: `Unknown requested status: ${requested}`,
      code: "SWI-STATUS-UNKNOWN-REQUESTED"
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

  for (const block of HARD_BLOCKS) {
    if (current === block.from && requested === block.to) {
      return {
        decision: "STATUS_PROMOTION_REJECTED",
        current,
        requested,
        missing: ["required_extra_evidence"],
        reason: `Hard block: ${current} cannot become ${requested}`,
        code: "SWI-STATUS-HARD-BLOCK"
      };
    }
  }

  if (current === "OPEN" && requested === "CLOSED") {
    const missing = missingKeys(evidence, REQUIREMENTS.CLOSED);
    if (missing.length > 0) {
      return {
        decision: "STATUS_PROMOTION_REJECTED",
        current,
        requested,
        missing,
        reason: "Residual OPEN cannot become CLOSED without closure_evidence",
        code: "SWI-STATUS-RESIDUAL-OPEN"
      };
    }
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
    reason: "All required evidence present for requested transition",
    code: "SWI-STATUS-ALLOW"
  };
}

export default {
  evaluate,
  REQUIREMENTS,
  HARD_BLOCKS,
  CONSTRUCTION,
  FORMAL,
  RESIDUAL
};
