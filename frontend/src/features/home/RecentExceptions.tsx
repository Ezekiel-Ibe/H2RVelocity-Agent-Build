import type { PayrollException } from "@/contracts/schemas";
import styles from "./RecentExceptions.module.css";

const severityLabel: Record<string, string> = {
  high: "High",
  medium: "Medium",
  low: "Low",
};

export function RecentExceptions({ exceptions }: { exceptions: PayrollException[] }) {
  return (
    <section className={styles.card} aria-label="Recent exceptions">
      <div className={styles.head}>
        <h2 className={styles.heading}>Recent Exceptions</h2>
        <a href="#exceptions" className={styles.viewAll}>
          View all →
        </a>
      </div>
      <ul className={styles.list}>
        {exceptions.map((exc) => (
          <li key={exc.id} className={styles.item}>
            <span className={styles.badge} data-severity={exc.severity}>
              {severityLabel[exc.severity]}
            </span>
            <div className={styles.itemBody}>
              <p className={styles.title}>{exc.title}</p>
              <p className={styles.meta}>{exc.employeesAffected} employees affected</p>
            </div>
            <div className={styles.count}>
              <span className={styles.countValue}>{exc.count}</span>
              <span className={styles.countLabel}>Exceptions</span>
            </div>
          </li>
        ))}
      </ul>
    </section>
  );
}
