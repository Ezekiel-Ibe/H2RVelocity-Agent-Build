import { useEffect, useMemo, useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { DismissRegular, ShieldCheckmarkRegular } from "@fluentui/react-icons";
import { fetchPeriods } from "@/services/periodsService";
import { runAssurance } from "@/services/assuranceService";
import styles from "./RunAssuranceModal.module.css";

type Props = { onClose: () => void };

// App period ids look like "PP-2026-06"; the agent expects "2026-06".
function toPeriodId(appPeriodId: string): string {
  return appPeriodId.replace(/^PP-/, "");
}

export function RunAssuranceModal({ onClose }: Props) {
  const queryClient = useQueryClient();
  const { data: periods } = useQuery({ queryKey: ["periods"], queryFn: fetchPeriods });

  const [appPeriodId, setAppPeriodId] = useState("");
  const [payrollRunId, setPayrollRunId] = useState("");
  const [runIdEdited, setRunIdEdited] = useState(false);

  // Default the first period once loaded.
  useEffect(() => {
    if (!appPeriodId && periods && periods.length > 0) {
      setAppPeriodId(periods[0].id);
    }
  }, [periods, appPeriodId]);

  const periodId = useMemo(() => toPeriodId(appPeriodId), [appPeriodId]);

  // Keep the run id in step with the period unless the user typed their own.
  useEffect(() => {
    if (!runIdEdited && periodId) {
      setPayrollRunId(`PR-${periodId}`);
    }
  }, [periodId, runIdEdited]);

  const mutation = useMutation({
    mutationFn: () => runAssurance(payrollRunId.trim(), periodId),
    onSuccess: () => {
      // The agent wrote closure state to Fabric — refresh the read views.
      queryClient.invalidateQueries({ queryKey: ["cases"] });
      queryClient.invalidateQueries({ queryKey: ["dashboard"] });
      queryClient.invalidateQueries({ queryKey: ["audit"] });
      queryClient.invalidateQueries({ queryKey: ["insights"] });
    },
  });

  const summary = mutation.data;
  const closed = summary?.case_state === "CLOSED";
  const held = summary?.case_state === "HELD_FOR_REVIEW";

  return (
    <div className={styles.overlay} role="dialog" aria-modal="true" aria-label="Run assurance checks">
      <div className={styles.panel}>
        <header className={styles.header}>
          <h2 className={styles.title}>
            <ShieldCheckmarkRegular aria-hidden="true" /> Run Assurance Checks
          </h2>
          <button type="button" className={styles.close} onClick={onClose} aria-label="Close">
            <DismissRegular />
          </button>
        </header>

        {!summary && (
          <form
            className={styles.form}
            onSubmit={(e) => {
              e.preventDefault();
              if (payrollRunId.trim() && periodId) mutation.mutate();
            }}
          >
            <p className={styles.note}>
              Triggers the deterministic payroll assurance workflow (W01–W20). The agent
              runs the governance gates and writes the closed case + audit evidence.
            </p>

            <label className={styles.label} htmlFor="ra-period">
              Period
            </label>
            <select
              id="ra-period"
              className={styles.input}
              value={appPeriodId}
              onChange={(e) => setAppPeriodId(e.target.value)}
            >
              {(periods ?? []).map((p) => (
                <option key={p.id} value={p.id}>
                  {p.name} ({toPeriodId(p.id)})
                </option>
              ))}
            </select>

            <label className={styles.label} htmlFor="ra-run">
              Payroll Run ID
            </label>
            <input
              id="ra-run"
              className={styles.input}
              value={payrollRunId}
              onChange={(e) => {
                setRunIdEdited(true);
                setPayrollRunId(e.target.value);
              }}
              placeholder="PR-2026-06"
            />

            {mutation.isError && (
              <p className={styles.error} role="alert">
                Couldn’t reach the assurance agent. Please try again.
              </p>
            )}

            <div className={styles.actions}>
              <button type="button" className={styles.secondary} onClick={onClose} disabled={mutation.isPending}>
                Cancel
              </button>
              <button
                type="submit"
                className={styles.run}
                disabled={mutation.isPending || !payrollRunId.trim() || !periodId}
              >
                {mutation.isPending ? "Running… (up to ~20s)" : "Run assurance"}
              </button>
            </div>
          </form>
        )}

        {summary && (
          <div className={styles.result}>
            {summary.success === false && !held ? (
              <p className={styles.error} role="alert">
                Run failed: {summary.error ?? "unknown error"}
                {summary.detail ? ` — ${summary.detail}` : ""}
              </p>
            ) : (
              <>
                <p
                  className={closed ? styles.badgeOk : styles.badgeHold}
                  role="status"
                >
                  {closed ? "Case CLOSED" : held ? "HELD FOR REVIEW" : summary.case_state}
                </p>
                <dl className={styles.grid}>
                  <dt>Case</dt>
                  <dd>{summary.case_id ?? "—"}</dd>
                  <dt>Risk</dt>
                  <dd>
                    {summary.risk_band ?? "—"}
                    {typeof summary.risk_score === "number" ? ` (${summary.risk_score})` : ""}
                  </dd>
                  <dt>Anomalies</dt>
                  <dd>
                    {summary.total_anomalies ?? 0}
                    {typeof summary.high_severity_count === "number"
                      ? ` (${summary.high_severity_count} high)`
                      : ""}
                  </dd>
                  <dt>Corrections</dt>
                  <dd>{summary.committed_corrections ?? 0}</dd>
                  <dt>Sign-off</dt>
                  <dd className={styles.mono}>{summary.signoff_token ?? "—"}</dd>
                  <dt>Manifest</dt>
                  <dd className={styles.mono}>
                    {summary.manifest_hash ? `${summary.manifest_hash.slice(0, 16)}…` : "—"}
                  </dd>
                </dl>
                {held && (
                  <p className={styles.note}>
                    A governance gate (input validation, segregation of duties, or closure
                    attestation) held this case for review. This is a valid outcome, not a system error.
                  </p>
                )}
              </>
            )}
            <div className={styles.actions}>
              <button type="button" className={styles.run} onClick={onClose}>
                Done
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
