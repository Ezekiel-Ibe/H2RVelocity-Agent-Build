import { useEffect, useRef, useState } from "react";
import { Routes, Route } from "react-router-dom";
import { SparkleRegular } from "@fluentui/react-icons";
import { Sidebar } from "@/features/navigation/Sidebar";
import { AgentChatPanel } from "@/features/agent-chat/AgentChatPanel";
import type { ChatMessage } from "@/contracts/schemas";
import { initialChatMessages } from "@/fixtures/dashboard";
import { HomePage } from "@/features/home/HomePage";
import { CasesPage } from "@/features/cases/CasesPage";
import { CaseDetailPage } from "@/features/cases/CaseDetailPage";
import { ExceptionsPage } from "@/features/exceptions/ExceptionsPage";
import { ApprovalsPage } from "@/features/approvals/ApprovalsPage";
import { AuditTrailPage } from "@/features/audit/AuditTrailPage";
import { InsightsPage } from "@/features/insights/InsightsPage";
import { SettingsPage } from "@/features/settings/SettingsPage";
import { PlaceholderPage } from "@/features/placeholder/PlaceholderPage";
import { PeriodFilterProvider } from "@/features/common/PeriodFilterContext";
import { navItems } from "./navigation";
import styles from "./App.module.css";

const builtInPaths = new Set(["/", "/cases", "/exceptions", "/approvals", "/audit", "/insights", "/settings"]);

export default function App() {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [agentOpen, setAgentOpen] = useState(true);
  // Chat state lives here so it survives the panel being collapsed/reopened.
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>(initialChatMessages);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [agentWidth, setAgentWidth] = useState<number | null>(() => {
    const saved = Number(localStorage.getItem("pa-agent-width"));
    return Number.isFinite(saved) && saved > 0 ? saved : null;
  });
  const draggingRef = useRef(false);

  // Drag the panel's left edge to resize; double-click resets to the default.
  function startResize(event: React.PointerEvent) {
    event.preventDefault();
    draggingRef.current = true;
    document.body.style.userSelect = "none";
    document.body.style.cursor = "col-resize";

    const onMove = (ev: PointerEvent) => {
      if (!draggingRef.current) return;
      const fromRight = window.innerWidth - ev.clientX;
      const max = Math.min(900, window.innerWidth - 420);
      const width = Math.round(Math.min(Math.max(fromRight, 320), max));
      setAgentWidth(width);
    };
    const onUp = () => {
      draggingRef.current = false;
      document.body.style.userSelect = "";
      document.body.style.cursor = "";
      window.removeEventListener("pointermove", onMove);
      window.removeEventListener("pointerup", onUp);
    };
    window.addEventListener("pointermove", onMove);
    window.addEventListener("pointerup", onUp);
  }

  function resetWidth() {
    setAgentWidth(null);
  }

  useEffect(() => {
    if (agentWidth) localStorage.setItem("pa-agent-width", String(agentWidth));
    else localStorage.removeItem("pa-agent-width");
  }, [agentWidth]);

  // Auto-fit: collapse the sidebar and dock the agent panel as space tightens.
  // Manual toggles still apply between breakpoint crossings.
  useEffect(() => {
    if (typeof window.matchMedia !== "function") return;
    const mqSidebar = window.matchMedia("(max-width: 1080px)");
    const mqAgent = window.matchMedia("(max-width: 1240px)");
    const applySidebar = () => setSidebarCollapsed(mqSidebar.matches);
    const applyAgent = () => setAgentOpen(!mqAgent.matches);
    applySidebar();
    applyAgent();
    mqSidebar.addEventListener("change", applySidebar);
    mqAgent.addEventListener("change", applyAgent);
    return () => {
      mqSidebar.removeEventListener("change", applySidebar);
      mqAgent.removeEventListener("change", applyAgent);
    };
  }, []);

  return (
    <PeriodFilterProvider>
      <div
        className={styles.shell}
        data-sidebar={sidebarCollapsed ? "collapsed" : "expanded"}
        data-agent={agentOpen ? "open" : "closed"}
      >
      <a href="#main-content" className={styles.skipLink}>
        Skip to main content
      </a>
      <Sidebar
        collapsed={sidebarCollapsed}
        onToggle={() => setSidebarCollapsed((v) => !v)}
      />
      <div
        className={styles.body}
        style={
          agentOpen && agentWidth
            ? { gridTemplateColumns: `1fr ${agentWidth}px` }
            : undefined
        }
      >
        <main id="main-content" className={styles.main} tabIndex={-1}>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/cases" element={<CasesPage />} />
            <Route path="/cases/:id" element={<CaseDetailPage />} />
            <Route path="/exceptions" element={<ExceptionsPage />} />
            <Route path="/approvals" element={<ApprovalsPage />} />
            <Route path="/audit" element={<AuditTrailPage />} />
            <Route path="/insights" element={<InsightsPage />} />
            <Route path="/settings" element={<SettingsPage />} />
            {navItems
              .filter((item) => !builtInPaths.has(item.path))
              .map((item) => (
                <Route
                  key={item.id}
                  path={item.path}
                  element={
                    <PlaceholderPage
                      title={item.label}
                      description={item.description}
                      icon={item.icon}
                    />
                  }
                />
              ))}
            <Route
              path="*"
              element={
                <PlaceholderPage
                  title="Page not found"
                  description="The page you requested does not exist."
                  icon={navItems[0].icon}
                />
              }
            />
          </Routes>
        </main>
        {agentOpen ? (
          <AgentChatPanel
            messages={chatMessages}
            setMessages={setChatMessages}
            conversationId={conversationId}
            setConversationId={setConversationId}
            onClose={() => setAgentOpen(false)}
            onResizeStart={startResize}
            onResizeReset={resetWidth}
          />
        ) : (
          <button
            type="button"
            className={styles.openAgent}
            onClick={() => setAgentOpen(true)}
            aria-label="Open agent chat"
          >
            <SparkleRegular />
          </button>
        )}
      </div>
    </div>
    </PeriodFilterProvider>
  );
}
