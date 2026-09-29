import type { ReactNode } from "react";
import {
  Home24Regular,
  BriefcaseRegular,
  WarningRegular,
  CheckmarkCircleRegular,
  HistoryRegular,
  DocumentTextRegular,
  DataTrendingRegular,
  SettingsRegular,
} from "@fluentui/react-icons";

export type NavItem = {
  id: string;
  label: string;
  path: string;
  icon: ReactNode;
  description: string;
  expandable?: boolean;
};

export const navItems: NavItem[] = [
  {
    id: "home",
    label: "Home",
    path: "/",
    icon: <Home24Regular />,
    description: "Overview of your payroll assurance engagement.",
  },
  {
    id: "cases",
    label: "Cases",
    path: "/cases",
    icon: <BriefcaseRegular />,
    description: "Payroll assurance cases for review, approval and evidence.",
  },
  {
    id: "exceptions",
    label: "Exceptions",
    path: "/exceptions",
    icon: <WarningRegular />,
    description: "Review payroll exceptions and supporting evidence.",
  },
  {
    id: "approvals",
    label: "Approvals",
    path: "/approvals",
    icon: <CheckmarkCircleRegular />,
    description: "Cases awaiting a Payroll Controller decision.",
  },
  {
    id: "audit",
    label: "Audit Trail",
    path: "/audit",
    icon: <HistoryRegular />,
    description: "Governance actions, decisions and evidence lineage.",
  },
  {
    id: "reports",
    label: "Reports",
    path: "/reports",
    icon: <DocumentTextRegular />,
    description: "Generate and view assurance reports.",
  },
  {
    id: "insights",
    label: "Insights",
    path: "/insights",
    icon: <DataTrendingRegular />,
    description: "Explore assurance insights and trends.",
  },
  {
    id: "settings",
    label: "Settings",
    path: "/settings",
    icon: <SettingsRegular />,
    description: "Manage workspace and account settings.",
  },
];
