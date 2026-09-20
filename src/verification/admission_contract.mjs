export class AdmissionRequiredError extends Error {
  constructor(message = "Admission required") {
    super(message);
    this.name = "AdmissionRequiredError";
    this.code = "ADMISSION_REQUIRED";
  }
}

export function assertAdmission(admission, opts = {}) {
  if (opts.testOnlyBypass === true) {
    return { mode: "TEST_ONLY", admitted: false };
  }
  if (!admission || admission.valid !== true) {
    throw new AdmissionRequiredError("missing or invalid admission");
  }
  return { mode: "PRODUCTION", admitted: true, admission };
}

export function runWithAdmission(admission, operation, opts = {}) {
  assertAdmission(admission, opts);
  if (typeof operation !== "function") throw new TypeError("operation must be a function");
  return operation();
}
