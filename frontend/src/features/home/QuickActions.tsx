import {
  ArrowUploadRegular,
  ShieldCheckmarkRegular,
  DataTrendingRegular,
  DocumentTextRegular,
} from "@fluentui/react-icons";
import { useState, type ReactNode } from "react";
import { useNavigate } from "react-router-dom";
import { RunAssuranceModal } from "./RunAssuranceModal";
import styles from "./QuickActions.module.css";

type QuickAction = {
  id: string;
  label: string;
  icon: ReactNode;
  to?: string;
};

const actions: QuickAction[] = [
  { id: "upload", label: "Upload Payroll Data", icon: <ArrowUploadRegular /> },
  { id: "run", label: "Run Assurance Checks", icon: <ShieldCheckmarkRegular /> },
  { id: "insights", label: "View Key Insights", icon: <DataTrendingRegular />, to: "/insights" },
  { id: "report", label: "Generate Report", icon: <DocumentTextRegular /> },
];

export function QuickActions() {
  const navigate = useNavigate();
  const [runOpen, setRunOpen] = useState(false);

  function onAction(action: QuickAction) {
    if (action.id === "run") {
      setRunOpen(true);
    } else if (action.to) {
      navigate(action.to);
    }
  }

  return (
    <>
      <section aria-label="Quick actions" className={styles.grid}>
        {actions.map((action) => (
          <button
            key={action.id}
            type="button"
            className={styles.action}
            onClick={() => onAction(action)}
          >
            <span className={styles.icon} aria-hidden="true">
              {action.icon}
            </span>
            <span className={styles.label}>{action.label}</span>
          </button>
        ))}
      </section>
      {runOpen && <RunAssuranceModal onClose={() => setRunOpen(false)} />}
    </>
  );
}
