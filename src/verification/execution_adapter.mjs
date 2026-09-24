export function createExecutionAdapter() {
  const metrics = { execution_attempts: 0, execution_successes: 0, side_effects: 0 };

  function execute(decision, operation) {
    metrics.execution_attempts++;
    if (decision !== "ALLOW" && decision !== "APPROVED") {
      return { decision, invoked: false, result: null, metrics: { ...metrics } };
    }
    metrics.execution_successes++;
    const result = typeof operation === "function" ? operation() : null;
    metrics.side_effects++;
    return { decision, invoked: true, result, metrics: { ...metrics } };
  }

  return {
    execute,
    getMetrics: () => ({ ...metrics }),
    reset: () => {
      metrics.execution_attempts = 0;
      metrics.execution_successes = 0;
      metrics.side_effects = 0;
    }
  };
}
