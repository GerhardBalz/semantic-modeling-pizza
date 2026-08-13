# Architecture

## 1. Purpose

This repository demonstrates how governed semantic-modeling concepts can connect an established external ontology to a purpose-specific semantic model, runtime data, validation/inference evidence, queries, and an operational contract without collapsing those artifact boundaries.

The Pizza Ontology is used because it is small and expressive enough to demonstrate classes, properties, restrictions, value partitions, disjointness, individuals, labels, and inference.

The project does **not** replace, fork, or modernize the Pizza Ontology. Historical Pizza ontology/version/entity identity remains external.

## 2. Source ontology and reproducible representation

Canonical published document:

```text
https://protege.stanford.edu/ontologies/pizza/pizza.owl
```

Historical ontology IRI:

```text
http://www.co-ode.org/ontologies/pizza
```

Historical version IRI:

```text
http://www.co-ode.org/ontologies/pizza/2.0.0
```

The repository also keeps a byte-for-byte cached RDF/XML representation under `source/cache/pizza.owl` for deterministic local validation and inference. The cache retains the historical ontology/version identity and therefore does not become a replacement ontology.

`source/cache/pizza-manifest.json` records source URL, retrieval time, SHA-256, byte size, ontology identity, version, and license metadata. Local validation verifies the checked-in bytes; a separate workflow compares the cache with the current upstream bytes.

## 3. Current artifact architecture

```text
External semantic model
    historical Pizza Ontology
            ↓ represented by
Published RDF/XML + verified local cache
            ↓ described as
smo:SemanticModel
            ↓ source of
Pizza Menu Semantic Model
    a smo:SemanticModel
            ↓ used with
Concrete runtime menu data
            ↓ verified by
SHACL + OWL inference
            ↓ connected through
SPARQL provenance/lineage
            ↓ operationalized by
find_suitable_pizzas Agent Contract
```

The chain is traceable but the layers are not interchangeable:

- a representation/cache is not a new semantic authority;
- a purpose-specific semantic model is not runtime data;
- derivation does not automatically imply `smo:ImplementationProjection`;
- SHACL/OWL results are verification evidence, not domain semantics;
- the agent contract is operational and remains repository-local.

## 4. Vocabulary boundary

### Governed SMO

The current repository uses governed SMO v0.1 only where its published meaning applies:

```text
smo:SemanticModel
smo:ImplementationProjection
```

No current artifact is typed as `smo:ImplementationProjection` merely because it is derived from another model.

### Established vocabularies

DCTERMS and PROV-O express source, derivation, conformance, representation/format, and part relationships where sufficient.

Following SMO #22 / PR #23 and the Pizza ↔ Wine/Food evidence cycle, textual competency questions use:

```text
mod:competencyQuestion
```

No `smo:answersQuestion` relation was added.

### Local vocabulary

Repository-local `smp:` vocabulary remains appropriate for Pizza-specific or execution-adjacent distinctions not justified as reusable SMO terms. The explicit exclusion relation remains local because the Wine/Food sibling did not independently require it.

## 5. Artifact responsibilities

### `models/pizza-model-description.ttl`

Describes the historical Pizza ontology as an `smo:SemanticModel`, preserving external identity and linking to source/format/provenance metadata through established vocabularies.

### `examples/pizza-menu-semantic-model.ttl`

Defines the purpose-specific Pizza Menu `smo:SemanticModel`. It records:

- source lineage to the historical Pizza ontology;
- selected concepts needed by the menu/recommendation use case;
- explicit Pizza-local exclusions;
- textual competency questions via `mod:competencyQuestion`;
- local menu concepts.

It is a derived semantic model. It is **not** classified as `smo:ImplementationProjection` in the current evidence baseline.

### `data/example-menu.ttl`

Contains concrete runtime facts such as menu items, prices, availability, and pizza instances. Runtime data can change independently from the enduring semantic models.

### `contracts/find-suitable-pizzas.ttl`

Defines a repository-local read-only operational contract. It uses local vocabulary for operation name, semantic inputs/outputs, and runtime context, while preserving lineage through PROV-O.

### `shapes/*.ttl`

Separates semantic-model metadata constraints from runtime menu-data constraints.

### `queries/trace-agent-lineage.rq`

Traces `prov:wasDerivedFrom` edges from the operational contract through the Pizza Menu Semantic Model to the historical Pizza ontology.

### `tests/test_semantic_models.py`

Verifies syntax, cache integrity, SHACL positive/negative cases, OWL inference, SPARQL lineage, governed SMO usage, and the MOD competency-question boundary.

## 6. Purpose-specific semantic-model scope

The Pizza Menu Semantic Model answers these competency questions:

1. Which pizzas are currently offered on the menu?
2. Which toppings are associated with a pizza?
3. Which offered pizzas satisfy a dietary or spiciness preference?
4. What evidence supports a recommendation?

They are represented as text through `mod:competencyQuestion`.

The model selects concepts needed for the use case, including Pizza, NamedPizza, PizzaBase, PizzaTopping, Spiciness, and the relevant Pizza relations. It deliberately excludes teaching-oriented or out-of-scope concepts such as `pizza:Country` and `pizza:IceCream` through the local `smp:excludesElement` relation.

Cross-example evidence matters here: Wine/Food did not need an explicit exclusion relation, so this remains a Pizza-specific modeling choice rather than a reusable SMO feature.

## 7. Runtime data, validation, and inference

Runtime menu data is separate from model definitions. The repository uses SHACL to validate declared graph structure and OWL RL reasoning to demonstrate entailment.

Example inference:

```text
Asserted:
    DiavolaPizza a Pizza
    DiavolaPizza hasTopping ChilliTopping
    ChilliTopping a SpicyTopping

Inferred:
    DiavolaPizza a SpicyPizza
```

This preserves the distinction:

```text
Assertions       what data explicitly states
OWL inference    what follows from ontology semantics
SHACL validation whether graph structure satisfies constraints
```

## 8. Operational contract and lineage

The first operational artifact is:

```text
find_suitable_pizzas
```

It is derived from the Pizza Menu Semantic Model and applies in a restaurant-menu runtime context. Inputs/outputs and runtime context are local execution-oriented concepts, not SMO vocabulary.

The lineage query verifies the direct chain:

```text
find_suitable_pizzas Agent Contract
    prov:wasDerivedFrom
Pizza Menu Semantic Model

Pizza Menu Semantic Model
    prov:wasDerivedFrom
historical Pizza Ontology
```

Execution therefore remains connected to semantic foundations without making the artifacts identical.

## 9. Cross-example findings

The completed Pizza ↔ Wine/Food evidence cycle produced these decisions:

- competency questions recur independently → reuse MOD `mod:competencyQuestion`;
- source lineage recurs → DCTERMS/PROV-O are sufficient;
- explicit exclusions do not recur → keep `smp:excludesElement` local;
- generic derivation is not an `smo:ImplementationProjection` → preserve the narrow governed class;
- operation signatures/runtime context/agent contracts remain local or ESKA-adjacent;
- recommendation-evidence structure remains insufficiently recurrent for reusable vocabulary;
- cache integrity is a repository engineering contract unless broader evidence emerges.

This is the intended governance pattern: demonstrate locally, compare independently, check standards, and generalize only when necessary.

## 10. Design principles

### Preserve external identity

Historical Pizza identifiers remain unchanged in the cached representation and repository metadata.

### Cache without forking

Caching preserves exact source bytes for reproducibility; it does not authorize semantic edits or new ontology identity.

### Use established vocabularies first

DCTERMS, PROV-O, and MOD are preferred over expanding SMO for relationships they already express adequately.

### Separate source, model, runtime, and execution artifacts

Each has a distinct lifecycle and authority boundary.

### Negative evidence matters

A concept observed in Pizza is not reusable merely because it is convenient locally. The Wine/Food comparison is explicitly used to test that assumption.

### Preserve machine-readable lineage

Operational artifacts must remain traceable to the semantic models on which they depend.

## 11. Current open questions

The earlier competency-question question is resolved through MOD. Remaining questions require new evidence rather than immediate vocabulary work:

1. Will another independent domain require explicit exclusion semantics?
2. When will a concrete artifact satisfy the governed `smo:ImplementationProjection` definition in this reference example?
3. Do operation-signature/runtime-context concepts recur strongly enough to warrant ESKA-level abstraction?
4. Does recommendation evidence need a reusable structure beyond established provenance vocabularies?
5. Is an RDF integrity vocabulary needed across repositories, or is the current manifest approach sufficient?

## 12. Visibility boundary

The semantic/reference baseline, sibling comparison, standards review, source attribution, and validation are stable enough for a public-readiness decision. SKE #29 owns that visibility decision.

Making this repository public would not imply authority over `co-ode.org`, endorsement by the original Pizza authors/hosts, activation of the separate Pizza #72 preservation/reference W3ID proposal, or standardization of local `smp:` vocabulary.
