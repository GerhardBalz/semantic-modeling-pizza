# Semantic Modeling Pizza

A Semantic Knowledge Engineering (SKE) reference example that applies the Semantic Modeling Ontology (SMO) to the Pizza domain while keeping semantic models, implementation projections, runtime data, validation/inference evidence, and operational artifacts distinct.

> **Status:** Working reference example. The repository remains private deliberately while its reference-example baseline and sibling Wine/Food comparison are still being established. Visibility is a governance choice, not a statement about semantic maturity.

## Initiative role

This repository is the **Semantic Modeling Pizza reference example** within the broader SKE initiative.

Related repositories have deliberately different responsibilities:

- [Semantic Knowledge Engineering](https://github.com/GerhardBalz/semantic-knowledge-engineering) owns initiative architecture, cross-repository governance, conventions, sequencing, and the repository map.
- [Semantic Modeling Ontology](https://github.com/GerhardBalz/semantic-modeling-ontology) owns reusable semantic-modeling vocabulary such as `smo:SemanticModel` and `smo:ImplementationProjection`.
- [Pizza Ontology](https://github.com/GerhardBalz/pizza-ontology) preserves and engineers around the historical Pizza Ontology and acts as a broader preservation/reference proving ground.
- [Semantic Modeling Wine/Food](https://github.com/GerhardBalz/semantic-modeling-wine-food) is the sibling semantic-modeling reference example and is currently bootstrap-pending.

`semantic-modeling-pizza` does **not** own the historical Pizza ontology, the `co-ode.org` namespace, SKE initiative governance, or reusable SMO vocabulary. It owns only the repository-authored reference-example artifacts and the evidence produced by applying SMO to this domain.

See [`docs/initiative-role.md`](docs/initiative-role.md) for the detailed ownership and escalation boundaries.

## Purpose

The project keeps the following concerns separate:

1. the external Pizza Ontology and its original identity;
2. a verified cached representation of the canonical ontology;
3. SMO statements describing the ontology as a semantic model;
4. a purpose-specific Pizza Menu Semantic Model;
5. implementation-facing projections where introduced and justified;
6. concrete runtime menu data;
7. SHACL validation and OWL inference evidence;
8. an operational agent contract derived from the semantic model.

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
        ↓ verified by
SHACL + OWL inference + SPARQL lineage evidence
        ↓ operationalized as
find_suitable_pizzas Agent Contract
```

The chain is traceable but the layers are not interchangeable: a semantic model is not runtime data; a projection is not automatically a semantic model; validation or inference evidence is not an implementation projection; and an agent contract is an operational artifact rather than domain semantics.

## Repository structure

```text
.
├── .github/workflows/
│   ├── validate.yml
│   ├── check-pizza-upstream.yml
│   └── refresh-pizza-cache.yml
├── README.md
├── BACKLOG.md
├── CONTRIBUTING.md
├── LICENSE
├── NOTICE.md
├── requirements-dev.txt
├── docs/
│   ├── architecture.md
│   └── initiative-role.md
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

## Architecture and reusable findings

The source-representation boundary, semantic-model scope, runtime-data boundary, inference example, agent contract, SMO gaps, and open questions are maintained in [`docs/architecture.md`](docs/architecture.md).

Reusable findings are not silently promoted into SMO or SKE. This repository records the evidence locally first; cross-example governance findings belong in SKE, while genuinely reusable semantic-modeling vocabulary candidates belong in the SMO backlog. The sibling Wine/Food example is expected to provide the next comparison point before generalizing Pizza-specific experimental terms.

Repository-local follow-up work is maintained in [`BACKLOG.md`](BACKLOG.md).

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the required branch and pull-request workflow.

## License

Original work in this repository is licensed under the MIT License. The external Pizza Ontology remains licensed separately under CC BY 3.0.
