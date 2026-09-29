import { useQuery } from "@tanstack/react-query";
import { fetchPeriods } from "@/services/periodsService";
import { type PeriodFilterValue } from "@/services/periodFilter";
import styles from "./PeriodFilter.module.css";

type PeriodFilterProps = {
  value: PeriodFilterValue;
  onChange: (value: PeriodFilterValue) => void;
};

const RANGE = "__range__";

function displayDate(iso: string): string {
  const d = new Date(`${iso}T00:00:00`);
  return Number.isNaN(d.getTime())
    ? iso
    : d.toLocaleDateString(undefined, { day: "numeric", month: "short", year: "numeric" });
}

export function PeriodFilter({ value, onChange }: PeriodFilterProps) {
  const { data: periods = [] } = useQuery({
    queryKey: ["periods"],
    queryFn: fetchPeriods,
  });

  const isRange = Boolean(value.from && value.to);
  const selectValue = isRange ? RANGE : value.period ?? "";
  const selected = periods.find((p) => p.id === value.period) ?? null;

  // Calendar bounds from the available periods.
  const bounds = periods.reduce<{ min?: string; max?: string }>((acc, p) => {
    if (!acc.min || p.start < acc.min) acc.min = p.start;
    if (!acc.max || p.end > acc.max) acc.max = p.end;
    return acc;
  }, {});

  function onSelect(next: string) {
    if (next === RANGE) {
      onChange({ period: null, from: bounds.min ?? null, to: bounds.max ?? null });
    } else if (next === "") {
      onChange({ period: null, from: null, to: null });
    } else {
      onChange({ period: next, from: null, to: null });
    }
  }

  return (
    <div className={styles.filter}>
      <label htmlFor="period-filter" className={styles.label}>
        Period
      </label>
      <select
        id="period-filter"
        className={styles.select}
        value={selectValue}
        onChange={(e) => onSelect(e.target.value)}
      >
        <option value="">All periods</option>
        {periods.map((p) => (
          <option key={p.id} value={p.id}>
            {p.name}
          </option>
        ))}
        <option value={RANGE}>Custom range…</option>
      </select>

      {isRange ? (
        <span className={styles.range}>
          <input
            type="date"
            aria-label="Start date"
            className={styles.date}
            value={value.from ?? ""}
            min={bounds.min}
            max={value.to ?? bounds.max}
            onChange={(e) => onChange({ ...value, period: null, from: e.target.value || null })}
          />
          <span aria-hidden="true" className={styles.dash}>
            –
          </span>
          <input
            type="date"
            aria-label="End date"
            className={styles.date}
            value={value.to ?? ""}
            min={value.from ?? bounds.min}
            max={bounds.max}
            onChange={(e) => onChange({ ...value, period: null, to: e.target.value || null })}
          />
        </span>
      ) : (
        <span className={styles.range}>
          {selected
            ? `${displayDate(selected.start)} – ${displayDate(selected.end)}`
            : "All available pay periods"}
        </span>
      )}
    </div>
  );
}
