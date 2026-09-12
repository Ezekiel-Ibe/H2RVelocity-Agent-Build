"""
Continuous Payroll Assurance Multi-Agent Execution Pipeline (CLI Entry Point).
Executes the Nine HR Capability Agents in Microsoft AI Foundry & Microsoft Fabric.
"""
import sys
import json
import logging
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from src.orchestration.workflow_runner import workflow_runner
from src.telemetry.agentops_tracer import agentops

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
console = Console()

def main():
    console.print(Panel.fit(
        "[bold cyan]Microsoft AI Foundry & Microsoft Fabric[/bold cyan]\n"
        "[bold green]Continuous Payroll Assurance - 9 Capability Agents[/bold green]\n"
        "Tenant: [yellow]mbsukdemo.com[/yellow] | Sub: [yellow]FO-BSDEV_DYN_AX (853a151d-93f2-492d-aaa3-2058ce27e753)[/yellow]\n"
        "Resource Group: [yellow]bsdevVelocityAI2[/yellow] | Fabric DW: [yellow]edm_wh_dev[/yellow]",
        border_style="cyan"
    ))

    payroll_run_id = "PR-2026-06"
    period_id = "2026-06"

    console.print(f"\n[bold blue]>> Initiating Assurance Lifecycle (W01 - W20) for Payroll Run: {payroll_run_id}...[/bold blue]\n")

    result = workflow_runner.run_full_assurance_cycle(
        payroll_run_id=payroll_run_id,
        period_id=period_id,
        human_approver_identity="controller.jane@mbsukdemo.com",
        human_approver_role="PAYROLL_CONTROLLER"
    )

    if not result["success"]:
        console.print(f"[bold red]Pipeline failed or held open:[/bold red] {result}")
        sys.exit(1)

    # 1. Anomaly Table
    table = Table(title="[bold yellow]CP02 7-Class Anomaly Register[/bold yellow]", border_style="yellow")
    table.add_column("Anomaly ID", style="cyan")
    table.add_column("Worker ID", style="magenta")
    table.add_column("Class", style="bold red")
    table.add_column("Severity", style="red")
    table.add_column("Details", style="white")

    for a in result["anomalies"]:
        table.add_row(
            a["anomaly_id"],
            a["worker_id"],
            a["anomaly_class"],
            a["severity"],
            a["details"]
        )
    console.print(table)

    # 2. Risk & Impact Summary
    risk = result["period_risk"]
    console.print(f"\n[bold green]Period Risk Score:[/bold green] {risk['risk_score']} ({risk['risk_band']} Band) | High Severity Count: {risk['high_severity_count']}")
    console.print(f"[bold green]Audit Manifest SHA-256 Hash (CP08):[/bold green] [cyan]{result['audit_manifest_hash']}[/cyan]")
    console.print(f"[bold green]Period Sign-off (A09):[/bold green] [yellow]{result['period_signoff']['signoff_token']}[/yellow] by {result['period_signoff']['signoff_identity']}")
    console.print(f"[bold green]Case Closure Status (CP10):[/bold green] [bold cyan]{result['case_state']}[/bold cyan]\n")

    # 3. AgentOps Telemetry Summary
    telemetry = agentops.get_fleet_telemetry_summary()
    console.print(Panel(
        f"[bold]AgentOps / EU AI Act & ISO 42001 Fleet Telemetry:[/bold]\n"
        f"Total Executions: {telemetry['fleet_metrics']['total_runs']} | "
        f"Total Tokens: {telemetry['fleet_metrics']['total_tokens']} | "
        f"Fleet Cost: £{telemetry['fleet_metrics']['total_cost_gbp']:.4f} | "
        f"Conformance Status: [bold green]{telemetry['iso_42001_conformance']}[/bold green]",
        border_style="green"
    ))

if __name__ == "__main__":
    main()
