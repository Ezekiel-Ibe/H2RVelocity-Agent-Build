import { useParams, Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { fetchCaseDetail } from "@/services/casesService";
import { LoadingState, ErrorState } from "@/features/common/QueryStates";
import { DecisionPanel } from "./DecisionPanel";
import styles from "./CaseDetailPage.module.css";

const controlTone: Record<string, string> = {
  Pass: "pass",
  Fail: "fail",
  Pending: "pending",
  "N/A": "na",
};

export function CaseDetailPage() {
  const { id = "" } = useParams();
  const { data, isLoading, isError } = useQuery({
    queryKey: ["case", id],
    queryFn: () => fetchCaseDetail(id),
  });

  return (
    <div className={styles.page}>
      <nav className={styles.breadcrumb} aria-label="Breadcrumb">
        <Link to="/cases">← Cases</Link>
      </nav>

      {isLoading && <LoadingState label="Loading case…" />}
      {isError && <ErrorState message="We couldn’t load this case. Please try again." />}

      {data && (
        <>
          <header className={styles.header}>
            <div>
              <h1 className={styles.title}>{data.id}</h1>
              <p className={styles.subtitle}>
                {data.workerName} · {data.workerRef} · {data.payPeriod} ·{" "}
                {data.payrollRunId}
              </p>
            </div>
            <div className={styles.headerMeta}>
              <span className={styles.anomaly} data-severity={data.severity}>
                {data.anomalyTitle}
              </span>
              <span className={styles.risk}>Risk {data.riskScore}</span>
              <span className={styles.step}>{data.currentStep}</span>
            </div>
          </header>

          <div className={styles.layout}>
            <div className={styles.main}>
              <section className={styles.card} aria-label="Anomaly">
                <h2 className={styles.h2}>Anomaly & root cause</h2>
                <p className={styles.text}>{data.anomalyDescription}</p>
                <p className={styles.meta}>
                  Rule {data.ruleId} ({data.ruleVersion})
                </p>
                <p className={styles.text}>
                  <strong>Root cause:</strong> {data.rootCause}
                </p>
              </section>

              <section className={styles.card} aria-label="Risk factors">
                <h2 className={styles.h2}>Risk factors (CP03)</h2>
                <table className={styles.table}>
                  <thead>
                    <tr>
                      <th scope="col">Factor</th>
                      <th scope="col">Weight</th>
                      <th scope="col">Contribution</th>
                      <th scope="col">Note</th>
                    </tr>
                  </thead>
                  <tbody>
                    {data.riskFactors.map((f) => (
                      <tr key={f.name}>
                        <td>{f.name}</td>
                        <td>{Math.round(f.weight * 100)}%</td>
                        <td className={styles.num}>{f.contribution}</td>
                        <td className={styles.mutedCell}>{f.note}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </section>

              <section className={styles.card} aria-label="Recommendation">
                <h2 className={styles.h2}>Recommendation (advisory)</h2>
                <p className={styles.text}>
                  <strong>{data.recommendation.summary}</strong>
                </p>
                <p className={styles.text}>{data.recommendation.rationale}</p>
                <p className={styles.meta}>
                  Confidence: {data.recommendation.confidence} · Evidence:{" "}
                  {data.recommendation.citations.join(", ")}
                </p>
                <ul className={styles.options}>
                  {data.correctionOptions.map((o) => (
                    <li key={o.id} className={styles.option} data-recommended={o.recommended}>
                      <span className={styles.optionLabel}>
                        {o.label}
                        {o.recommended && <span className={styles.tag}>Recommended</span>}
                      </span>
                      <span className={styles.optionDesc}>{o.description}</span>
                    </li>
                  ))}
                </ul>
              </section>

              <section className={styles.card} aria-label="Impact">
                <h2 className={styles.h2}>Impact assessment (CP04)</h2>
                <dl className={styles.impact}>
                  {data.impact.map((line) => (
                    <div key={line.label} className={styles.impactRow}>
                      <dt>{line.label}</dt>
                      <dd>{line.value}</dd>
                    </div>
                  ))}
                </dl>
              </section>

              <section className={styles.card} aria-label="Control results">
                <h2 className={styles.h2}>Control results (CP01–CP10)</h2>
                <table className={styles.table}>
                  <thead>
                    <tr>
                      <th scope="col">Control</th>
                      <th scope="col">Owner</th>
                      <th scope="col">Result</th>
                      <th scope="col">Detail</th>
                    </tr>
                  </thead>
                  <tbody>
                    {data.controls.map((c) => (
                      <tr key={c.id}>
                        <td className={styles.controlId}>
                          {c.id} {c.name}
                        </td>
                        <td>{c.owner}</td>
                        <td>
                          <span className={styles.control} data-tone={controlTone[c.result]}>
                            {c.result}
                          </span>
                        </td>
                        <td className={styles.mutedCell}>{c.detail}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </section>

              <section className={styles.card} aria-label="Evidence">
                <h2 className={styles.h2}>Evidence (CP08)</h2>
                <table className={styles.table}>
                  <thead>
                    <tr>
                      <th scope="col">ID</th>
                      <th scope="col">Item</th>
                      <th scope="col">Source</th>
                      <th scope="col">Hash</th>
                      <th scope="col">Captured</th>
                    </tr>
                  </thead>
                  <tbody>
                    {data.evidence.map((e) => (
                      <tr key={e.id}>
                        <td className={styles.controlId}>{e.id}</td>
                        <td>{e.label}</td>
                        <td>{e.source}</td>
                        <td className={styles.hash}>{e.hash}</td>
                        <td>{e.capturedOn}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </section>
            </div>

            <aside className={styles.side}>
              <DecisionPanel
                caseId={data.id}
                allowedActions={data.allowedActions}
                decision={data.decision}
              />
            </aside>
          </div>
        </>
      )}
    </div>
  );
}
