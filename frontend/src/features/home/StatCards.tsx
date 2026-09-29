import {
  DocumentRegular,
  PeopleRegular,
  WarningRegular,
  ShieldCheckmarkRegular,
  ArrowUpRegular,
  ArrowDownRegular,
} from "@fluentui/react-icons";
import type { StatCard } from "@/contracts/schemas";
import styles from "./StatCards.module.css";

const iconMap = {
  payrolls: <DocumentRegular />,
  employees: <PeopleRegular />,
  exceptions: <WarningRegular />,
  score: <ShieldCheckmarkRegular />,
};

export function StatCards({ stats }: { stats: StatCard[] }) {
  return (
    <section aria-label="Key metrics" className={styles.grid}>
      {stats.map((stat) => {
        const isUp = stat.trend.direction === "up";
        return (
          <article key={stat.id} className={styles.card}>
            <div className={styles.cardHead}>
              <span className={styles.label}>{stat.label}</span>
              <span className={styles.icon} aria-hidden="true">
                {iconMap[stat.icon]}
              </span>
            </div>
            <p className={styles.value}>{stat.value}</p>
            <p className={styles.caption}>{stat.caption}</p>
            <p className={styles.trend} data-direction={stat.trend.direction}>
              <span className={styles.trendIcon} aria-hidden="true">
                {isUp ? <ArrowUpRegular /> : <ArrowDownRegular />}
              </span>
              <span>
                {stat.trend.value} {stat.trend.label}
              </span>
            </p>
          </article>
        );
      })}
    </section>
  );
}
