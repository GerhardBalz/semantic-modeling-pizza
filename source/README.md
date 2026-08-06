# Source ontology

This directory references and caches the canonical Protégé Pizza Ontology used by the project.

## Canonical document

```text
https://protege.stanford.edu/ontologies/pizza/pizza.owl
```

## Ontology identity

```text
Ontology IRI: http://www.co-ode.org/ontologies/pizza
Version IRI:  http://www.co-ode.org/ontologies/pizza/2.0.0
Version:      2.0
Format:       RDF/XML
License:      Creative Commons Attribution 3.0 (CC BY 3.0)
```

The cached file does not create a new ontology identity. It is a byte-for-byte retrieved representation of the canonical document and retains the ontology and version IRIs embedded in that document.

## Cached representation

```text
source/cache/pizza.owl
source/cache/pizza-manifest.json
```

The manifest records:

- the canonical source URL;
- retrieval timestamp;
- SHA-256 hash;
- byte size;
- ontology IRI;
- version IRI and version information;
- license text extracted from the ontology.

The current cache is verified without network access on every pull request and push to `main`.

```bash
python tools/pizza_cache.py verify
```

## Checking for upstream changes

A scheduled GitHub Actions workflow compares the canonical source with the cached SHA-256 once per week. It can also be run manually.

```bash
python tools/pizza_cache.py check-upstream
```

A changed upstream hash causes the check to fail and prints the cached and upstream hashes.

## Refreshing the cache

Create a feature branch and run:

```bash
python tools/pizza_cache.py refresh
python tools/pizza_cache.py verify
```

Alternatively, run the **Refresh Pizza ontology cache** workflow from a feature branch. The workflow explicitly refuses to commit to `main`.

[`pizza-import.ttl`](pizza-import.ttl) continues to import the ontology using its original ontology IRI. The cached representation exists for reproducibility and offline validation, not as a fork of the ontology.
