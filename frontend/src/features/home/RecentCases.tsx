import type { PayrollCase } from "@/contracts/schemas";
import styles from "./RecentCases.module.css";

const statusTone: Record<string, string> = {
  Detected: "info",
  "In Analysis": "info",
  "Awaiting Approval": "medium",
  Approved: "success",
  Correcting: "info",
  Validating: "info",
  Closed: "muted",
  Escalated: "high",
};

export function RecentCases({ cases }: { cases: PayrollCase[] }) {
  return (
    <section className={styles.card} aria-label="Recent cases">
      <div className={styles.head}>
        <h2 className={styles.heading}>Recent Cases</h2>
        <a href="/cases" className={styles.viewAll}>
          View all cases →
        </a>
      </div>
      <table className={styles.table}>
        <thead>
          <tr>
            <th scope="col">Case ID</th>
            <th scope="col">Worker</th>
            <th scope="col">Pay Period</th>
            <th scope="col">Anomaly</th>
            <th scope="col">Risk</th>
            <th scope="col">Status</th>
            <th scope="col">Updated</th>
          </tr>
        </thead>
        <tbody>
          {cases.map((c) => (
            <tr key={c.id}>
              <td className={styles.caseId}>{c.id}</td>
              <td>{c.workerName}</td>
              <td>{c.payPeriod}</td>
              <td className={styles.anomaly}>{c.anomalyTitle}</td>
              <td className={styles.risk}>{c.riskScore}</td>
              <td>
                <span className={styles.status} data-tone={statusTone[c.status]}>
                  {c.status}
                </span>
              </td>
              <td>{c.lastUpdated}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}
