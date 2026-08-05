# Architecture

## 1. Purpose

This repository explores how the Semantic Modeling Ontology (SMO) can describe an established external ontology and connect it to derived semantic models, constraints, and later operational artifacts.

The Pizza Ontology is used because it is small, familiar, and expressive enough to demonstrate classes, object properties, restrictions, value partitions, disjointness, individuals, labels, and inference.

The project is not intended to replace, fork, or improve the Pizza Ontology itself. It uses the ontology as an external semantic foundation and investigates the additional model-management relationships that SMO can express around it.

## 2. Source ontology

The canonical Pizza Ontology is published at:

```text
https://protege.stanford.edu/ontologies/pizza/pizza.owl
```

Its ontology IRI is:

```text
http://www.co-ode.org/ontologies/pizza
```

Its embedded metadata identifies version 2.0 and the Creative Commons Attribution 3.0 license.

The repository references the canonical ontology through [`source/pizza-import.ttl`](../source/pizza-import.ttl) rather than copying or modifying it.

## 3. Core experiment

The first experiment separates four layers:

```text
External ontology
    Protégé Pizza Ontology

Model description
    SMO statements describing the ontology as a model

Derived semantic model
    Pizza Menu Semantic Model as a purpose-specific projection

Validation
    SHACL shapes for the model descriptions
```

Conceptually:

```text
Protégé Pizza Ontology
        ↓ described using
Semantic Modeling Ontology
        ↓ projected as
Pizza Menu Semantic Model
        ↓ constrained by
Pizza model SHACL shapes
        ↓ later operationalized as
APIs / UI / Rules / Agent Contracts
```

The derived semantic model is not asserted to be part of the original Pizza Ontology. It is a repository-specific exploration of how a concrete model may select and organize Pizza semantics for a particular purpose.

## 4. Modeling levels

The Pizza example illustrates the modeling levels used by SMO:

```text
M3 — Semantic modeling foundations
     RDF, RDFS, OWL, SHACL, SKOS, PROV-O

M2 — Semantic Modeling Ontology
     Model, Model Element, Model Kind, Projection,
     Constraint, Mapping, Artifact, Runtime Context

M1 — Concrete models
     Pizza Ontology,
     Pizza Menu Semantic Model

M0 — Runtime entities and facts
     A particular pizza, topping, menu item, or order
```

The Pizza Ontology belongs to M1 because it is a concrete ontology expressed using OWL. Its classes such as `Pizza` and `PizzaTopping` are model elements. Particular runtime pizzas or orders would belong to M0.

## 5. Artifact responsibilities

### `source/pizza-import.ttl`

Provides a small local import document that points to the canonical Pizza Ontology and records its source and license.

It preserves the original ontology identity and avoids silently maintaining a copied source file.

### `models/pizza-model-description.ttl`

Uses SMO to describe the Pizza Ontology as a model, including:

- model kind;
- modeling languages;
- representation;
- source and version information;
- selected model elements relevant to the exploration.

This file describes the ontology. It does not redefine Pizza domain semantics.

### `examples/pizza-menu-semantic-model.ttl`

Declares a purpose-specific semantic model derived from the Pizza Ontology.

The initial example is deliberately small. Its main purpose is to exercise SMO relationships such as `isProjectionOf`, `hasConstraint`, `usesLanguage`, and `hasRepresentation`.

### `shapes/pizza-model-shapes.ttl`

Defines SHACL constraints for the model descriptions in this repository.

The shapes validate metadata and derivation relationships, not all logical axioms of the Pizza Ontology.

## 6. Initial competency questions

The repository should make it possible to answer:

1. What is the external source ontology?
2. What is its ontology IRI and version?
3. Which model kind is assigned to it?
4. Which modeling languages does it use?
5. Which local artifact represents or imports it?
6. Which semantic models are derived from it?
7. Is a derived model a projection, specialization, or realization?
8. Which SHACL constraints apply to each model?
9. Which model elements from the source ontology are relevant to a projection?
10. Can the complete derivation chain be queried without confusing source semantics and repository-specific artifacts?

## 7. Initial model description

The Pizza Ontology is described conceptually as:

```text
Pizza Ontology
    kind: Ontology Model
    languages: RDF, RDFS, OWL, SKOS
    representation: canonical RDF/XML document
    source: Protégé Pizza ontology document
    version: 2.0
```

The first derived model is described as:

```text
Pizza Menu Semantic Model
    kind: Semantic Model
    source: Pizza Ontology
    relationship: projection
    languages: RDF, OWL, SHACL
    purpose: explore menu-oriented Pizza semantics
```

## 8. Validation scope

Initial SHACL validation checks that:

- the Pizza Ontology description has a title, model kind, language, and representation;
- the Pizza Menu Semantic Model identifies the source model it projects;
- the projection declares at least one modeling language;
- the projection identifies its applicable constraint model.

OWL reasoning and ontology consistency are separate concerns. They should eventually be validated with an OWL reasoner rather than conflated with SHACL model-metadata validation.

## 9. Design principles

### Preserve external identity

The canonical Pizza Ontology keeps its original ontology IRI. The repository does not mint a replacement identity for it.

### Describe rather than duplicate

SMO statements describe the ontology and its role in a modeling lifecycle without reproducing its complete OWL metamodel.

### Separate source from projection

The Pizza Ontology and Pizza Menu Semantic Model are distinct models. The latter must retain an explicit derivation link to the former.

### Add concepts through evidence

SMO should be extended only when the Pizza exploration reveals a concrete requirement that the current vocabulary cannot express clearly.

### Keep operationalization provisional

APIs, UI models, recommendation rules, and agent contracts are future artifacts. They should not be introduced until the semantic projection and validation approach is understood.

## 10. Repository structure

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

## 11. Initial milestone

The first milestone is complete when:

1. the canonical Pizza Ontology is referenced with attribution;
2. SMO describes it as an ontology model;
3. one derived Pizza semantic model is declared as a projection;
4. SHACL validates both model descriptions;
5. the repository clearly separates external ontology semantics from its own exploratory models;
6. gaps discovered in SMO are recorded before the vocabulary is expanded.

## 12. Open questions

1. Should an external ontology document be modeled only as a `ModelRepresentation`, or also as a general `Artifact` with provenance?
2. How should the source ontology version be linked to an immutable retrieved representation?
3. Should selected Pizza classes be listed as SMO model elements, or should membership be derived from named-graph or ontology boundaries?
4. What precisely distinguishes the Pizza Menu Semantic Model from a semantic view?
5. Should a purpose-specific projection import the complete Pizza Ontology or copy only selected axioms into a new ontology?
6. Which validations belong in SHACL and which belong in OWL reasoning tests?
7. What operational artifact would provide the clearest next test: menu API, recommendation rules, or an agent contract?
