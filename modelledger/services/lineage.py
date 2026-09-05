from dataclasses import dataclass


@dataclass(frozen=True)
class LineageNode:
    id: str
    kind: str
    label: str


@dataclass(frozen=True)
class LineageEdge:
    source: str
    target: str
    relation: str


def build_lineage_graph(model_name: str, dataset: str, run_id: str, version_id: str) -> dict[str, list[dict[str, str]]]:
    nodes = [
        LineageNode(f"dataset:{dataset}", "dataset", dataset),
        LineageNode(f"run:{run_id}", "experiment_run", run_id),
        LineageNode(f"version:{version_id}", "model_version", model_name),
    ]
    edges = [
        LineageEdge(nodes[0].id, nodes[1].id, "trained"),
        LineageEdge(nodes[1].id, nodes[2].id, "registered"),
    ]
    return {
        "nodes": [node.__dict__ for node in nodes],
        "edges": [edge.__dict__ for edge in edges],
    }
