/**
 * SWI V4.7 Status Engine
 * Pure function. Mechanically enforces evidence-boundary rules.
 *
 * NON-CLAIMS:
 * - Does not prove production correctness
 * - Does not close FM-005
 * - Does not establish Universal Gate
 * - Does not invent evidence
 */

const CONSTRUCTION = new Set([
  "PROPOSED", "MAPPED", "SPECIFIED", "IMPLEMENTED",
  "TESTED", "ADVERSARIALLY_TESTED", "REPLAY_VERIFIED",
  "EVIDENCE_HASHED", "SEALED"
]);

const FORMAL = new Set([
  "NOT_PROVEN", "PROVEN_ON_MODEL", "PROVEN", "FALSIFIED", "BOUND_ONLY"
]);

const RESIDUAL = new Set(["OPEN", "CLOSED", "INAPPLICABLE"]);

/** Required evidence keys for each target status */
const REQUIREMENTS = {
  MAPPED: ["mapping"],
  SPECIFIED: ["specification"],
  IMPLEMENTED: ["implementation"],
  TESTED: ["implementation", "tests"],
  ADVERSARIALLY_TESTED: ["implementation", "tests", "adversarial_tests"],
  REPLAY_VERIFIED: ["implementation", "tests", "replay"],
  EVIDENCE_HASHED: ["implementation", "tests", "replay", "evidence_hash"],
  SEALED: [
    "implementation",
    "tests",
    "replay",
    "evidence_hash",
    "required_review",
    "runtime_correspondence"
  ],
  PROVEN_ON_MODEL: ["model_evidence", "tlc_result"],
  PROVEN: ["model_evidence", "tlc_result", "runtime_correspondence", "refinement"],
  CLOSED: ["closure_evidence"]
};

/** Illegal promotions that must always be rejected */
const HARD_BLOCKS = [
  { from: "PROVEN_ON_MODEL", to: "SEALED" },
  { from: "FALSIFIED", to: "PROVEN_ON_MODEL" },
  { from: "FALSIFIED", to: "PROVEN" },
  { from: "NOT_PROVEN", to: "SEALED" },
  { from: "PROVEN_ON_MODEL", to: "PROVEN" }
];

function hasEvidence(evidence, key) {
  if (!evidence || typeof evidence !== "object") return false;
  const v = evidence[key];
  if (v === true) return true;
  if (typeof v === "string" && v.length > 0) return true;
  if (Array.isArray(v) && v.length > 0) return true;
  if (v && typeof v === "object" && Object.keys(v).length > 0) return true;
  return false;
}

/**
 * Evaluate a status promotion request.
 * @param {string} current
 * @param {string} requested
 * @param {object} evidence
 * @returns {{ decision: string, current: string, requested: string, missing?: string[], reason?: string }}
 */
export function evaluate(current, requested, evidence = {}) {
  if (!current || !requested) {
    return {
      decision: "STATUS_PROMOTION_REJECTED",
      current: current || null,
      requested: requested || null,
      missing: ["current_status", "requested_status"],
      reason: "Both current and requested status are required"
    };
  }

  if (current === requested) {
    return {
      decision: "ALLOW",
      current,
      requested,
      reason: "No change requested"
    };
  }

  for (const block of HARD_BLOCKS) {
    if (current === block.from && requested === block.to) {
      const reqs = REQUIREMENTS[requested] || [];
      const missing = reqs.filter(k => !hasEvidence(evidence, k));
      return {
        decision: "STATUS_PROMOTION_REJECTED",
        current,
        requested,
        missing: missing.length ? missing : ["required_extra_evidence"],
        reason: `Hard block: ${current} cannot become ${requested} without additional independent evidence`
      };
    }
  }

  if (current === "OPEN" && requested === "CLOSED") {
    if (!hasEvidence(evidence, "closure_evidence")) {
      return {
        decision: "STATUS_PROMOTION_REJECTED",
        current,
        requested,
        missing: ["closure_evidence"],
        reason: "Residual OPEN cannot become CLOSED without closure_evidence"
      };
    }
  }

  const required = REQUIREMENTS[requested];
  if (required) {
    const missing = required.filter(k => !hasEvidence(evidence, k));
    if (missing.length > 0) {
      return {
        decision: "STATUS_PROMOTION_REJECTED",
        current,
        requested,
        missing,
        reason: `Missing required evidence for ${requested}`
      };
    }
  }

  return {
    decision: "ALLOW",
    current,
    requested,
    reason: "All required evidence present for requested transition"
  };
}

export default { evaluate, REQUIREMENTS, HARD_BLOCKS };
