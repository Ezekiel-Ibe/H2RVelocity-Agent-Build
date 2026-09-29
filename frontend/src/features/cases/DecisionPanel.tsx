import { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { submitCaseDecision } from "@/services/casesService";
import type { CaseDecision, DecisionAction } from "@/contracts/schemas";
import styles from "./DecisionPanel.module.css";

type Props = {
  caseId: string;
  allowedActions: DecisionAction[];
  decision: CaseDecision | null;
};

export function DecisionPanel({ caseId, allowedActions, decision }: Props) {
  const queryClient = useQueryClient();
  const [action, setAction] = useState<DecisionAction | null>(null);
  const [rationale, setRationale] = useState("");
  const [error, setError] = useState<string | null>(null);

  const mutation = useMutation({
    mutationFn: () => submitCaseDecision(caseId, action!, rationale.trim()),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["case", caseId] });
      queryClient.invalidateQueries({ queryKey: ["cases"] });
      queryClient.invalidateQueries({ queryKey: ["audit"] });
    },
  });

  // Already decided (immutable post-submit per A01 spec).
  if (decision) {
    return (
      <section className={styles.panel} aria-label="Decision">
        <h2 className={styles.heading}>Decision</h2>
        <p className={styles.recorded} role="status">
          <strong>{decision.action}</strong> recorded by {decision.decidedBy} on{" "}
          {decision.decidedOn}.
        </p>
        <p className={styles.rationale}>“{decision.rationale}”</p>
      </section>
    );
  }

  if (allowedActions.length === 0) {
    return (
      <section className={styles.panel} aria-label="Decision">
        <h2 className={styles.heading}>Decision</h2>
        <p className={styles.note}>No decision is required at this stage.</p>
      </section>
    );
  }

  if (mutation.isSuccess) {
    return (
      <section className={styles.panel} aria-label="Decision">
        <h2 className={styles.heading}>Decision</h2>
        <p className={styles.recorded} role="status">
          {mutation.data.outcome}
        </p>
      </section>
    );
  }

  function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    if (!action) {
      setError("Select an action.");
      return;
    }
    if (rationale.trim().length < 10) {
      setError("A rationale of at least 10 characters is required.");
      return;
    }
    mutation.mutate();
  }

  return (
    <section className={styles.panel} aria-label="Decision">
      <h2 className={styles.heading}>Human decision</h2>
      <p className={styles.note}>
        The agent recommends and prepares actions; only an authorised Payroll
        Controller may approve pay-impacting changes (CP05, CP06).
      </p>

      <form onSubmit={onSubmit}>
        <fieldset className={styles.actions}>
          <legend className={styles.legend}>Action</legend>
          {allowedActions.map((a) => (
            <label key={a} className={styles.action} data-action={a}>
              <input
                type="radio"
                name="decision-action"
                value={a}
                checked={action === a}
                onChange={() => setAction(a)}
              />
              {a}
            </label>
          ))}
        </fieldset>

        <label htmlFor="decision-rationale" className={styles.rationaleLabel}>
          Rationale <span aria-hidden="true">*</span>
        </label>
        <textarea
          id="decision-rationale"
          className={styles.textarea}
          value={rationale}
          onChange={(e) => setRationale(e.target.value)}
          rows={3}
          aria-required="true"
          placeholder="Record the reason for this decision (mandatory)…"
        />

        {error && (
          <p className={styles.error} role="alert">
            {error}
          </p>
        )}
        {mutation.isError && (
          <p className={styles.error} role="alert">
            Failed to record the decision. Please try again.
          </p>
        )}

        <button type="submit" className={styles.submit} disabled={mutation.isPending}>
          {mutation.isPending ? "Recording…" : "Submit decision"}
        </button>
      </form>
    </section>
  );
}
