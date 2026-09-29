import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { fetchExceptions } from "@/services/exceptionsService";
import type { RiskLevel } from "@/contracts/schemas";
import { LoadingState, ErrorState, EmptyState } from "@/features/common/QueryStates";
import styles from "./ExceptionsPage.module.css";

type Filter = "all" | RiskLevel;

const filters: { id: Filter; label: string }[] = [
  { id: "all", label: "All" },
  { id: "high", label: "High" },
  { id: "medium", label: "Medium" },
  { id: "low", label: "Low" },
];

const severityLabel: Record<RiskLevel, string> = {
  high: "High",
  medium: "Medium",
  low: "Low",
};

export function ExceptionsPage() {
  const [filter, setFilter] = useState<Filter>("all");
  const { data, isLoading, isError } = useQuery({
    queryKey: ["exceptions"],
    queryFn: fetchExceptions,
  });

  const visible = data?.filter((e) => filter === "all" || e.severity === filter) ?? [];

  return (
    <div className={styles.page}>
      <header className={styles.header}>
        <h1 className={styles.title}>Exceptions</h1>
        <p className={styles.subtitle}>
          Review payroll exceptions and supporting evidence.
        </p>
      </header>

      {isLoading && <LoadingState label="Loading exceptions…" />}
      {isError && <ErrorState message="We couldn’t load exceptions. Please try again." />}

      {data && (
        <>
          <div className={styles.filters} role="group" aria-label="Filter by severity">
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
            <EmptyState>No exceptions match the selected filter.</EmptyState>
          ) : (
            <section className={styles.card} aria-label="Exceptions">
              <table className={styles.table}>
                <thead>
                  <tr>
                    <th scope="col">Severity</th>
                    <th scope="col">Anomaly</th>
                    <th scope="col">Case</th>
                    <th scope="col">Worker</th>
                    <th scope="col">Employees</th>
                    <th scope="col">Status</th>
                    <th scope="col">Detected</th>
                  </tr>
                </thead>
                <tbody>
                  {visible.map((exc) => (
                    <tr key={exc.id}>
                      <td>
                        <span className={styles.badge} data-severity={exc.severity}>
                          {severityLabel[exc.severity]}
                        </span>
                      </td>
                      <td>
                        <p className={styles.excTitle}>{exc.title}</p>
                        <p className={styles.excDesc}>{exc.description}</p>
                      </td>
                      <td className={styles.caseRef}>{exc.caseRef}</td>
                      <td>{exc.workerName}</td>
                      <td className={styles.num}>{exc.employeesAffected}</td>
                      <td>{exc.status}</td>
                      <td>{exc.detectedOn}</td>
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
