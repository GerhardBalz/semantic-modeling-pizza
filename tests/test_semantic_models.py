from __future__ import annotations

import unittest
from pathlib import Path
from urllib.request import urlopen

from rdflib import BNode, Graph, Namespace, RDF, URIRef
from owlrl import DeductiveClosure, OWLRL_Semantics
from pyshacl import validate

ROOT = Path(__file__).resolve().parents[1]
SMP = Namespace("https://github.com/GerhardBalz/semantic-modeling-pizza#")
SMO = Namespace("https://github.com/GerhardBalz/semantic-modeling-ontology#")
PIZZA = Namespace("http://www.co-ode.org/ontologies/pizza/pizza.owl#")
PIZZA_SOURCE = "https://protege.stanford.edu/ontologies/pizza/pizza.owl"


def load_graph(*relative_paths: str) -> Graph:
    graph = Graph()
    for relative_path in relative_paths:
        graph.parse(ROOT / relative_path, format="turtle")
    return graph


def extract_shape(shapes: Graph, shape: URIRef) -> Graph:
    """Copy one shape and its nested blank-node constraints into a new graph."""
    result = Graph()
    pending = [shape]
    visited: set[URIRef | BNode] = set()

    while pending:
        subject = pending.pop()
        if subject in visited:
            continue
        visited.add(subject)
        for predicate, obj in shapes.predicate_objects(subject):
            result.add((subject, predicate, obj))
            if isinstance(obj, BNode):
                pending.append(obj)

    return result


class SemanticModelTests(unittest.TestCase):
    def test_all_turtle_files_parse(self) -> None:
        for path in sorted(ROOT.rglob("*.ttl")):
            with self.subTest(path=path.relative_to(ROOT)):
                Graph().parse(path, format="turtle")

    def test_model_descriptions_conform(self) -> None:
        data = load_graph(
            "models/pizza-model-description.ttl",
            "examples/pizza-menu-semantic-model.ttl",
            "contracts/find-suitable-pizzas.ttl",
        )
        shapes = load_graph("shapes/pizza-model-shapes.ttl")
        conforms, _, report = validate(
            data_graph=data,
            shacl_graph=shapes,
            inference="none",
            advanced=True,
        )
        self.assertTrue(conforms, report)

    def test_projection_without_source_fails(self) -> None:
        data = load_graph("tests/invalid/pizza-menu-missing-source.ttl")
        all_shapes = load_graph("shapes/pizza-model-shapes.ttl")
        shapes = extract_shape(all_shapes, SMP.PizzaMenuSemanticModelShape)
        conforms, _, report = validate(
            data_graph=data,
            shacl_graph=shapes,
            inference="none",
            advanced=True,
        )
        self.assertFalse(conforms)
        self.assertIn("single source projection", report)

    def test_example_menu_conforms(self) -> None:
        data = load_graph(
            "examples/pizza-menu-semantic-model.ttl",
            "data/example-menu.ttl",
        )
        shapes = load_graph("shapes/pizza-menu-data-shapes.ttl")
        conforms, _, report = validate(
            data_graph=data,
            shacl_graph=shapes,
            inference="none",
            advanced=True,
        )
        self.assertTrue(conforms, report)

    def test_menu_item_without_price_fails(self) -> None:
        data = load_graph(
            "examples/pizza-menu-semantic-model.ttl",
            "tests/invalid/menu-item-missing-price.ttl",
        )
        shapes = load_graph("shapes/pizza-menu-data-shapes.ttl")
        conforms, _, report = validate(
            data_graph=data,
            shacl_graph=shapes,
            inference="none",
            advanced=True,
        )
        self.assertFalse(conforms)
        self.assertIn("decimal price", report)

    def test_owl_infers_spicy_pizza(self) -> None:
        graph = Graph()
        with urlopen(PIZZA_SOURCE, timeout=30) as response:
            graph.parse(data=response.read(), format="xml")
        graph.parse(ROOT / "data/example-menu.ttl", format="turtle")

        DeductiveClosure(OWLRL_Semantics).expand(graph)

        self.assertIn(
            (SMP.DiavolaPizza, RDF.type, PIZZA.SpicyPizza),
            graph,
            "OWL reasoning should classify DiavolaPizza as a SpicyPizza.",
        )

    def test_agent_lineage_query(self) -> None:
        graph = load_graph(
            "models/pizza-model-description.ttl",
            "examples/pizza-menu-semantic-model.ttl",
            "contracts/find-suitable-pizzas.ttl",
        )
        query = (ROOT / "queries/trace-agent-lineage.rq").read_text(encoding="utf-8")
        rows = {
            (row.child, row.relation, row.parent)
            for row in graph.query(query)
        }

        self.assertIn(
            (
                SMP.FindSuitablePizzasContract,
                SMO.isGeneratedFrom,
                SMP.PizzaMenuSemanticModel,
            ),
            rows,
        )
        self.assertIn(
            (
                SMP.PizzaMenuSemanticModel,
                SMO.isProjectionOf,
                URIRef("http://www.co-ode.org/ontologies/pizza"),
            ),
            rows,
        )


if __name__ == "__main__":
    unittest.main()
