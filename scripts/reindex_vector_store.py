#!/usr/bin/env python
"""Force rebuild of the legal knowledge vector store."""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from services.retrieval import KnowledgeRetrieval  # noqa: E402


def main():
    print("Rebuilding vector store from CSV sources...")
    KnowledgeRetrieval(force_reindex=True)
    print("Reindex complete.")


if __name__ == "__main__":
    main()
