# Semantic Modeling Pizza backlog

This backlog owns repository-local improvements for the Semantic Modeling Pizza reference example. Cross-repository governance and reusable vocabulary decisions remain owned by SKE and SMO respectively.

## Active

- Keep the repository role aligned with the SKE initiative map and with `semantic-modeling-pizza#4`.
- Preserve the separation between source semantic model, purpose-specific semantic model, implementation projections, runtime data, validation/inference evidence, and operational/agent artifacts.
- Exercise local experimental vocabulary only where the Pizza example needs it; promote findings upward only after evidence shows cross-example reuse.
- Reassess the current private visibility deliberately after the reference-example baseline and sibling Wine/Food bootstrap are mature enough for public comparison.

## Candidate follow-ups

- Compare Pizza findings with the Wine/Food reference example once `semantic-modeling-wine-food` is bootstrapped.
- Evaluate whether competency-question and excluded-element relationships recur across examples strongly enough to justify SMO backlog work.
- Evaluate operation-signature and evidence/provenance needs against ESKA and other execution examples before proposing reusable vocabulary.
- Reassess whether implementation-projection examples should be added here or linked from the related `pizza-ontology` proving ground rather than duplicated.

## Ownership rule

Use this repository backlog for improvements specific to the Pizza reference example. Link reusable findings to the appropriate upstream backlog instead of silently generalizing them here:

- SKE initiative/governance and cross-repository conventions: `GerhardBalz/semantic-knowledge-engineering`
- SMO reusable semantic-modeling vocabulary: `GerhardBalz/semantic-modeling-ontology`
- Pizza preservation/reference engineering: `GerhardBalz/pizza-ontology`
- sibling Wine/Food reference-example work: `GerhardBalz/semantic-modeling-wine-food`
