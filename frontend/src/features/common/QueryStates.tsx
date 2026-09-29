import type { ReactNode } from "react";
import styles from "./QueryStates.module.css";

export function LoadingState({ label }: { label: string }) {
  return (
    <p role="status" className={styles.status}>
      {label}
    </p>
  );
}

export function ErrorState({ message }: { message: string }) {
  return (
    <p role="alert" className={styles.error}>
      {message}
    </p>
  );
}

export function EmptyState({ children }: { children: ReactNode }) {
  return <p className={styles.empty}>{children}</p>;
}
