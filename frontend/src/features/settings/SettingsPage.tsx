import { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { ArrowResetRegular, CheckmarkCircleRegular } from "@fluentui/react-icons";
import { resetDemoData } from "@/services/settingsService";
import styles from "./SettingsPage.module.css";

export function SettingsPage() {
  const queryClient = useQueryClient();
  const [confirming, setConfirming] = useState(false);

  const mutation = useMutation({
    mutationFn: resetDemoData,
    onSuccess: () => {
      setConfirming(false);
      // Refresh everything that reflects recorded decisions.
      queryClient.invalidateQueries();
    },
  });

  return (
    <div className={styles.page}>
      <header className={styles.header}>
        <h1 className={styles.title}>Settings</h1>
        <p className={styles.subtitle}>
          Manage workspace preferences and demonstration data.
        </p>
      </header>

      <section className={styles.card} aria-label="Demo data">
        <h2 className={styles.cardTitle}>Demo data</h2>
        <p className={styles.text}>
          This environment is for demonstration. Human approval decisions
          (Approve / Reject / Escalate) recorded against cases are stored so you
          can see them reflected across the case list, approvals queue and audit
          trail. Reset returns the workspace to its initial state.
        </p>

        {mutation.isSuccess && !confirming && (
          <p className={styles.success} role="status">
            <CheckmarkCircleRegular aria-hidden="true" />
            Demo data reset. Cleared {mutation.data.clearedDecisions} decision
            {mutation.data.clearedDecisions === 1 ? "" : "s"}.
          </p>
        )}
        {mutation.isError && (
          <p className={styles.error} role="alert">
            Couldn’t reset demo data. Please try again.
          </p>
        )}

        {confirming ? (
          <div className={styles.confirmRow}>
            <span className={styles.confirmText}>
              Reset all recorded decisions?
            </span>
            <button
              type="button"
              className={styles.danger}
              onClick={() => mutation.mutate()}
              disabled={mutation.isPending}
            >
              {mutation.isPending ? "Resetting…" : "Yes, reset"}
            </button>
            <button
              type="button"
              className={styles.secondary}
              onClick={() => setConfirming(false)}
              disabled={mutation.isPending}
            >
              Cancel
            </button>
          </div>
        ) : (
          <button
            type="button"
            className={styles.reset}
            onClick={() => {
              mutation.reset();
              setConfirming(true);
            }}
          >
            <ArrowResetRegular aria-hidden="true" />
            Reset demo data
          </button>
        )}
      </section>
    </div>
  );
}
