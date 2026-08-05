# Architecture

## 1. Purpose

This repository explores how the Semantic Modeling Ontology (SMO) can describe an established external ontology and connect it to a purpose-specific semantic model, runtime data, constraints, inference, queries, and an operational agent contract.

The Pizza Ontology is used because it is small, familiar, and expressive enough to demonstrate classes, object properties, restrictions, value partitions, disjointness, individuals, labels, and inference.

The project does not replace, fork, or improve the Pizza Ontology itself. It uses the ontology as an external semantic foundation and investigates the model-management relationships that SMO can express around it.

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

## 3. Experiment architecture

The experiment separates six layers:

```text
External ontology
    Protégé Pizza Ontology

Model description
    SMO statements describing the ontology as a model

Derived semantic model
    Pizza Menu Semantic Model as a purpose-specific projection

Runtime data
    Concrete menu items, pizza instances, prices, and availability

Operational artifact
    find_suitable_pizzas Agent Contract

Verification
    SHACL validation, OWL inference, and SPARQL lineage queries
```

Conceptually:

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

The derived model, runtime facts, and agent contract are repository-specific artifacts. They are not asserted to be part of the original Pizza Ontology.

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

The Pizza Ontology belongs to M1 because it is a concrete ontology expressed using OWL. Its classes such as `Pizza` and `PizzaTopping` are model elements. The menu items and pizza instances in [`data/example-menu.ttl`](../data/example-menu.ttl) belong to M0.

## 5. Artifact responsibilities

### `source/pizza-import.ttl`

Points to the canonical Pizza Ontology and records its source and license without creating a replacement ontology identity.

### `models/pizza-model-description.ttl`

Uses SMO to describe the external Pizza Ontology as a model, including its kind, languages, representation, source, version, and selected model elements.

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

Executes syntax, SHACL, OWL-inference, and SPARQL-lineage tests.

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

The canonical ontology defines `pizza:SpicyPizza` as any pizza with at least one spicy topping. The test suite loads the canonical ontology, applies OWL RL reasoning, and verifies that this additional type is inferred:

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
- relating a projection to its source model;
- associating constraints;
- relating an operational artifact to its source model;
- applying an artifact in a runtime context.

The Pizza experiment exposes candidate gaps:

1. **Projection scope** — `smo:containsElement` identifies included elements, but SMO has no explicit concept for excluded elements.
2. **Competency questions** — SMO has no dedicated relationship connecting a model to the questions it is intended to answer.
3. **Operational signatures** — SMO does not yet define operation names or semantic input and output concepts for contracts.
4. **Evidence semantics** — recommendation evidence is represented only as a local concept; its provenance and explanation structure remain open.

The repository uses local `smp:` properties for these needs. They remain experimental until a second domain demonstrates that they are reusable.

## 13. Design principles

### Preserve external identity

The canonical Pizza Ontology keeps its original ontology IRI.

### Describe rather than duplicate

SMO statements describe the ontology and its role without reproducing its complete OWL metamodel.

### Separate source, projection, and runtime facts

The external ontology, purpose-specific semantic model, and current menu data are distinct artifacts with different lifecycles.

### Demonstrate before generalizing

Local vocabulary is preferred over changing SMO until a requirement proves reusable across more than one example.

### Keep validation and inference distinct

SHACL constraints and OWL semantics answer different questions and are tested separately.

### Preserve lineage

Operational artifacts must retain machine-readable links to their source semantic models and ontologies.

## 14. Repository structure

```text
.
├── .github/workflows/validate.yml
├── README.md
├── CONTRIBUTING.md
├── LICENSE
├── NOTICE.md
├── requirements-dev.txt
├── docs/architecture.md
├── source/
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
4. at least one OWL inference is demonstrated against the canonical ontology;
5. one agent contract is derived from the semantic model;
6. a SPARQL query traces the complete derivation chain;
7. SMO gaps discovered by the experiment are documented without prematurely changing SMO.

## 16. Open questions

1. Should `answersQuestion` and `excludesElement` become reusable SMO concepts?
2. Is the Pizza Menu Semantic Model better classified as a semantic model, semantic view, or both?
3. Should a purpose-specific projection import the complete source ontology or materialize only selected axioms?
4. How should immutable retrieved source representations be recorded for reproducible inference tests?
5. Should agent inputs and outputs be model elements, contract parameters, or projections of domain concepts?
6. How should recommendation evidence and provenance be modeled?
7. Which next example best challenges the emerging pattern: Wine and Food, FIBO, or another non-food ontology?
