# Semantic Modeling Pizza

An exploration of the Protégé Pizza Ontology using the Semantic Modeling Ontology, including semantic models, constraints, projections, runtime data, inference, and operational artifacts.

> **Status:** Exploratory. The current milestone tests whether the initial Semantic Modeling Ontology can support a traceable path from an external OWL ontology to a purpose-specific semantic model and agent contract.

## Purpose

The project keeps the following concerns separate:

1. the external Pizza Ontology and its original identity;
2. Semantic Modeling Ontology statements that describe the ontology as a model;
3. a purpose-specific Pizza Menu Semantic Model;
4. concrete runtime menu data;
5. SHACL validation and OWL inference tests;
6. an operational agent contract derived from the semantic model.

The canonical Pizza Ontology is referenced from its published ontology IRI rather than modified or redefined here.

## Model chain

```text
Protégé Pizza Ontology
        ↓ described using
Semantic Modeling Ontology
        ↓ projected as
Pizza Menu Semantic Model
        ↓ applied to
Example menu data
        ↓ operationalized as
find_suitable_pizzas Agent Contract
```

Cross-cutting validation and traceability are provided by SHACL shapes, OWL reasoning tests, and SPARQL lineage queries.

## Repository structure

```text
.
├── .github/workflows/validate.yml
├── README.md
├── CONTRIBUTING.md
├── LICENSE
├── NOTICE.md
├── requirements-dev.txt
├── docs/
│   └── architecture.md
├── source/
│   ├── README.md
│   └── pizza-import.ttl
├── models/
│   └── pizza-model-description.ttl
├── examples/
│   └── pizza-menu-semantic-model.ttl
├── data/
│   └── example-menu.ttl
├── contracts/
│   └── find-suitable-pizzas.ttl
├── shapes/
│   ├── pizza-model-shapes.ttl
│   └── pizza-menu-data-shapes.ttl
├── queries/
│   └── trace-agent-lineage.rq
└── tests/
    ├── test_semantic_models.py
    └── invalid/
        ├── menu-item-missing-price.ttl
        └── pizza-menu-missing-source.ttl
```

## Source ontology

The project uses the Pizza Ontology from the Protégé tutorial. Its ontology metadata identifies version 2.0 and the Creative Commons Attribution 3.0 license. See [`NOTICE.md`](NOTICE.md) and [`source/README.md`](source/README.md).

## Validation

Install the development dependencies and run the test suite:

```bash
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
```

The tests parse every Turtle artifact, execute positive and negative SHACL cases, demonstrate an OWL inference against the canonical Pizza Ontology, and run the SPARQL lineage query.

## Architecture

The projection scope, runtime-data boundary, inference example, agent contract, SMO gaps, and open questions are maintained in [`docs/architecture.md`](docs/architecture.md).

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the required branch and pull-request workflow.

## License

Original work in this repository is licensed under the MIT License. The external Pizza Ontology remains licensed separately under CC BY 3.0.
