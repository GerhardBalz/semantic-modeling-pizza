# Semantic Modeling Pizza backlog

This backlog owns repository-local improvements for the Semantic Modeling Pizza reference example. Cross-repository governance and reusable vocabulary decisions remain owned by SKE and SMO respectively.

## Active

- Keep the repository role aligned with the SKE initiative map and current evidence conventions.
- Preserve the separation between external source semantics, repository representations, purpose-specific semantic models, implementation projections, runtime data, validation/inference evidence, and operational artifacts.
- Support the explicit visibility decision in SKE #29; do not treat visibility as semantic authority or maturity.

## Completed evidence cycle

- Semantic Modeling Pizza #6 / PR #7 — aligned current artifacts with governed SMO v0.1 and isolated historical experimental vocabulary.
- SKE #25 / PR #26 and SKE PR #28 — compared Pizza with Wine/Food and recorded the cross-domain decision matrix.
- SMO #22 / PR #23 — concluded that competency questions should reuse MOD rather than add SMO vocabulary.
- Semantic Modeling Pizza #8 / PR #9 — adopted `mod:competencyQuestion` and removed the superseded literal `smp:answersQuestion` relation from current artifacts.

## Candidate follow-ups

- Keep `smp:excludesElement` local unless another independent domain demonstrates the same need and established standards remain insufficient.
- Evaluate operation-signature, runtime-context, and recommendation-evidence semantics against ESKA and a second executable domain before proposing reusable vocabulary.
- Add an explicit `smo:ImplementationProjection` example here only if a concrete implementation-facing artifact satisfies the governed definition; do not introduce one merely for symmetry.
- Revisit cryptographic-integrity RDF modeling only if a concrete cross-repository need emerges; the current JSON manifest remains sufficient for the cache contract.

## Visibility

The reference-example and sibling-comparison prerequisites for public-readiness are complete. The remaining decision is initiative governance under SKE #29, including final public-facing documentation review and verification of the resulting repository URLs.

## Ownership rule

Use this repository backlog for improvements specific to the Pizza reference example. Link reusable findings to the appropriate upstream backlog instead of silently generalizing them:

- SKE initiative/governance and cross-repository conventions: `GerhardBalz/semantic-knowledge-engineering`
- SMO reusable semantic-modeling vocabulary: `GerhardBalz/semantic-modeling-ontology`
- Pizza preservation/reference engineering: `GerhardBalz/pizza-ontology`
- sibling Wine/Food reference-example work: `GerhardBalz/semantic-modeling-wine-food`
