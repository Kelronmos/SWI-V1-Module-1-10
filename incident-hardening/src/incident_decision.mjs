/**
 * SWI Incident decision helper (logic layer only).
 * Does NOT enforce network/process. enforcement_point remains OPEN until adapters exist.
 * NON-CLAIMS: not production boundary, not T10 pass, not SEALED.
 */

function absent(v) {
  return v === null || v === undefined || v === "" || v === "UNKNOWN";
}

export function evaluateIncident(input) {
  const i = input?.inputs || {};
  const reasons = [];

  if (i.declared_environment === "SIMULATED" && i.actual_network === "EXTERNAL") {
    reasons.push("SIMULATION_REALITY_MISMATCH");
  }
  if (i.target_declared && i.target_resolved && i.target_declared !== i.target_resolved) {
    reasons.push("TARGET_IDENTITY_MISMATCH");
  }
  if (i.credential_found && (absent(i.credential_authority) || i.credential_authority === "UNKNOWN")) {
    reasons.push("CREDENTIAL_WITHOUT_AUTHORITY");
  }
  if (i.hidden_channel) {
    reasons.push("UNAUTHORIZED_CHANNEL");
  }
  if (i.admission === "APPROVED" && i.environment_hash_at_admission && i.environment_hash_current
      && i.environment_hash_at_admission !== i.environment_hash_current) {
    reasons.push("ADMISSION_ENVIRONMENT_MISMATCH");
  }
  if (i.model_claim && typeof i.model_claim === "string") {
    reasons.push("MODEL_CLAIM_NOT_AUTHORITY");
  }
  if (i.network_policy === "NO_INTERNET" && i.actual_network === "EXTERNAL") {
    reasons.push("NETWORK_POLICY_VIOLATION");
  }
  if (i.force_execute_after_deny) {
    reasons.push("EXECUTION_AFTER_DENY_PATTERN");
  }

  const denied = reasons.length > 0;
  return {
    test_id: input?.test_id || null,
    decision: denied ? "DENIED" : "UNKNOWN",
    reason_codes: reasons,
    execution_occurred: false,
    boundary_enforced: false,
    enforcement_gap: true,
    status: denied ? "LOGIC_DENY" : "LOGIC_UNKNOWN",
    non_claims: [
      "Does not enforce network or process isolation",
      "boundary_enforced remains false until execution adapters exist",
      "LOGIC_DENY \u2260 T10 PASS"
    ]
  };
}

export default { evaluateIncident };
