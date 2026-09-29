/** Period filter value: either a single pay period, a custom date range, or all. */
export type PeriodFilterValue = {
  period: string | null;
  from: string | null;
  to: string | null;
};

export const EMPTY_PERIOD_FILTER: PeriodFilterValue = { period: null, from: null, to: null };

/** Build the `?period=` or `?from=&to=` query string for a filter value. */
export function periodQuery(filter?: PeriodFilterValue | null): string {
  if (!filter) return "";
  const params = new URLSearchParams();
  if (filter.from && filter.to) {
    params.set("from", filter.from);
    params.set("to", filter.to);
  } else if (filter.period) {
    params.set("period", filter.period);
  }
  const query = params.toString();
  return query ? `?${query}` : "";
}
