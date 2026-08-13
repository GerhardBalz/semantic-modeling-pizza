# SKE reference-example role

## Purpose

`semantic-modeling-pizza` is a Semantic Knowledge Engineering (SKE) **semantic-modeling reference example**. Its purpose is to exercise governed semantic-modeling concepts against a concrete domain and make the resulting model, runtime, validation/inference, and operational boundaries explicit and executable.

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
        ↔ sibling comparison
Semantic Modeling Wine/Food

Semantic Modeling Pizza
        ↔ related to
Pizza Ontology
    historical preservation / reference / proving ground
```

### SKE

[GerhardBalz/semantic-knowledge-engineering](https://github.com/GerhardBalz/semantic-knowledge-engineering) owns the initiative map, cross-repository architecture, conventions, sequencing, and governance. This repository adopts that positioning but does not duplicate SKE ownership.

### SMO

[GerhardBalz/semantic-modeling-ontology](https://github.com/GerhardBalz/semantic-modeling-ontology) owns reusable semantic-modeling vocabulary. Current governed SMO v0.1 provides `smo:SemanticModel` and `smo:ImplementationProjection`.

The completed competency-question evaluation in SMO #22 / PR #23 is an example of the escalation rule working as intended: Pizza and Wine/Food supplied independent evidence, standards were checked first, and the result was to reuse MOD `mod:competencyQuestion` rather than expand SMO.

### Pizza Ontology

[GerhardBalz/pizza-ontology](https://github.com/GerhardBalz/pizza-ontology) owns preservation/reference engineering around the historical Pizza Ontology. It preserves historical identity, publication evidence, reference-resolution policy, and broader proving-ground artifacts.

This repository does not replace that work. It consumes Pizza as a semantic-modeling example and owns only the reference-example artifacts authored here.

### Wine/Food sibling

[GerhardBalz/semantic-modeling-wine-food](https://github.com/GerhardBalz/semantic-modeling-wine-food) is the sibling executable reference example. Its role is comparison rather than duplication. It provided the independent evidence needed to test Pizza-observed concepts, including positive recurrence for competency questions and negative evidence for explicit exclusions, first-class question resources, and `smo:ImplementationProjection` use.

## Artifact boundaries

| Category | Meaning | Example here | Ownership implication |
| --- | --- | --- | --- |
| External semantic model | Source domain semantics with independent authority | historical Pizza Ontology | not owned here |
| Repository representation | Reproducible local bytes or metadata for the source | cached Pizza RDF/XML + manifest | representation maintained here; source semantics not owned here |
| Semantic model | Purpose-specific reusable meaning | Pizza Menu Semantic Model | owned here |
| Implementation projection | Non-authoritative implementation-facing projection satisfying the governed SMO definition | none required by the current reference baseline | never inferred merely from derivation |
| Runtime data | Current facts using the model | example menu items, prices, availability | owned here as example data |
| Validation evidence | Evidence that declared constraints are satisfied or violated | SHACL positive/negative tests | verification artifact, not semantic model or projection |
| Inference evidence | Evidence of entailments under ontology semantics | inferred `SpicyPizza` type | verification evidence, not authored domain semantics |
| Operational artifact | Contract exposing semantic capability | `find_suitable_pizzas` agent contract | owned here; retains lineage to source models |

The invariant is that traceability does not collapse category boundaries. Derivation alone does not make an artifact an `smo:ImplementationProjection`, and execution/validation evidence does not become domain semantics merely because it depends on the model.

## Upward flow of reusable findings

```text
Pizza-specific need
    → keep local in semantic-modeling-pizza

Repeated cross-example engineering/governance pattern
    → raise to SKE

Repeated cross-example semantic-modeling concept
    → standards-first SMO evaluation
```

Current outcomes:

- competency questions → **MOD `mod:competencyQuestion`**, not SMO;
- explicit excluded-element scope → remains Pizza-local because Wine/Food did not require it;
- operation signatures, runtime context, and agent contracts → local / ESKA-adjacent pending independent evidence;
- recommendation evidence/provenance → defer until a second domain demonstrates a reusable need;
- representation integrity → current cache manifest remains repository engineering unless broader evidence emerges.

## Repository-local backlog

Repository-specific improvements are tracked in [`../BACKLOG.md`](../BACKLOG.md). Cross-repository work should link to SKE or SMO instead of being duplicated locally.

## Visibility decision

The original private-bootstrap prerequisites are now satisfied: SKE positioning is stable, the Wine/Food sibling has an executable comparable baseline, source attribution/licensing boundaries are explicit, and the first cross-domain standards cycle is complete.

The remaining visibility decision is governed by SKE #29. A public repository would still not imply authority over the historical Pizza namespace, approval of the separate Pizza #72 W3ID proposal, or standardization of local experimental vocabulary.
