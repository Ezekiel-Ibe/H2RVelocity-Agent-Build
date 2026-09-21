from src.fabric.repository import FabricRepository


def test_fabric_table_catalog_contains_governed_payroll_tables(monkeypatch):
    repository = FabricRepository()
    monkeypatch.setattr(repository.conn_mgr, "get_connection", lambda: None)

    catalog = repository.get_table_catalog()
    table_names = {(table["table_schema"], table["table_name"]) for table in catalog}

    assert ("silver", "worker") in table_names
    assert ("silver", "payroll_line") in table_names
    assert ("gold", "fact_payroll_anomaly") in table_names
    assert ("gold", "fact_audit_evidence") in table_names


def test_agent_data_context_names_warehouse_and_access_boundary(monkeypatch):
    repository = FabricRepository()
    monkeypatch.setattr(repository.conn_mgr, "get_connection", lambda: None)

    context = repository.get_agent_data_context()

    assert "edm_wh_dev" in context
    assert "silver.payroll_line" in context
    assert "governed A03 data-management application path" in context