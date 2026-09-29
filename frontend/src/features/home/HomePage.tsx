import { useQuery } from "@tanstack/react-query";
import { fetchDashboard } from "@/services/dashboardService";
import { PageHeader } from "./PageHeader";
import { WelcomeBanner } from "./WelcomeBanner";
import { QuickActions } from "./QuickActions";
import { StatCards } from "./StatCards";
import { AssuranceOverview } from "./AssuranceOverview";
import { RecentExceptions } from "./RecentExceptions";
import { RecentCases } from "./RecentCases";
import { PeriodFilter } from "@/features/common/PeriodFilter";
import { usePeriodFilter } from "@/features/common/PeriodFilterContext";
import styles from "./HomePage.module.css";

export function HomePage() {
  const { filter: period, setFilter: setPeriod } = usePeriodFilter();
  const { data, isLoading, isError } = useQuery({
    queryKey: ["dashboard", period],
    queryFn: () => fetchDashboard(period),
  });

  return (
    <div className={styles.page}>
      <PageHeader />

      <div className={styles.toolbar}>
        <PeriodFilter value={period} onChange={setPeriod} />
      </div>

      {isLoading && (
        <p role="status" className={styles.status}>
          Loading assurance dashboard…
        </p>
      )}

      {isError && (
        <p role="alert" className={styles.error}>
          We couldn’t load the dashboard. Please try again.
        </p>
      )}

      {data && (
        <>
          <WelcomeBanner />
          <QuickActions />
          <StatCards stats={data.stats} />
          <div className={styles.twoColumn}>
            <AssuranceOverview overview={data.overview} />
            <RecentExceptions exceptions={data.exceptions} />
          </div>
          <RecentCases cases={data.cases} />
        </>
      )}
    </div>
  );
}
