import styles from "./WelcomeBanner.module.css";

export function WelcomeBanner() {
  return (
    <section className={styles.banner} aria-label="Welcome">
      <div className={styles.content}>
        <h2 className={styles.heading}>Welcome back, KPMG User</h2>
        <p className={styles.text}>
          Here’s what’s happening with your payroll assurance engagement.
        </p>
      </div>
      <div className={styles.wave} aria-hidden="true" />
    </section>
  );
}
