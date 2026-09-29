import { NavLink } from "react-router-dom";
import {
  ChevronDownRegular,
  PanelLeftContractRegular,
  PanelLeftExpandRegular,
} from "@fluentui/react-icons";
import { KpmgLogo } from "@/design-system/KpmgLogo";
import { navItems } from "@/app/navigation";
import styles from "./Sidebar.module.css";

type SidebarProps = {
  collapsed: boolean;
  onToggle: () => void;
};

export function Sidebar({ collapsed, onToggle }: SidebarProps) {
  return (
    <nav
      className={styles.sidebar}
      data-collapsed={collapsed}
      aria-label="Primary"
    >
      <div className={styles.brand}>
        {!collapsed && <KpmgLogo variant="white" height={96} />}
        <button
          type="button"
          className={styles.toggle}
          onClick={onToggle}
          aria-label={collapsed ? "Expand navigation" : "Collapse navigation"}
          aria-expanded={!collapsed}
        >
          {collapsed ? <PanelLeftExpandRegular /> : <PanelLeftContractRegular />}
        </button>
      </div>

      <ul className={styles.navList}>
        {navItems.map((item) => (
          <li key={item.id}>
            <NavLink
              to={item.path}
              end={item.path === "/"}
              title={collapsed ? item.label : undefined}
              className={({ isActive }) =>
                isActive ? `${styles.navItem} ${styles.navItemActive}` : styles.navItem
              }
            >
              <span className={styles.navIcon} aria-hidden="true">
                {item.icon}
              </span>
              <span className={styles.navLabel}>{item.label}</span>
              {item.expandable && (
                <ChevronDownRegular className={styles.chevron} aria-hidden="true" />
              )}
            </NavLink>
          </li>
        ))}
      </ul>

      <div className={styles.footer}>
        <div className={styles.user}>
          <span className={styles.avatar} aria-hidden="true">
            KB
          </span>
          <span className={styles.userInfo}>
            <span className={styles.userName}>KPMG User</span>
            <span className={styles.userEmail}>kpmg.user@kpmg.com</span>
          </span>
        </div>
        <p className={styles.copyright}>© 2026 KPMG. All rights reserved.</p>
        <p className={styles.legal}>
          <a href="#privacy">Privacy</a>
          <span aria-hidden="true"> | </span>
          <a href="#legal">Legal</a>
        </p>
      </div>
    </nav>
  );
}
