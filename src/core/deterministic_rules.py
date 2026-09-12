"""
Deterministic Calculation Core Engine for Continuous Payroll Assurance.
Adheres to the KPMG Agent Factory Assurance Principle:
"Every figure, threshold, anomaly, gap, scenario and score is computed by a tested deterministic core - no model call for numbers."
"""
from typing import Dict, List, Any, Optional
from datetime import datetime
from src.config.constants import AnomalyClass, Severity
from src.config.settings import settings

class DeterministicCoreEngine:
    @staticmethod
    def validate_input_completeness(dataset: Dict[str, Any]) -> Dict[str, Any]:
        """
        CP01: Input completeness control (W02).
        Blocks analysis if mandatory worker or pay item fields are missing.
        """
        blocking_errors = []
        warnings = []

        workers = dataset.get("workers", [])
        current_pay = dataset.get("current_pay", [])

        if not workers:
            blocking_errors.append("No worker master records found in snapshot.")
        if not current_pay:
            blocking_errors.append("No current pay records found in snapshot.")

        for w in workers:
            if not w.get("worker_id"):
                blocking_errors.append("Worker record missing worker_id.")
            if not w.get("status"):
                blocking_errors.append(f"Worker {w.get('worker_id', 'UNKNOWN')} missing status.")

        for p in current_pay:
            if not p.get("worker_id"):
                blocking_errors.append(f"PayItem {p.get('pay_item_id', 'UNKNOWN')} missing worker_id.")
            if p.get("gross") is None or p.get("net") is None:
                blocking_errors.append(f"PayItem {p.get('pay_item_id')} missing gross or net pay values.")

        is_valid = len(blocking_errors) == 0
        return {
            "is_valid": is_valid,
            "blocking_errors": blocking_errors,
            "warnings": warnings,
            "total_workers": len(workers),
            "total_pay_items": len(current_pay)
        }

    @staticmethod
    def detect_anomalies(
        workers: List[Dict[str, Any]],
        current_pay: List[Dict[str, Any]],
        prior_pay: List[Dict[str, Any]],
        period_id: str,
        variance_threshold: float = None
    ) -> List[Dict[str, Any]]:
        """
        CP02: 7-Class Deterministic Anomaly Detection (W03).
        """
        if variance_threshold is None:
            variance_threshold = settings.gross_variance_tolerance_pct

        anomalies = []
        worker_map = {w["worker_id"]: w for w in workers}
        prior_pay_map = {p["worker_id"]: p for p in prior_pay}

        # Count pay records per worker for duplicate detection
        worker_pay_counts: Dict[str, List[Dict[str, Any]]] = {}
        for p in current_pay:
            wid = p["worker_id"]
            if wid not in worker_pay_counts:
                worker_pay_counts[wid] = []
            worker_pay_counts[wid].append(p)

        # 1. Leaver Still Paid
        for p in current_pay:
            wid = p["worker_id"]
            w = worker_map.get(wid)
            if w and w.get("status") == "leaver" and p.get("gross", 0) > 0:
                anomalies.append({
                    "anomaly_id": f"ANOM-LSP-{wid}",
                    "worker_id": wid,
                    "anomaly_class": AnomalyClass.LEAVER_STILL_PAID.value,
                    "severity": Severity.HIGH.value,
                    "rule_version": "v2.0_CP02",
                    "gross": p.get("gross"),
                    "net": p.get("net"),
                    "term_date": w.get("term_date"),
                    "details": f"Worker is marked as 'leaver' (term_date={w.get('term_date')}) but has positive gross pay of £{p.get('gross'):.2f}."
                })

        # 2. Joiner Not Paid
        paid_worker_ids = set(p["worker_id"] for p in current_pay)
        for w in workers:
            wid = w["worker_id"]
            hire_date_str = w.get("hire_date")
            if w.get("status") == "active" and wid not in paid_worker_ids:
                anomalies.append({
                    "anomaly_id": f"ANOM-JNP-{wid}",
                    "worker_id": wid,
                    "anomaly_class": AnomalyClass.JOINER_NOT_PAID.value,
                    "severity": Severity.HIGH.value,
                    "rule_version": "v2.0_CP02",
                    "hire_date": hire_date_str,
                    "details": f"Active worker (hire_date={hire_date_str}) has no pay record in current payroll run {period_id}."
                })

        # 3. Unexplained Gross Pay Variance (> threshold and no approved change)
        for p in current_pay:
            wid = p["worker_id"]
            curr_gross = p.get("gross", 0.0)
            prior_p = prior_pay_map.get(wid)
            w = worker_map.get(wid, {})

            if prior_p and prior_p.get("gross", 0) > 0:
                prior_gross = prior_p.get("gross")
                variance_pct = (curr_gross - prior_gross) / prior_gross
                if abs(variance_pct) > variance_threshold and not w.get("has_approved_comp_change", False):
                    anomalies.append({
                        "anomaly_id": f"ANOM-VAR-{wid}",
                        "worker_id": wid,
                        "anomaly_class": AnomalyClass.UNEXPLAINED_VARIANCE.value,
                        "severity": Severity.MEDIUM.value if abs(variance_pct) <= 0.50 else Severity.HIGH.value,
                        "rule_version": "v2.0_CP02",
                        "current_gross": curr_gross,
                        "prior_gross": prior_gross,
                        "variance_pct": round(variance_pct * 100, 2),
                        "details": f"Unexplained gross pay variance of {variance_pct*100:+.2f}% (£{prior_gross:.2f} -> £{curr_gross:.2f}) without approved compensation change."
                    })

        # 4. Missing Tax Code
        for p in current_pay:
            wid = p["worker_id"]
            tax_code = p.get("tax_code")
            if not tax_code or not str(tax_code).strip():
                anomalies.append({
                    "anomaly_id": f"ANOM-TAX-{wid}",
                    "worker_id": wid,
                    "anomaly_class": AnomalyClass.MISSING_TAX_CODE.value,
                    "severity": Severity.HIGH.value,
                    "rule_version": "v2.0_CP02",
                    "gross": p.get("gross"),
                    "details": f"Missing statutory HMRC tax code for worker with gross pay £{p.get('gross', 0):.2f}."
                })

        # 5. Negative Net Pay
        for p in current_pay:
            wid = p["worker_id"]
            net_pay = p.get("net", 0.0)
            if net_pay < 0:
                anomalies.append({
                    "anomaly_id": f"ANOM-NEG-{wid}",
                    "worker_id": wid,
                    "anomaly_class": AnomalyClass.NEGATIVE_NET_PAY.value,
                    "severity": Severity.CRITICAL.value,
                    "rule_version": "v2.0_CP02",
                    "net": net_pay,
                    "gross": p.get("gross"),
                    "deductions": (p.get("tax", 0) + p.get("ni", 0) + p.get("pension", 0) + p.get("other_deductions", 0)),
                    "details": f"Negative net pay calculated: £{net_pay:.2f} (Total deductions exceed gross earnings)."
                })

        # 6. Duplicate Pay Records
        for wid, records in worker_pay_counts.items():
            if len(records) > 1:
                anomalies.append({
                    "anomaly_id": f"ANOM-DUP-{wid}",
                    "worker_id": wid,
                    "anomaly_class": AnomalyClass.DUPLICATE_PAY_RECORD.value,
                    "severity": Severity.CRITICAL.value,
                    "rule_version": "v2.0_CP02",
                    "duplicate_count": len(records),
                    "pay_item_ids": [r.get("pay_item_id") for r in records],
                    "details": f"Duplicate pay items detected: {len(records)} records for worker {wid} in the same pay run."
                })

        # 7. Unapproved Pay Change
        for p in current_pay:
            wid = p["worker_id"]
            changed_fields = p.get("changed_fields")
            approved_by = p.get("approved_by")
            if changed_fields and (approved_by is None or str(approved_by).strip() == ""):
                anomalies.append({
                    "anomaly_id": f"ANOM-UNA-{wid}",
                    "worker_id": wid,
                    "anomaly_class": AnomalyClass.UNAPPROVED_PAY_CHANGE.value,
                    "severity": Severity.HIGH.value,
                    "rule_version": "v2.0_CP02",
                    "changed_fields": changed_fields,
                    "gross": p.get("gross"),
                    "details": f"Unapproved pay changes detected in fields [{changed_fields}] with missing approved_by signature."
                })

        return anomalies

    @staticmethod
    def calculate_period_risk_score(anomalies: List[Dict[str, Any]], total_lines: int) -> Dict[str, Any]:
        """
        CP03: Calculate risk score for the payroll period (W04).
        """
        if total_lines == 0:
            return {"risk_score": 0.0, "risk_band": "LOW", "high_severity_count": 0}

        weights = {
            Severity.CRITICAL.value: 1.0,
            Severity.HIGH.value: 0.75,
            Severity.MEDIUM.value: 0.40,
            Severity.LOW.value: 0.15
        }

        weighted_sum = sum(weights.get(a.get("severity", Severity.MEDIUM.value), 0.5) for a in anomalies)
        # Scaled score bounded [0.0, 1.0]
        raw_score = weighted_sum / max(total_lines, 1)
        # Normalize to risk indicator
        risk_score = min(round(raw_score * 1.5, 4), 1.0)

        if risk_score >= settings.period_risk_high_threshold:
            risk_band = "HIGH"
        elif risk_score >= 0.40:
            risk_band = "MEDIUM"
        else:
            risk_band = "LOW"

        high_sev = sum(1 for a in anomalies if a.get("severity") in (Severity.HIGH.value, Severity.CRITICAL.value))

        return {
            "risk_score": risk_score,
            "risk_percentage": round(risk_score * 100, 2),
            "risk_band": risk_band,
            "total_anomalies": len(anomalies),
            "high_severity_count": high_sev
        }

    @staticmethod
    def explain_pay_math(pay_item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deterministic gross-to-net arithmetic check and breakdown (W06).
        """
        base = pay_item.get("base_pay", 0.0)
        allowances = pay_item.get("allowances", 0.0)
        overtime = pay_item.get("overtime", 0.0)
        computed_gross = round(base + allowances + overtime, 2)

        tax = pay_item.get("tax", 0.0)
        ni = pay_item.get("ni", 0.0)
        pension = pay_item.get("pension", 0.0)
        other_deductions = pay_item.get("other_deductions", 0.0)
        total_deductions = round(tax + ni + pension + other_deductions, 2)

        computed_net = round(computed_gross - total_deductions, 2)
        recorded_net = pay_item.get("net", 0.0)

        arithmetic_match = (abs(computed_net - recorded_net) < 0.01)

        return {
            "worker_id": pay_item.get("worker_id"),
            "base_pay": base,
            "allowances": allowances,
            "overtime": overtime,
            "gross": computed_gross,
            "tax": tax,
            "ni": ni,
            "pension": pension,
            "other_deductions": other_deductions,
            "total_deductions": total_deductions,
            "computed_net": computed_net,
            "recorded_net": recorded_net,
            "arithmetic_match": arithmetic_match,
            "tax_code": pay_item.get("tax_code"),
            "ni_category": pay_item.get("ni_category")
        }

    @staticmethod
    def generate_correction_options(anomaly: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        W09: Generate compliant correction options based on anomaly class.
        """
        anom_class = anomaly.get("anomaly_class")
        options = []

        if anom_class == AnomalyClass.LEAVER_STILL_PAID.value:
            options.append({
                "option_id": "OPT-STOP-PAY",
                "type": "STOP_PAY_AND_RECOVER",
                "description": "Zero gross pay for current period and generate overpayment recovery note.",
                "system_of_record": "Payroll / HCM",
                "target_gross": 0.0,
                "target_net": 0.0,
                "auto_executable": False,
                "requires_approval": True
            })
        elif anom_class == AnomalyClass.JOINER_NOT_PAID.value:
            options.append({
                "option_id": "OPT-OFFCYCLE-PAY",
                "type": "ENROL_FIRST_PAY_OFFCYCLE",
                "description": "Enrol in current run or schedule immediate off-cycle payment based on offer letter.",
                "system_of_record": "HCM -> Payroll Interface",
                "auto_executable": False,
                "requires_approval": True
            })
        elif anom_class == AnomalyClass.UNEXPLAINED_VARIANCE.value:
            options.append({
                "option_id": "OPT-REVERT-PRIOR",
                "type": "REVERT_TO_PRIOR_BASE",
                "description": "Revert gross pay to prior approved period baseline pending HR compensation approval.",
                "system_of_record": "HCM Compensation",
                "auto_executable": False,
                "requires_approval": True
            })
            options.append({
                "option_id": "OPT-CONFIRM-OVERRIDE",
                "type": "CONFIRM_WITH_OVERRIDE_RATIONALE",
                "description": "Accept current pay upon Controller manual sign-off with audit rationale.",
                "system_of_record": "Payroll",
                "auto_executable": False,
                "requires_approval": True
            })
        elif anom_class == AnomalyClass.MISSING_TAX_CODE.value:
            options.append({
                "option_id": "OPT-APPLY-EMERGENCY-TAX",
                "type": "APPLY_EMERGENCY_TAX_CODE",
                "description": "Apply standard HMRC emergency tax code 1257L W1/M1 pending HMRC P6 notification.",
                "system_of_record": "HMRC RTI / Payroll",
                "target_tax_code": "1257L W1",
                "auto_executable": False,
                "requires_approval": True
            })
        elif anom_class == AnomalyClass.NEGATIVE_NET_PAY.value:
            options.append({
                "option_id": "OPT-CAP-VOLUNTARY-DED",
                "type": "CAP_VOLUNTARY_DEDUCTIONS",
                "description": "Cap voluntary deductions to keep net pay at £0.00 and carry forward remaining balance.",
                "system_of_record": "Benefits / Payroll Deductions",
                "auto_executable": True,
                "requires_approval": False
            })
        elif anom_class == AnomalyClass.DUPLICATE_PAY_RECORD.value:
            options.append({
                "option_id": "OPT-REMOVE-DUPLICATE",
                "type": "VOID_DUPLICATE_RECORD",
                "description": "Void secondary duplicate pay item and retain single primary record.",
                "system_of_record": "Payroll",
                "auto_executable": True,
                "requires_approval": False
            })
        elif anom_class == AnomalyClass.UNAPPROVED_PAY_CHANGE.value:
            options.append({
                "option_id": "OPT-HOLD-CHANGES",
                "type": "REVERT_UNAPPROVED_FIELDS",
                "description": "Revert unapproved fields to last authorized state.",
                "system_of_record": "HCM Master",
                "auto_executable": False,
                "requires_approval": True
            })

        return options

    @staticmethod
    def validate_recalculation_outcome(
        original_net: float,
        expected_net: float,
        actual_recalc_net: float
    ) -> Dict[str, Any]:
        """
        CP07: Post-correction validation control (W17).
        """
        delta = abs(actual_recalc_net - expected_net)
        is_valid = (delta < 0.01)

        return {
            "is_valid": is_valid,
            "original_net": original_net,
            "expected_net": expected_net,
            "actual_recalc_net": actual_recalc_net,
            "variance": round(actual_recalc_net - expected_net, 2),
            "status": "PASSED" if is_valid else "FAILED_REWORK_REQUIRED"
        }
