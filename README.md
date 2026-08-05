# Semantic Modeling Pizza

An exploration of the Protégé Pizza Ontology using the Semantic Modeling Ontology, including semantic models, constraints, projections, and operational artifacts.

> **Status:** Exploratory. This repository tests the Semantic Modeling Ontology against a small, established OWL example.

## Purpose

The project keeps three concerns separate:

1. the external Pizza Ontology and its original identity;
2. Semantic Modeling Ontology statements that describe the ontology as a model;
3. derived semantic models, constraints, and later operational artifacts.

The canonical Pizza Ontology is referenced from its published ontology IRI rather than modified or redefined here.

## Initial model chain

```text
Protégé Pizza Ontology
        ↓ described using
Semantic Modeling Ontology
        ↓ projected as
Pizza Menu Semantic Model
        ↓ constrained by
SHACL shapes
        ↓ later operationalized as
APIs / UI / Rules / Agent Contracts
```

## Repository structure

```text
.
├── README.md
├── CONTRIBUTING.md
├── LICENSE
├── NOTICE.md
├── docs/
│   └── architecture.md
├── source/
│   ├── README.md
│   └── pizza-import.ttl
├── models/
│   └── pizza-model-description.ttl
├── shapes/
│   └── pizza-model-shapes.ttl
└── examples/
    └── pizza-menu-semantic-model.ttl
```

## Source ontology

The project uses the Pizza Ontology from the Protégé tutorial. Its ontology metadata identifies version 2.0 and the Creative Commons Attribution 3.0 license. See [`NOTICE.md`](NOTICE.md) and [`source/README.md`](source/README.md).

## Architecture

The exploration goals, model boundaries, competency questions, and open questions are maintained in [`docs/architecture.md`](docs/architecture.md).

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the required branch and pull-request workflow.

## License

Original work in this repository is licensed under the MIT License. The external Pizza Ontology remains licensed separately under CC BY 3.0.
