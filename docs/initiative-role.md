# SKE reference-example role

## Purpose

`semantic-modeling-pizza` is a Semantic Knowledge Engineering (SKE) **semantic-modeling reference example**. Its purpose is to exercise the Semantic Modeling Ontology (SMO) against a concrete domain and make the resulting modeling, projection, runtime, validation/inference, and operational boundaries explicit and executable.

This role is intentionally narrower than the related Pizza preservation/reference project.

## Repository relationships

```text
Semantic Knowledge Engineering
    initiative architecture / governance / conventions
        ↓
Semantic Modeling Ontology
    reusable semantic-modeling vocabulary
        ↓ exercised by
Semantic Modeling Pizza
    Pizza-domain reference example
        ↔ related to
Pizza Ontology
    historical preservation / reference / proving ground

Semantic Modeling Pizza
        ↔ sibling comparison
Semantic Modeling Wine/Food
```

### SKE

[GerhardBalz/semantic-knowledge-engineering](https://github.com/GerhardBalz/semantic-knowledge-engineering) owns the initiative map, cross-repository architecture, conventions, sequencing, and governance. This repository adopts that positioning but does not duplicate SKE ownership.

### SMO

[GerhardBalz/semantic-modeling-ontology](https://github.com/GerhardBalz/semantic-modeling-ontology) owns reusable semantic-modeling vocabulary. Local `smp:` terms remain experiment evidence until repeated use across independent examples justifies SMO evaluation.

### Pizza Ontology

[GerhardBalz/pizza-ontology](https://github.com/GerhardBalz/pizza-ontology) owns the preservation/reference engineering line around the historical Pizza Ontology. It preserves historical identity, publication evidence, reference-resolution policy, and broader proving-ground artifacts.

This repository does not replace that work. It consumes the Pizza domain as a semantic-modeling example and owns only the reference-example artifacts authored here.

### Wine/Food sibling

[GerhardBalz/semantic-modeling-wine-food](https://github.com/GerhardBalz/semantic-modeling-wine-food) is the sibling reference example. It is currently bootstrap-pending. Its main initiative value is not duplication but comparison: recurring requirements across Pizza and Wine/Food are stronger evidence for reusable conventions or vocabulary than a Pizza-only need.

## Artifact boundaries

The reference example keeps these artifact categories distinct:

| Category | Meaning | Example here | Ownership implication |
| --- | --- | --- | --- |
| External semantic model | Source domain semantics with independent authority | historical Pizza Ontology | not owned here |
| Repository representation | Reproducible local bytes or metadata for the source | cached Pizza RDF/XML + manifest | representation maintained here; source semantics not owned here |
| Semantic model | Purpose-specific reusable meaning | Pizza Menu Semantic Model | owned here |
| Implementation projection | Purpose-specific implementation-facing representation of a semantic model | only where explicitly introduced and typed | owned here when present; never inferred merely from derivation |
| Runtime data | Current facts using the model | example menu items, prices, availability | owned here as example data |
| Validation evidence | Evidence that declared constraints are satisfied or violated | SHACL positive/negative tests | verification artifact, not semantic model or projection |
| Inference evidence | Evidence of entailments under ontology semantics | inferred `SpicyPizza` type | verification evidence, not authored domain semantics |
| Operational artifact | Contract exposing semantic capability | `find_suitable_pizzas` agent contract | owned here; retains lineage to source models |

The important invariant is that traceability does not collapse category boundaries. Derivation alone does not make an artifact an `smo:ImplementationProjection`, and execution/validation evidence does not become domain semantics merely because it depends on the model.

## Upward flow of reusable findings

This repository is evidence-producing rather than vocabulary-authoritative.

Use the following escalation rule:

```text
Pizza-specific need
    → keep local in semantic-modeling-pizza

Repeated cross-example engineering/governance pattern
    → raise to SKE

Repeated cross-example semantic-modeling concept
    → raise to SMO vocabulary evaluation
```

Current candidate findings include:

- competency-question relationships;
- explicit excluded-element scope;
- operational signatures and semantic input/output concepts;
- recommendation evidence and provenance;
- representation-integrity modeling.

None of these should be generalized from the Pizza example alone. Wine/Food or another independent example should provide corroborating evidence first unless a standards-aligned existing vocabulary already supplies the needed semantics.

## Repository-local backlog

Repository-specific improvements are tracked in [`../BACKLOG.md`](../BACKLOG.md). Cross-repository work should link to SKE or SMO instead of being duplicated locally.

## Visibility decision

The repository is currently **private by deliberate governance choice**. This is independent of semantic maturity.

The visibility decision should be revisited after:

1. the SKE reference-example positioning is stable;
2. the Wine/Food sibling has a comparable baseline;
3. provenance, licensing, and external-source attribution remain clear for public consumption.

Making the repository public later should therefore be an explicit publication/governance action, not an implicit consequence of completing a modeling milestone.
