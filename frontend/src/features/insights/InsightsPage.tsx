import { useQuery } from "@tanstack/react-query";
import { fetchInsights } from "@/services/insightsService";
import { LoadingState, ErrorState } from "@/features/common/QueryStates";
import { PeriodFilter } from "@/features/common/PeriodFilter";
import { usePeriodFilter } from "@/features/common/PeriodFilterContext";
import type { Insights } from "@/contracts/schemas";
import styles from "./InsightsPage.module.css";

const dotColor: Record<string, string> = {
  high: "var(--pa-viz-high)",
  medium: "var(--pa-viz-medium)",
  low: "var(--pa-viz-low)",
};

function riskLevel(risk: number): "high" | "medium" | "low" {
  if (risk >= 80) return "high";
  if (risk >= 50) return "medium";
  return "low";
}

export function InsightsPage() {
  const { filter: period, setFilter: setPeriod } = usePeriodFilter();
  const { data, isLoading, isError } = useQuery({
    queryKey: ["insights", period],
    queryFn: () => fetchInsights(period),
  });

  return (
    <div className={styles.page}>
      <header className={styles.header}>
        <h1 className={styles.title}>Assurance Insights</h1>
        <p className={styles.subtitle}>
          Trends and analytics across the payroll assurance lifecycle — case
          resolution, anomaly distribution, risk concentration and governance
          control activity — aggregated from the live assurance data.
        </p>
      </header>

      <div className={styles.toolbar}>
        <PeriodFilter value={period} onChange={setPeriod} />
      </div>

      {isLoading && <LoadingState label="Loading insights…" />}
      {isError && <ErrorState message="We couldn’t load insights. Please try again." />}

      {data && <InsightsContent data={data} />}
    </div>
  );
}

function InsightsContent({ data }: { data: Insights }) {
  const funnelMax = Math.max(1, ...data.funnel.map((f) => f.count));
  const typeMax = Math.max(1, ...data.anomalyTypes.map((t) => t.count));
  const controlMax = Math.max(1, ...data.controlActivity.map((c) => c.count));

  return (
    <>
      <section className={styles.statRow} aria-label="Key figures">
        <Stat value={`${data.assuranceScore}%`} label="Assurance Score" accent />
        <Stat value={data.summary.totalCases} label="Total Cases" />
        <Stat value={data.summary.openCases} label="Open Cases" />
        <Stat value={data.summary.resolvedCases} label="Resolved / Closed" />
        <Stat value={data.summary.totalAnomalies} label="Anomalies" />
        <Stat value={data.summary.evidencePacks} label="Evidence Packs" />
      </section>

      <div className={styles.grid}>
        <section className={styles.card} aria-label="Case resolution funnel">
          <h2 className={styles.cardTitle}>Case Resolution Funnel</h2>
          <div className={styles.bars}>
            {data.funnel.map((f) => (
              <div key={f.stage} className={styles.barRow}>
                <span className={styles.barLabel}>{f.stage}</span>
                <span className={styles.barTrack}>
                  <span
                    className={styles.barFill}
                    style={{ width: `${(f.count / funnelMax) * 100}%` }}
                  />
                </span>
                <span className={styles.barCount}>{f.count}</span>
              </div>
            ))}
          </div>
        </section>

        <section className={styles.card} aria-label="Anomaly severity mix">
          <h2 className={styles.cardTitle}>Anomaly Severity Mix</h2>
          <table className={styles.legend}>
            <tbody>
              {data.severityMix.map((row) => (
                <tr key={row.level}>
                  <th scope="row" className={styles.legendLabel}>
                    <span
                      className={styles.dot}
                      style={{ background: dotColor[row.level] }}
                      aria-hidden="true"
                    />
                    {row.label}
                  </th>
                  <td className={styles.legendCount}>{row.count}</td>
                  <td className={styles.legendPct}>{row.percentage}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>

        <section className={styles.cardWide} aria-label="Anomalies by type">
          <h2 className={styles.cardTitle}>Anomalies by Type</h2>
          <div className={styles.bars}>
            {data.anomalyTypes.map((t) => (
              <div key={t.type} className={styles.barRow}>
                <span className={styles.barLabel} title={t.type}>
                  {t.type}
                </span>
                <span className={styles.barTrack}>
                  <span
                    className={styles.barFill}
                    data-risk={riskLevel(t.maxRisk)}
                    style={{ width: `${(t.count / typeMax) * 100}%` }}
                  />
                </span>
                <span className={styles.barCount}>
                  {t.count}
                  <span className={styles.barSub}>risk {t.maxRisk}</span>
                </span>
              </div>
            ))}
          </div>
        </section>

        <section className={styles.cardWide} aria-label="Top risk cases">
          <h2 className={styles.cardTitle}>Top Risk Cases</h2>
          <table className={styles.table}>
            <thead>
              <tr>
                <th>Case</th>
                <th>Worker</th>
                <th>Anomaly</th>
                <th>Status</th>
                <th className={styles.num}>Risk</th>
              </tr>
            </thead>
            <tbody>
              {data.topRiskCases.map((c) => (
                <tr key={c.id}>
                  <td className={styles.mono}>{c.id}</td>
                  <td>{c.workerName}</td>
                  <td>{c.anomalyTitle}</td>
                  <td>{c.status}</td>
                  <td className={styles.num}>
                    <span className={styles.riskTag} data-risk={c.severity}>
                      {c.riskScore}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>

        <section className={styles.card} aria-label="Governance control activity">
          <h2 className={styles.cardTitle}>Control Activity</h2>
          <div className={styles.bars}>
            {data.controlActivity.map((c) => (
              <div key={c.control} className={styles.barRow}>
                <span className={styles.barLabel} title={c.control}>
                  {c.control}
                </span>
                <span className={styles.barTrack}>
                  <span
                    className={styles.barFill}
                    style={{ width: `${(c.count / controlMax) * 100}%` }}
                  />
                </span>
                <span className={styles.barCount}>{c.count}</span>
              </div>
            ))}
          </div>
        </section>
      </div>
    </>
  );
}

function Stat({
  value,
  label,
  accent,
}: {
  value: string | number;
  label: string;
  accent?: boolean;
}) {
  return (
    <div className={styles.stat} data-accent={accent ? "true" : undefined}>
      <span className={styles.statValue}>{value}</span>
      <span className={styles.statLabel}>{label}</span>
    </div>
  );
}
