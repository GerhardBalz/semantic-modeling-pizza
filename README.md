# Semantic Modeling Pizza

An exploration of the Protégé Pizza Ontology using the Semantic Modeling Ontology, including semantic models, constraints, projections, runtime data, inference, and operational artifacts.

> **Status:** Exploratory. The current milestone tests whether the initial Semantic Modeling Ontology can support a traceable path from an external OWL ontology to a purpose-specific semantic model and agent contract.

## Purpose

The project keeps the following concerns separate:

1. the external Pizza Ontology and its original identity;
2. a verified cached representation of the canonical ontology;
3. Semantic Modeling Ontology statements that describe the ontology as a model;
4. a purpose-specific Pizza Menu Semantic Model;
5. concrete runtime menu data;
6. SHACL validation and OWL inference tests;
7. an operational agent contract derived from the semantic model.

The canonical Pizza Ontology retains its published ontology IRI. The repository cache is a byte-for-byte retrieved representation used for reproducible, offline validation and inference—not a fork or replacement ontology.

## Model chain

```text
Protégé Pizza Ontology
        ↓ cached and verified as
Local canonical representation
        ↓ described using
Semantic Modeling Ontology
        ↓ projected as
Pizza Menu Semantic Model
        ↓ applied to
Example menu data
        ↓ operationalized as
find_suitable_pizzas Agent Contract
```

Cross-cutting validation and traceability are provided by SHA-256 verification, SHACL shapes, OWL reasoning tests, and SPARQL lineage queries.

## Repository structure

```text
.
├── .github/workflows/
│   ├── validate.yml
│   ├── check-pizza-upstream.yml
│   └── refresh-pizza-cache.yml
├── README.md
├── CONTRIBUTING.md
├── LICENSE
├── NOTICE.md
├── requirements-dev.txt
├── docs/
│   └── architecture.md
├── source/
│   ├── README.md
│   ├── pizza-import.ttl
│   └── cache/
│       ├── pizza.owl
│       └── pizza-manifest.json
├── tools/
│   └── pizza_cache.py
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

## Source ontology cache

The project uses the Pizza Ontology from the Protégé tutorial. Its ontology metadata identifies version 2.0 and the Creative Commons Attribution 3.0 license.

The cached representation and JSON manifest are maintained under [`source/cache`](source/cache). The manifest records the source URL, retrieval timestamp, SHA-256, byte size, ontology IRI, version, and license metadata.

Verify the local cache without accessing the network:

```bash
python tools/pizza_cache.py verify
```

Check whether the canonical source has changed:

```bash
python tools/pizza_cache.py check-upstream
```

Refresh the cache on a feature branch:

```bash
python tools/pizza_cache.py refresh
```

See [`NOTICE.md`](NOTICE.md) and [`source/README.md`](source/README.md) for source attribution and maintenance details.

## Validation

Install the development dependencies and run the test suite:

```bash
python -m pip install -r requirements-dev.txt
python tools/pizza_cache.py verify
python -m unittest discover -s tests -v
```

The tests parse every Turtle artifact, verify the cached ontology and manifest, execute positive and negative SHACL cases, demonstrate an OWL inference using the local cache, and run the SPARQL lineage query.

## Architecture

The source-representation boundary, projection scope, runtime-data boundary, inference example, agent contract, SMO gaps, and open questions are maintained in [`docs/architecture.md`](docs/architecture.md).

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the required branch and pull-request workflow.

## License

Original work in this repository is licensed under the MIT License. The external Pizza Ontology remains licensed separately under CC BY 3.0.
