from __future__ import annotations

import json
import unittest
from hashlib import sha256
from pathlib import Path

from owlrl import DeductiveClosure, OWLRL_Semantics
from pyshacl import validate
from rdflib import BNode, Graph, Namespace, RDF, URIRef
from rdflib.namespace import OWL

ROOT = Path(__file__).resolve().parents[1]
SMP = Namespace("https://github.com/GerhardBalz/semantic-modeling-pizza#")
SMO = Namespace("https://w3id.org/smo#")
MOD = Namespace("https://w3id.org/mod#")
PROV = Namespace("http://www.w3.org/ns/prov#")
PIZZA = Namespace("http://www.co-ode.org/ontologies/pizza/pizza.owl#")
PIZZA_ONTOLOGY = URIRef("http://www.co-ode.org/ontologies/pizza")
PIZZA_CACHE = ROOT / "source" / "cache" / "pizza.owl"
PIZZA_MANIFEST = ROOT / "source" / "cache" / "pizza-manifest.json"
OLD_SMO_NAMESPACE = "https://github.com/GerhardBalz/semantic-modeling-ontology#"
OLD_COMPETENCY_RELATION = str(SMP.answersQuestion)


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

    def test_cached_pizza_ontology_matches_manifest(self) -> None:
        content = PIZZA_CACHE.read_bytes()
        manifest = json.loads(PIZZA_MANIFEST.read_text(encoding="utf-8"))

        self.assertEqual(sha256(content).hexdigest(), manifest["sha256"])
        self.assertEqual(len(content), manifest["size_bytes"])

        graph = Graph().parse(data=content, format="xml")
        self.assertIn((PIZZA_ONTOLOGY, RDF.type, OWL.Ontology), graph)

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

    def test_semantic_model_without_source_fails(self) -> None:
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
        self.assertIn("single semantic source", report)

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
        graph = Graph().parse(PIZZA_CACHE, format="xml")
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
        rows = {(row.child, row.relation, row.parent) for row in graph.query(query)}

        self.assertIn(
            (
                SMP.FindSuitablePizzasContract,
                PROV.wasDerivedFrom,
                SMP.PizzaMenuSemanticModel,
            ),
            rows,
        )
        self.assertIn(
            (
                SMP.PizzaMenuSemanticModel,
                PROV.wasDerivedFrom,
                PIZZA_ONTOLOGY,
            ),
            rows,
        )

    def test_competency_questions_use_mod(self) -> None:
        graph = load_graph("examples/pizza-menu-semantic-model.ttl")
        questions = set(graph.objects(SMP.PizzaMenuSemanticModel, MOD.competencyQuestion))
        self.assertEqual(len(questions), 4)
        self.assertNotIn((SMP.PizzaMenuSemanticModel, SMP.answersQuestion, None), graph)

    def test_old_competency_relation_is_absent_from_current_turtle(self) -> None:
        for path in sorted(ROOT.rglob("*.ttl")):
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertNotIn(OLD_COMPETENCY_RELATION, path.read_text(encoding="utf-8"))

    def test_old_smo_namespace_is_absent_from_current_turtle(self) -> None:
        for path in sorted(ROOT.rglob("*.ttl")):
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertNotIn(OLD_SMO_NAMESPACE, path.read_text(encoding="utf-8"))

    def test_only_governed_smo_terms_are_used(self) -> None:
        allowed = {SMO.SemanticModel, SMO.ImplementationProjection}
        graph = Graph()
        for path in sorted(ROOT.rglob("*.ttl")):
            graph.parse(path, format="turtle")
        for triple in graph:
            for term in triple:
                if isinstance(term, URIRef) and str(term).startswith(str(SMO)):
                    self.assertIn(term, allowed)


if __name__ == "__main__":
    unittest.main()
