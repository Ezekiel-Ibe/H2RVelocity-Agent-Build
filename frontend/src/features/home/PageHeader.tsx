import styles from "./PageHeader.module.css";

export function PageHeader() {
  return (
    <header className={styles.header}>
      <div>
        <h1 className={styles.title}>Payroll Assurance Agent</h1>
        <p className={styles.subtitle}>
          AI-powered assurance for accurate, compliant and trusted payroll
        </p>
      </div>
      <p className={styles.tagline}>KPMG. Make the Difference.</p>
    </header>
  );
}
