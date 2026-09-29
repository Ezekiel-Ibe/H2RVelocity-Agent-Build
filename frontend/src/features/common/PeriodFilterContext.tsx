import { createContext, useContext, useEffect, useState, type ReactNode } from "react";
import { EMPTY_PERIOD_FILTER, type PeriodFilterValue } from "@/services/periodFilter";

type PeriodFilterContextValue = {
  filter: PeriodFilterValue;
  setFilter: (filter: PeriodFilterValue) => void;
};

const PeriodFilterContext = createContext<PeriodFilterContextValue | null>(null);
const STORAGE_KEY = "pa-period-filter";

function loadFilter(): PeriodFilterValue {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) {
      const parsed = JSON.parse(raw) as Partial<PeriodFilterValue>;
      return {
        period: parsed.period ?? null,
        from: parsed.from ?? null,
        to: parsed.to ?? null,
      };
    }
  } catch {
    // ignore malformed storage
  }
  return EMPTY_PERIOD_FILTER;
}

export function PeriodFilterProvider({ children }: { children: ReactNode }) {
  const [filter, setFilter] = useState<PeriodFilterValue>(loadFilter);

  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(filter));
    } catch {
      // ignore storage failures
    }
  }, [filter]);

  return (
    <PeriodFilterContext.Provider value={{ filter, setFilter }}>
      {children}
    </PeriodFilterContext.Provider>
  );
}

export function usePeriodFilter(): PeriodFilterContextValue {
  const ctx = useContext(PeriodFilterContext);
  if (!ctx) {
    throw new Error("usePeriodFilter must be used within a PeriodFilterProvider");
  }
  return ctx;
}
