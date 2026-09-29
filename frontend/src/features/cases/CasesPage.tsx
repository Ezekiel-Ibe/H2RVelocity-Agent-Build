import { useState } from "react";
import { Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { fetchCases } from "@/services/casesService";
import type { CaseStatus } from "@/contracts/schemas";
import { LoadingState, ErrorState, EmptyState } from "@/features/common/QueryStates";
import styles from "./CasesPage.module.css";

type Filter = "all" | "open" | "closed";

const filters: { id: Filter; label: string }[] = [
  { id: "all", label: "All" },
  { id: "open", label: "Open" },
  { id: "closed", label: "Closed" },
];

const statusTone: Record<CaseStatus, string> = {
  Detected: "info",
  "In Analysis": "info",
  "Awaiting Approval": "medium",
  Approved: "success",
  Correcting: "info",
  Validating: "info",
  Closed: "muted",
  Escalated: "high",
};

export function CasesPage() {
  const [filter, setFilter] = useState<Filter>("all");
  const { data, isLoading, isError } = useQuery({
    queryKey: ["cases"],
    queryFn: fetchCases,
  });

  const visible =
    data?.filter((c) =>
      filter === "all"
        ? true
        : filter === "closed"
          ? c.status === "Closed"
          : c.status !== "Closed",
    ) ?? [];

  return (
    <div className={styles.page}>
      <header className={styles.header}>
        <h1 className={styles.title}>Cases</h1>
        <p className={styles.subtitle}>
          Payroll assurance cases for review, approval and evidence.
        </p>
      </header>

      {isLoading && <LoadingState label="Loading cases…" />}
      {isError && <ErrorState message="We couldn’t load cases. Please try again." />}

      {data && (
        <>
          <div className={styles.filters} role="group" aria-label="Filter cases">
            {filters.map((f) => (
              <button
                key={f.id}
                type="button"
                className={styles.filter}
                aria-pressed={filter === f.id}
                onClick={() => setFilter(f.id)}
              >
                {f.label}
              </button>
            ))}
          </div>

          {visible.length === 0 ? (
            <EmptyState>No cases match the selected filter.</EmptyState>
          ) : (
            <section className={styles.card} aria-label="Cases">
              <table className={styles.table}>
                <thead>
                  <tr>
                    <th scope="col">Case ID</th>
                    <th scope="col">Worker</th>
                    <th scope="col">Pay Period</th>
                    <th scope="col">Anomaly</th>
                    <th scope="col">Risk</th>
                    <th scope="col">Status</th>
                    <th scope="col">Current Step</th>
                    <th scope="col">Updated</th>
                  </tr>
                </thead>
                <tbody>
                  {visible.map((c) => (
                    <tr key={c.id}>
                      <td className={styles.caseId}>
                        <Link to={`/cases/${c.id}`}>{c.id}</Link>
                      </td>
                      <td>{c.workerName}</td>
                      <td>{c.payPeriod}</td>
                      <td>
                        <span className={styles.anomaly} data-severity={c.severity}>
                          {c.anomalyTitle}
                        </span>
                      </td>
                      <td className={styles.risk}>{c.riskScore}</td>
                      <td>
                        <span className={styles.status} data-tone={statusTone[c.status]}>
                          {c.status}
                        </span>
                      </td>
                      <td className={styles.step}>{c.currentStep}</td>
                      <td>{c.lastUpdated}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </section>
          )}
        </>
      )}
    </div>
  );
}
