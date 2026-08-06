# Architecture

## 1. Purpose

This repository explores how the Semantic Modeling Ontology (SMO) can describe an established external ontology and connect it to a purpose-specific semantic model, runtime data, constraints, inference, queries, and an operational agent contract.

The Pizza Ontology is used because it is small, familiar, and expressive enough to demonstrate classes, object properties, restrictions, value partitions, disjointness, individuals, labels, and inference.

The project does not replace, fork, or improve the Pizza Ontology itself. It uses the ontology as an external semantic foundation and investigates the model-management relationships that SMO can express around it.

## 2. Source ontology and cached representation

The canonical Pizza Ontology is published at:

```text
https://protege.stanford.edu/ontologies/pizza/pizza.owl
```

Its ontology IRI is:

```text
http://www.co-ode.org/ontologies/pizza
```

Its embedded metadata identifies version 2.0 and the Creative Commons Attribution 3.0 license.

The repository keeps two distinct representations of the same ontology:

```text
Published representation
    https://protege.stanford.edu/ontologies/pizza/pizza.owl

Cached representation
    source/cache/pizza.owl
```

The cached file is a byte-for-byte retrieved representation. It retains the original ontology IRI and version IRI and therefore does not create a replacement or forked ontology.

[`source/cache/pizza-manifest.json`](../source/cache/pizza-manifest.json) records the canonical source URL, retrieval timestamp, SHA-256 hash, byte size, ontology IRI, version information, and license text. The cache can be verified without network access, while a separate scheduled check compares it with the current canonical source.

[`source/pizza-import.ttl`](../source/pizza-import.ttl) continues to import the original ontology IRI. Runtime validation and inference use the local cached representation for reproducibility.

## 3. Experiment architecture

The experiment separates seven layers:

```text
External ontology
    Protégé Pizza Ontology

Cached representation
    Verified local copy of the canonical RDF/XML document

Model description
    SMO statements describing the ontology and its representations

Derived semantic model
    Pizza Menu Semantic Model as a purpose-specific projection

Runtime data
    Concrete menu items, pizza instances, prices, and availability

Operational artifact
    find_suitable_pizzas Agent Contract

Verification
    SHA-256 checks, SHACL validation, OWL inference, and SPARQL lineage queries
```

Conceptually:

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

The cached document is a representation of the external ontology. The derived model, runtime facts, and agent contract are repository-specific artifacts and are not asserted to be part of the original Pizza Ontology.

## 4. Modeling levels

```text
M3 — Semantic modeling foundations
     RDF, RDFS, OWL, SHACL, SKOS, PROV-O

M2 — Semantic Modeling Ontology
     Model, Model Element, Model Kind, Projection,
     Constraint, Mapping, Artifact, Runtime Context

M1 — Concrete models and contracts
     Pizza Ontology,
     Pizza Menu Semantic Model,
     find_suitable_pizzas Agent Contract

M0 — Runtime entities and facts
     Menu Item 4711,
     a particular Margherita pizza,
     its price and current availability
```

The published and cached RDF/XML documents are representations of the M1 Pizza Ontology, not additional domain models. The menu items and pizza instances in [`data/example-menu.ttl`](../data/example-menu.ttl) belong to M0.

## 5. Artifact responsibilities

### `source/pizza-import.ttl`

Imports the canonical Pizza Ontology using its original ontology IRI and records its published source and license.

### `source/cache/pizza.owl`

Contains the exact retrieved RDF/XML bytes used by automated tests and local tooling. It is not edited manually.

### `source/cache/pizza-manifest.json`

Records the cryptographic hash, size, retrieval time, source URL, ontology identity, version, and license metadata for the cached representation.

### `tools/pizza_cache.py`

Provides three operations:

```text
verify          verify local bytes and metadata against the manifest
check-upstream  compare the canonical upstream bytes with the cached hash
refresh         replace the cache and manifest when the upstream bytes change
```

### `.github/workflows/validate.yml`

Verifies the cache without network access and then executes the semantic-model tests.

### `.github/workflows/check-pizza-upstream.yml`

Runs weekly and on demand. It downloads the canonical document and fails when its SHA-256 differs from the cached hash.

### `.github/workflows/refresh-pizza-cache.yml`

Refreshes and commits the cache when run from a feature branch. It explicitly refuses to update `main` directly.

### `models/pizza-model-description.ttl`

Uses SMO to describe the external Pizza Ontology as a model, including its kind, languages, source, version, selected model elements, published representation, cached representation, and cache-manifest artifact.

The cached representation is linked to the published representation with `prov:specializationOf`.

### `examples/pizza-menu-semantic-model.ttl`

Defines the purpose and scope of the Pizza Menu Semantic Model. It identifies selected source concepts, explicitly excluded source concepts, local menu concepts, and the competency questions the model is intended to answer.

### `data/example-menu.ttl`

Contains concrete runtime facts. It deliberately remains separate from ontology classes and semantic-model metadata.

### `contracts/find-suitable-pizzas.ttl`

Describes a read-only agent contract derived from the Pizza Menu Semantic Model. It identifies the operation name, semantic input and output concepts, runtime context, representation, and source model.

### `shapes/*.ttl`

Separates model-metadata constraints from runtime menu-data constraints.

### `queries/trace-agent-lineage.rq`

Traces the direct derivation edges from the agent contract through the semantic model to the source ontology.

### `tests/test_semantic_models.py`

Executes cache, syntax, SHACL, OWL-inference, and SPARQL-lineage tests. The OWL test reads the cached ontology and therefore does not depend on network availability.

## 6. Projection scope

The Pizza Menu Semantic Model is a task-oriented projection rather than a copy of the complete Pizza Ontology.

Its competency questions are:

1. Which pizzas are currently offered on the menu?
2. Which toppings are associated with a pizza?
3. Which offered pizzas satisfy a dietary or spiciness preference?
4. What evidence supports a recommendation?

The projection selects concepts needed for menu representation and recommendation, including:

```text
Pizza
NamedPizza
Margherita
VegetarianPizza
SpicyPizza
PizzaBase
PizzaTopping
SpicyTopping
Spiciness
hasBase
hasTopping
hasSpiciness
```

It explicitly excludes teaching-oriented or out-of-scope concepts such as:

```text
Country
IceCream
```

The local properties `smp:answersQuestion` and `smp:excludesElement` are experimental. They make the projection boundary explicit while testing whether equivalent concepts belong in SMO itself.

## 7. Runtime data boundary

The semantic model defines reusable meaning. Runtime data records what currently exists.

```text
Pizza Ontology class
    pizza:Margherita

Runtime pizza instance
    smp:MargheritaPizza

Runtime menu item
    smp:MenuItem4711

Runtime facts
    title, price, availability
```

The runtime menu data may change without changing the enduring source ontology or the purpose of the semantic model.

## 8. SHACL validation

Two shape graphs are used:

- `pizza-model-shapes.ttl` validates model descriptions, projection metadata, and the agent contract;
- `pizza-menu-data-shapes.ttl` validates concrete menu items.

Positive tests confirm that the current artifacts conform. Negative fixtures demonstrate that:

- a semantic projection without its source model fails;
- a menu item without a price fails.

SHACL validates declared graph structure. It does not replace OWL reasoning or ontology-consistency checking.

## 9. OWL inference

The example menu contains `smp:DiavolaPizza`, asserted as a `pizza:Pizza`, with a topping asserted as a `pizza:SpicyTopping`.

The cached canonical ontology defines `pizza:SpicyPizza` as any pizza with at least one spicy topping. The test suite loads [`source/cache/pizza.owl`](../source/cache/pizza.owl), applies OWL RL reasoning, and verifies that this additional type is inferred:

```text
Asserted:
    DiavolaPizza a Pizza
    DiavolaPizza hasTopping ChilliTopping
    ChilliTopping a SpicyTopping

Inferred:
    DiavolaPizza a SpicyPizza
```

This keeps three concerns distinct:

```text
Assertions       what the data explicitly states
OWL inference    what follows from ontology semantics
SHACL validation whether the graph satisfies expected constraints
```

## 10. Agent contract

The first operational artifact is a read-only contract named:

```text
find_suitable_pizzas
```

It is derived from the Pizza Menu Semantic Model and applies in the restaurant-menu runtime context.

Semantic inputs include:

- dietary preference;
- spiciness;
- required or excluded toppings.

Semantic outputs include:

- matching pizzas;
- recommendation evidence.

The contract describes meaning and lineage. It does not yet prescribe a particular MCP, OpenAPI, or implementation schema.

## 11. Traceability

The lineage query should return these direct edges:

```text
find_suitable_pizzas Agent Contract
    smo:isGeneratedFrom
Pizza Menu Semantic Model

Pizza Menu Semantic Model
    smo:isProjectionOf
Protégé Pizza Ontology
```

This proves that an operational artifact can be traced back to its semantic foundation without treating the artifacts as identical.

## 12. SMO findings

The current SMO vocabulary already supports:

- identifying models and model kinds;
- declaring modeling languages and representations;
- representing both published and cached forms of one model;
- relating a projection to its source model;
- associating constraints;
- relating an operational artifact to its source model;
- applying an artifact in a runtime context.

The Pizza experiment exposes candidate gaps:

1. **Projection scope** — `smo:containsElement` identifies included elements, but SMO has no explicit concept for excluded elements.
2. **Competency questions** — SMO has no dedicated relationship connecting a model to the questions it is intended to answer.
3. **Operational signatures** — SMO does not yet define operation names or semantic input and output concepts for contracts.
4. **Evidence semantics** — recommendation evidence is represented only as a local concept; its provenance and explanation structure remain open.
5. **Representation integrity** — the checksum remains in an external JSON manifest; the appropriate reusable RDF representation of cryptographic integrity remains open.

The repository uses local `smp:` properties for domain-specific needs and a JSON manifest for cache integrity. These choices remain experimental until a second domain demonstrates what should be generalized.

## 13. Design principles

### Preserve external identity

The canonical Pizza Ontology keeps its original ontology IRI and version IRI in both published and cached representations.

### Cache without forking

Caching records exact source bytes for reproducibility. It does not authorize semantic edits or mint a replacement ontology identity.

### Verify locally, compare remotely

Normal validation verifies the checked-in bytes against the manifest without network access. A separate scheduled workflow performs the unstable network comparison with the canonical source.

### Separate source, projection, and runtime facts

The external ontology, its representations, the purpose-specific semantic model, and current menu data are distinct artifacts with different lifecycles.

### Demonstrate before generalizing

Local vocabulary is preferred over changing SMO until a requirement proves reusable across more than one example.

### Keep validation and inference distinct

SHACL constraints and OWL semantics answer different questions and are tested separately.

### Preserve lineage

Operational artifacts must retain machine-readable links to their source semantic models and ontologies.

## 14. Repository structure

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
├── docs/architecture.md
├── source/
│   ├── pizza-import.ttl
│   └── cache/
│       ├── pizza.owl
│       └── pizza-manifest.json
├── tools/pizza_cache.py
├── models/
├── examples/
├── data/
├── contracts/
├── shapes/
├── queries/
└── tests/
```

## 15. Milestone v0.2

The milestone is complete when:

1. the projection states its purpose, included concepts, excluded concepts, and competency questions;
2. concrete menu data is separate from model definitions;
3. valid and invalid SHACL examples are executable;
4. at least one OWL inference is demonstrated against the verified cached ontology;
5. one agent contract is derived from the semantic model;
6. a SPARQL query traces the complete derivation chain;
7. a cached source representation is protected by a cryptographic manifest and upstream-change check;
8. SMO gaps discovered by the experiment are documented without prematurely changing SMO.

## 16. Open questions

1. Should `answersQuestion` and `excludesElement` become reusable SMO concepts?
2. Is the Pizza Menu Semantic Model better classified as a semantic model, semantic view, or both?
3. Should a purpose-specific projection import the complete source ontology or materialize only selected axioms?
4. Should cryptographic integrity be represented using SPDX, another existing RDF vocabulary, or remain an artifact-level manifest concern?
5. Should cached representations use `prov:specializationOf`, `prov:alternateOf`, or a more precise SMO relationship?
6. Should agent inputs and outputs be model elements, contract parameters, or projections of domain concepts?
7. How should recommendation evidence and provenance be modeled?
8. Which next example best challenges the emerging pattern: Wine and Food, FIBO, or another non-food ontology?
