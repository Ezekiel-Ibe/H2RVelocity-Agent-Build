import { Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { fetchCases } from "@/services/casesService";
import { LoadingState, ErrorState, EmptyState } from "@/features/common/QueryStates";
import styles from "./ApprovalsPage.module.css";

export function ApprovalsPage() {
  const { data, isLoading, isError } = useQuery({
    queryKey: ["cases"],
    queryFn: fetchCases,
  });

  const awaiting = data?.filter((c) => c.status === "Awaiting Approval") ?? [];

  return (
    <div className={styles.page}>
      <header className={styles.header}>
        <h1 className={styles.title}>Approvals</h1>
        <p className={styles.subtitle}>
          Cases awaiting a Payroll Controller decision (CP05, CP06). The agent
          recommends; only an authorised approver may approve pay-impacting changes.
        </p>
      </header>

      {isLoading && <LoadingState label="Loading approvals…" />}
      {isError && <ErrorState message="We couldn’t load approvals. Please try again." />}

      {data && awaiting.length === 0 && (
        <EmptyState>No cases are awaiting approval.</EmptyState>
      )}

      {awaiting.length > 0 && (
        <section className={styles.card} aria-label="Awaiting approval">
          <table className={styles.table}>
            <thead>
              <tr>
                <th scope="col">Case ID</th>
                <th scope="col">Worker</th>
                <th scope="col">Anomaly</th>
                <th scope="col">Risk</th>
                <th scope="col">Current Step</th>
                <th scope="col" className={styles.actionCol}>
                  Action
                </th>
              </tr>
            </thead>
            <tbody>
              {awaiting.map((c) => (
                <tr key={c.id}>
                  <td className={styles.caseId}>{c.id}</td>
                  <td>{c.workerName}</td>
                  <td>
                    <span className={styles.anomaly} data-severity={c.severity}>
                      {c.anomalyTitle}
                    </span>
                  </td>
                  <td className={styles.risk}>{c.riskScore}</td>
                  <td className={styles.step}>{c.currentStep}</td>
                  <td className={styles.actionCol}>
                    <Link className={styles.review} to={`/cases/${c.id}`}>
                      Review & decide →
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      )}
    </div>
  );
}
