#!/usr/bin/env python
"""Ingest statutory data from external legal APIs into data/laws CSVs."""

import argparse
import csv
import json
import os
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Optional

import requests
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "laws"
CONFIG_PATH = DATA_DIR / "sources.json"

DEFAULT_HEADERS = {"Accept": "application/json"}


def load_config(path: Path) -> Dict:
    if not path.exists():
        raise FileNotFoundError(f"Law sources configuration not found at {path}")
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def build_headers(base_headers: Dict[str, str]) -> Dict[str, str]:
    headers = dict(DEFAULT_HEADERS)
    headers.update(base_headers or {})

    api_key = os.getenv("LAW_API_KEY")
    header_name = os.getenv("LAW_API_KEY_HEADER", "Authorization")
    scheme = os.getenv("LAW_API_KEY_SCHEME", "Bearer")
    if api_key:
        headers[header_name] = f"{scheme} {api_key}".strip()
    return headers


def normalise_endpoint(endpoint: str) -> str:
    base = os.getenv("LAW_API_BASE", "").rstrip("/")
    if not endpoint.startswith("http"):
        if not base:
            raise ValueError("Relative endpoint provided but LAW_API_BASE is not set")
        return f"{base}{endpoint}"
    return endpoint


def extract_sections(payload: Dict) -> List[Dict]:
    if isinstance(payload, list):
        return payload
    for key in ("sections", "data", "results", "items"):
        value = payload.get(key)
        if isinstance(value, list):
            return value
    raise ValueError("Unable to locate sections array in API response")


def fetch_sections(source: Dict, headers: Dict[str, str]) -> Iterable[Dict]:
    endpoint = normalise_endpoint(source["endpoint"])
    params = source.get("params", {})
    method = source.get("method", "GET").upper()
    session = requests.Session()

    while True:
        resp = session.request(method, endpoint, params=params, headers=headers, timeout=30)
        if resp.status_code >= 400:
            raise RuntimeError(f"API request failed for {source['id']} ({resp.status_code}): {resp.text[:200]}")
        payload = resp.json()
        sections = extract_sections(payload)
        for section in sections:
            yield section

        next_link = payload.get("next") or payload.get("links", {}).get("next")
        if not next_link:
            break
        endpoint = next_link if next_link.startswith("http") else normalise_endpoint(next_link)
        params = {}


def normalise_record(section: Dict, source: Dict) -> Dict[str, str]:
    title = section.get("title") or section.get("section_title") or section.get("name") or "Untitled"
    code = section.get("section_code") or section.get("number") or section.get("code") or ""
    text = section.get("text") or section.get("content") or section.get("body") or ""
    citations = section.get("citations") or section.get("references") or []

    if isinstance(citations, list):
        citations_val = "; ".join(str(c) for c in citations if c)
    else:
        citations_val = str(citations)

    jurisdiction = source.get("jurisdiction", "IN")
    act_name = source.get("act_name", source.get("id", ""))

    return {
        "title": title.strip(),
        "section_code": str(code).strip(),
        "act_name": act_name,
        "jurisdiction": jurisdiction,
        "text": text.strip(),
        "citations": citations_val.strip(),
    }


def write_csv(records: Iterable[Dict[str, str]], destination: Path) -> int:
    destination.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["title", "section_code", "act_name", "jurisdiction", "text", "citations"]
    count = 0
    with destination.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for record in records:
            writer.writerow(record)
            count += 1
    return count


def ingest_source(source: Dict, headers: Dict[str, str]) -> int:
    print(f"Fetching {source['act_name']} ({source['id']})...")
    sections = (normalise_record(section, source) for section in fetch_sections(source, headers))
    destination = DATA_DIR / f"{source['id']}.csv"
    count = write_csv(sections, destination)
    print(f"  -> wrote {count} sections to {destination.relative_to(PROJECT_ROOT)}")
    return count


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description="Ingest law sections from external APIs")
    parser.add_argument("--source", dest="source_ids", action="append", help="Specific source id(s) to ingest")
    parser.add_argument("--config", dest="config_path", default=str(CONFIG_PATH), help="Path to sources.json")

    args = parser.parse_args()

    config = load_config(Path(args.config_path))
    sources = config.get("sources", [])
    if not sources:
        print("No sources defined in configuration", file=sys.stderr)
        sys.exit(1)

    if args.source_ids:
        wanted = set(args.source_ids)
        sources = [src for src in sources if src["id"] in wanted]
        if not sources:
            print(f"No matching sources for ids: {', '.join(wanted)}", file=sys.stderr)
            sys.exit(1)

    headers = build_headers(config.get("default_headers", {}))

    total = 0
    for source in sources:
        try:
            total += ingest_source(source, headers)
        except Exception as exc:
            print(f"Failed to ingest {source['id']}: {exc}", file=sys.stderr)

    print(f"Completed ingestion. Total sections processed: {total}")


if __name__ == "__main__":
    main()
