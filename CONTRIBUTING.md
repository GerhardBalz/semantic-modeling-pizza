# Contributing

## Development workflow

Changes must not be committed directly to `main`.

Use the following workflow for every change, including small documentation updates:

1. Create a focused branch from the current `main` branch.
2. Make the intended changes on that branch.
3. Validate the affected ontology, SHACL, examples, documentation, or tooling.
4. Commit the changes with a concise and descriptive commit message.
5. Open a pull request targeting `main`.
6. Merge the pull request automatically after the applicable checks have passed.

Squash merging is preferred so that each pull request results in one coherent commit on `main`.

The `main` branch should remain usable and represent the current accepted state of the project.

Post-merge review may be used when explicitly agreed, but the branch and pull-request workflow still applies.

A completely empty repository may require one minimal bootstrap commit to establish the default branch before the first pull request can be created. All substantive initialization must still be performed through a branch and pull request.

## Branch naming

Use short, descriptive branch names, for example:

```text
feature/add-pizza-projection
docs/clarify-source-ontology
fix/model-description-shape
```

Automation-created branches may use:

```text
agent/<change-description>
```

## Pull requests

A pull request should explain:

- what changed;
- why the change is needed;
- which files or concepts are affected;
- how the change was validated.
