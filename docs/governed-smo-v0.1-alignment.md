# Governed SMO v0.1 alignment

The original Semantic Modeling Pizza experiment predates governed SMO v0.1 and used `https://github.com/GerhardBalz/semantic-modeling-ontology#` for an exploratory vocabulary surface.

That historical surface included terms such as `Model`, `ModelRepresentation`, `ModelElement`, `Artifact`, model-kind/language relations, projection lineage, constraints, runtime context, and agent-contract concepts. Those terms are **not** published SMO v0.1 vocabulary.

Current artifacts use governed SMO only at:

```text
https://w3id.org/smo#
```

and only for concepts actually published there:

```text
smo:SemanticModel
smo:ImplementationProjection
```

In the current Pizza example:

- the historical Pizza ontology and the Pizza Menu Semantic Model are `smo:SemanticModel` instances;
- no artifact is classified as `smo:ImplementationProjection` merely because it is derived;
- DCTERMS and PROV-O express source, derivation, representation/format, conformance, and part relationships where sufficient;
- agent-contract, runtime-context, competency-question, exclusion, and operation-signature concepts remain explicitly local `smp:` experimental vocabulary;
- historical Pizza ontology/version/entity IRIs remain unchanged.

Tests reject the old GitHub SMO namespace in current Turtle artifacts and reject governed-SMO IRIs other than the published v0.1 classes.

This cleanup preserves the experimental evidence without promoting it into SMO. Any future reusable term requires independent cross-domain evidence through SKE before an SMO change is proposed.
