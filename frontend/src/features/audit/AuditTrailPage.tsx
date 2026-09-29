import { useQuery } from "@tanstack/react-query";
import { fetchAuditTrail } from "@/services/auditService";
import { LoadingState, ErrorState, EmptyState } from "@/features/common/QueryStates";
import styles from "./AuditTrailPage.module.css";

export function AuditTrailPage() {
  const { data, isLoading, isError } = useQuery({
    queryKey: ["audit"],
    queryFn: fetchAuditTrail,
  });

  return (
    <div className={styles.page}>
      <header className={styles.header}>
        <h1 className={styles.title}>Audit Trail</h1>
        <p className={styles.subtitle}>
          Governance actions, decisions and evidence lineage recorded by the
          Governance &amp; Audit Agent (CP08, CP09) and the Orchestrator (CP10).
        </p>
      </header>

      {isLoading && <LoadingState label="Loading audit trail…" />}
      {isError && <ErrorState message="We couldn’t load the audit trail. Please try again." />}

      {data && data.length === 0 && <EmptyState>No audit events recorded.</EmptyState>}

      {data && data.length > 0 && (
        <section className={styles.card} aria-label="Audit events">
          <ol className={styles.timeline}>
            {data.map((e) => (
              <li key={e.id} className={styles.event}>
                <span className={styles.dot} aria-hidden="true" />
                <div className={styles.body}>
                  <div className={styles.row}>
                    <span className={styles.action}>{e.action}</span>
                    <span className={styles.control}>{e.control}</span>
                  </div>
                  <p className={styles.detail}>{e.detail}</p>
                  <p className={styles.meta}>
                    {e.timestamp} · {e.actor} · case {e.caseRef} · {e.id}
                  </p>
                </div>
              </li>
            ))}
          </ol>
        </section>
      )}
    </div>
  );
}
