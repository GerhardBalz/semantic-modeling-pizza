from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tempfile
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CACHE_PATH = ROOT / "source" / "cache" / "pizza.owl"
MANIFEST_PATH = ROOT / "source" / "cache" / "pizza-manifest.json"
SOURCE_URL = "https://protege.stanford.edu/ontologies/pizza/pizza.owl"
USER_AGENT = "semantic-modeling-pizza-cache/1.0"

NS = {
    "owl": "http://www.w3.org/2002/07/owl#",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "dc": "http://purl.org/dc/elements/1.1/",
    "dcterms": "http://purl.org/dc/terms/",
}
RDF_ABOUT = f"{{{NS['rdf']}}}about"
RDF_RESOURCE = f"{{{NS['rdf']}}}resource"


class CacheError(RuntimeError):
    pass


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def fetch_upstream() -> bytes:
    request = urllib.request.Request(
        SOURCE_URL,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/rdf+xml, application/xml;q=0.9, */*;q=0.1",
        },
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        content = response.read()
    if not content:
        raise CacheError("Upstream Pizza ontology returned an empty response.")
    return content


def ontology_metadata(content: bytes) -> dict[str, str | None]:
    try:
        root = ET.fromstring(content)
    except ET.ParseError as exc:
        raise CacheError(f"Cached content is not valid XML: {exc}") from exc

    ontology = root.find("owl:Ontology", NS)
    if ontology is None:
        raise CacheError("No owl:Ontology element found in cached content.")

    version_iri = ontology.find("owl:versionIRI", NS)
    version_info = ontology.find("owl:versionInfo", NS)
    license_node = ontology.find("dcterms:license", NS)

    return {
        "ontology_iri": ontology.get(RDF_ABOUT),
        "version_iri": version_iri.get(RDF_RESOURCE) if version_iri is not None else None,
        "version_info": version_info.text.strip() if version_info is not None and version_info.text else None,
        "license": license_node.text.strip() if license_node is not None and license_node.text else None,
    }


def build_manifest(content: bytes) -> dict[str, Any]:
    metadata = ontology_metadata(content)
    return {
        "schema_version": 1,
        "source_url": SOURCE_URL,
        "retrieved_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "sha256": sha256_bytes(content),
        "size_bytes": len(content),
        **metadata,
    }


def load_manifest() -> dict[str, Any]:
    try:
        return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise CacheError(f"Cache manifest does not exist: {MANIFEST_PATH.relative_to(ROOT)}") from exc
    except json.JSONDecodeError as exc:
        raise CacheError(f"Cache manifest is invalid JSON: {exc}") from exc


def atomic_write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as temp:
        temp.write(content)
        temp_path = Path(temp.name)
    temp_path.replace(path)


def refresh() -> int:
    content = fetch_upstream()
    new_hash = sha256_bytes(content)

    if CACHE_PATH.exists() and MANIFEST_PATH.exists():
        current_manifest = load_manifest()
        current_hash = sha256_bytes(CACHE_PATH.read_bytes())
        if current_hash == new_hash and current_manifest.get("sha256") == new_hash:
            print(f"Pizza ontology cache is already current: sha256={new_hash}")
            return 0

    manifest = build_manifest(content)
    atomic_write(CACHE_PATH, content)
    atomic_write(
        MANIFEST_PATH,
        (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode("utf-8"),
    )
    print(
        "Updated Pizza ontology cache: "
        f"sha256={manifest['sha256']} size={manifest['size_bytes']} bytes"
    )
    return 0


def verify() -> int:
    try:
        content = CACHE_PATH.read_bytes()
    except FileNotFoundError as exc:
        raise CacheError(f"Cached ontology does not exist: {CACHE_PATH.relative_to(ROOT)}") from exc

    manifest = load_manifest()
    actual_hash = sha256_bytes(content)
    expected_hash = manifest.get("sha256")
    if actual_hash != expected_hash:
        raise CacheError(
            f"Cached ontology hash mismatch: expected {expected_hash}, actual {actual_hash}."
        )
    if len(content) != manifest.get("size_bytes"):
        raise CacheError(
            f"Cached ontology size mismatch: expected {manifest.get('size_bytes')}, actual {len(content)}."
        )
    if manifest.get("source_url") != SOURCE_URL:
        raise CacheError("Cache manifest source_url does not match the configured canonical URL.")

    metadata = ontology_metadata(content)
    for key in ("ontology_iri", "version_iri", "version_info", "license"):
        if metadata.get(key) != manifest.get(key):
            raise CacheError(
                f"Cached ontology metadata mismatch for {key}: "
                f"manifest={manifest.get(key)!r}, content={metadata.get(key)!r}."
            )

    print(
        "Verified Pizza ontology cache: "
        f"sha256={actual_hash} version={metadata.get('version_info')}"
    )
    return 0


def check_upstream() -> int:
    verify()
    manifest = load_manifest()
    upstream = fetch_upstream()
    upstream_hash = sha256_bytes(upstream)
    cached_hash = manifest["sha256"]

    if upstream_hash != cached_hash:
        print("Upstream Pizza ontology differs from the cached representation.", file=sys.stderr)
        print(f"cached:   {cached_hash}", file=sys.stderr)
        print(f"upstream: {upstream_hash}", file=sys.stderr)
        print("Run: python tools/pizza_cache.py refresh", file=sys.stderr)
        return 3

    print(f"Upstream Pizza ontology is unchanged: sha256={cached_hash}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Manage the canonical Pizza ontology cache.")
    parser.add_argument("command", choices=("refresh", "verify", "check-upstream"))
    args = parser.parse_args()

    try:
        if args.command == "refresh":
            return refresh()
        if args.command == "verify":
            return verify()
        return check_upstream()
    except (CacheError, OSError, urllib.error.URLError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
