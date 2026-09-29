import { Link } from "react-router-dom";
import type { AssuranceOverview as Overview } from "@/contracts/schemas";
import styles from "./AssuranceOverview.module.css";

const dotColor: Record<string, string> = {
  high: "var(--pa-viz-high)",
  medium: "var(--pa-viz-medium)",
  low: "var(--pa-viz-low)",
};

export function AssuranceOverview({ overview }: { overview: Overview }) {
  const radius = 54;
  const circumference = 2 * Math.PI * radius;
  const filled = (overview.score / 100) * circumference;

  return (
    <section className={styles.card} aria-label="Assurance overview">
      <h2 className={styles.heading}>Assurance Overview</h2>
      <div className={styles.body}>
        <div className={styles.donutWrap}>
          <svg
            className={styles.donut}
            viewBox="0 0 140 140"
            role="img"
            aria-label={`Assurance score ${overview.score} percent`}
          >
            <circle
              cx="70"
              cy="70"
              r={radius}
              fill="none"
              stroke="var(--pa-viz-track)"
              strokeWidth="14"
            />
            <circle
              cx="70"
              cy="70"
              r={radius}
              fill="none"
              stroke="var(--pa-brand-blue-bright)"
              strokeWidth="14"
              strokeLinecap="round"
              strokeDasharray={`${filled} ${circumference - filled}`}
              transform="rotate(-90 70 70)"
            />
          </svg>
          <div className={styles.donutLabel}>
            <span className={styles.donutValue}>{overview.score}%</span>
            <span className={styles.donutCaption}>Assurance Score</span>
          </div>
        </div>

        <table className={styles.legend}>
          <tbody>
            {overview.breakdown.map((row) => (
              <tr key={row.level}>
                <th scope="row" className={styles.legendLabel}>
                  <span
                    className={styles.dot}
                    style={{ background: dotColor[row.level] }}
                    aria-hidden="true"
                  />
                  {row.label}
                </th>
                <td className={styles.legendCount}>{row.count}</td>
                <td className={styles.legendPct}>{row.percentage}%</td>
              </tr>
            ))}
            <tr className={styles.totalRow}>
              <th scope="row" className={styles.legendLabel}>
                Total
              </th>
              <td className={styles.legendCount}>{overview.total}</td>
              <td className={styles.legendPct}>100%</td>
            </tr>
          </tbody>
        </table>
      </div>
      <p className={styles.footnote}>
        Score is based on the latest payroll run and assurance checks.{" "}
        <Link to="/insights" className={styles.link}>
          View full insights →
        </Link>
      </p>
    </section>
  );
}
