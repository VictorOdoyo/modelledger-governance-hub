from modelledger.services.lineage import build_lineage_graph


def test_lineage_graph_links_dataset_run_and_version():
    graph = build_lineage_graph("Claims Triage", "claims-q3", "run-123", "version-456")
    assert [edge["relation"] for edge in graph["edges"]] == ["trained", "registered"]
    assert {node["kind"] for node in graph["nodes"]} == {"dataset", "experiment_run", "model_version"}
