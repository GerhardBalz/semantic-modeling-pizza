# Semantic Modeling Pizza

A Semantic Knowledge Engineering (SKE) reference example that applies the Semantic Modeling Ontology (SMO) to the Pizza domain while keeping semantic models, implementation projections, runtime data, validation/inference evidence, and operational artifacts distinct.

> **Status:** Public reference-example baseline complete. The repository is public following the completed SKE #29 publication decision. Public visibility is a publication/governance state; it does not transfer authority over the historical Pizza namespace or imply semantic maturity beyond the evidence in this repository.

## Initiative role

This repository is the **Semantic Modeling Pizza reference example** within the broader SKE initiative.

Related repositories have deliberately different responsibilities:

- [Semantic Knowledge Engineering](https://github.com/GerhardBalz/semantic-knowledge-engineering) — initiative architecture, governance, conventions, sequencing, and repository map;
- [Semantic Modeling Ontology](https://github.com/GerhardBalz/semantic-modeling-ontology) — reusable semantic-modeling vocabulary, currently `smo:SemanticModel` and `smo:ImplementationProjection`;
- [Pizza Ontology](https://github.com/GerhardBalz/pizza-ontology) — preservation/reference engineering around the historical Pizza Ontology;
- [Semantic Modeling Wine/Food](https://github.com/GerhardBalz/semantic-modeling-wine-food) — sibling executable semantic-modeling reference example.

`semantic-modeling-pizza` does **not** own the historical Pizza ontology, the `co-ode.org` namespace, SKE governance, or reusable SMO vocabulary. It owns the repository-authored reference-example artifacts and the evidence produced by applying the initiative patterns to Pizza.

See [`docs/initiative-role.md`](docs/initiative-role.md) for the detailed ownership and escalation boundaries.

## Purpose and artifact chain

The project separates:

1. the external Pizza Ontology and its historical identity;
2. a verified local cache of the canonical RDF/XML representation;
3. metadata describing the source ontology as an `smo:SemanticModel`;
4. a purpose-specific Pizza Menu `smo:SemanticModel` derived from the source;
5. concrete runtime menu data;
6. SHACL validation and OWL inference evidence;
7. an operational `find_suitable_pizzas` agent contract with explicit lineage.

```text
Protégé Pizza Ontology
        ↓ cached and verified as
Local canonical representation
        ↓ described as
smo:SemanticModel
        ↓ source of
Pizza Menu Semantic Model
        ↓ applied to
Example menu data
        ↓ verified by
SHACL + OWL inference + SPARQL lineage
        ↓ operationalized as
find_suitable_pizzas Agent Contract
```

The layers are traceable but not interchangeable. A cache is not a new ontology, derivation does not automatically create an `smo:ImplementationProjection`, and an operational contract is not domain semantics.

## Vocabulary choices

The current example uses:

- `smo:SemanticModel` only where the governed SMO meaning applies;
- DCTERMS and PROV-O for source, derivation, representation, and conformance relationships;
- MOD `mod:competencyQuestion` for textual competency questions following SMO #22 / PR #23;
- local `smp:` vocabulary for Pizza-specific or execution-adjacent concepts that are not justified as reusable SMO terms.

The local exclusion relation remains Pizza-specific evidence. The sibling Wine/Food example did not require explicit exclusions, so no cross-domain vocabulary promotion is justified.

See [`docs/governed-smo-v0.1-alignment.md`](docs/governed-smo-v0.1-alignment.md) and [`docs/architecture.md`](docs/architecture.md).

## Source ontology cache

The project uses the Pizza Ontology from the Protégé tutorial. Its embedded ontology metadata identifies version 2.0 and Creative Commons Attribution 3.0.

The cached representation under [`source/cache`](source/cache) is byte-for-byte retrieved source material used for deterministic validation and inference. It retains the original ontology/version identity and is **not** a fork or replacement ontology.

Verify the cache:

```bash
python tools/pizza_cache.py verify
```

Check for upstream byte changes:

```bash
python tools/pizza_cache.py check-upstream
```

See [`NOTICE.md`](NOTICE.md) and [`source/README.md`](source/README.md) for attribution and maintenance boundaries.

## Executable evidence

The repository contains:

- purpose-specific semantic-model metadata;
- concrete menu data;
- positive and negative SHACL cases;
- an OWL RL inference showing a pizza inferred as `pizza:SpicyPizza`;
- an operational contract;
- a SPARQL lineage query;
- regression tests protecting the governed SMO/MOD vocabulary boundaries.

Run the deterministic validation suite:

```bash
python -m pip install -r requirements-dev.txt
python tools/pizza_cache.py verify
python -m unittest discover -s tests -v
```

## Repository structure

```text
.
├── .github/workflows/
├── README.md
├── BACKLOG.md
├── CONTRIBUTING.md
├── LICENSE
├── NOTICE.md
├── docs/
│   ├── architecture.md
│   ├── governed-smo-v0.1-alignment.md
│   └── initiative-role.md
├── source/
│   ├── pizza-import.ttl
│   └── cache/
├── models/
├── examples/
├── data/
├── contracts/
├── shapes/
├── queries/
├── tests/
└── tools/
```

## Evidence and governance

Reusable findings are not silently promoted. The completed Pizza ↔ Wine/Food evidence cycle is governed through SKE; SMO #22 concluded that competency questions should reuse MOD rather than add new SMO vocabulary.

Repository-local follow-up work is maintained in [`BACKLOG.md`](BACKLOG.md). The repository is public following completed SKE #29. That publication decision does not imply authority over the historical Pizza namespace or approval of the separate Pizza preservation/reference W3ID proposal in Pizza #72.

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md).

## License

Original work in this repository is licensed under the MIT License. The external Pizza Ontology remains licensed separately under CC BY 3.0 as recorded in [`NOTICE.md`](NOTICE.md).
