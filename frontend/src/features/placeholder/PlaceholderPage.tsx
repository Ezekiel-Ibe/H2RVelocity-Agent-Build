import type { ReactNode } from "react";
import styles from "./PlaceholderPage.module.css";

type Props = {
  title: string;
  description: string;
  icon: ReactNode;
};

export function PlaceholderPage({ title, description, icon }: Props) {
  return (
    <div className={styles.page}>
      <header className={styles.header}>
        <h1 className={styles.title}>{title}</h1>
        <p className={styles.subtitle}>{description}</p>
      </header>
      <section className={styles.panel} aria-label={`${title} placeholder`}>
        <span className={styles.icon} aria-hidden="true">
          {icon}
        </span>
        <h2 className={styles.heading}>Coming soon</h2>
        <p className={styles.text}>
          This area is scaffolded and will be wired to governed backend services
          once approved API contracts and endpoints are available. No authoritative
          payroll data is shown here.
        </p>
      </section>
    </div>
  );
}
