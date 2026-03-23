#!/usr/bin/env python3
"""Memray stress test for link_fixer hot paths."""

import os

os.environ.setdefault("LOG_LEVEL", "ERROR")

from provide.foundry.docs.link_fixer import fix_md_links


def _build_markdown_document(num_links: int) -> str:
    """Build a synthetic markdown document with many links."""
    lines = ["# Test Document\n", "Some introductory text.\n"]
    for i in range(num_links):
        if i % 5 == 0:
            lines.append(f"[external](https://example.com/page{i}.md)")
        elif i % 5 == 1:
            lines.append(f"[local link](../path/to/file{i}.md)")
        elif i % 5 == 2:
            lines.append(f"[anchored](page{i}.md#section-{i})")
        elif i % 5 == 3:
            lines.append(f"[deep path](../../docs/guide/topic{i}.md)")
        else:
            lines.append(f"[special](path/.provide/config{i}.md)")
    return "\n".join(lines)


def main() -> None:
    cycles = 500
    links_per_doc = 200

    # Warmup
    doc = _build_markdown_document(links_per_doc)
    for _ in range(5):
        fix_md_links(doc)

    # Stress: N cycles
    for _ in range(cycles):
        fix_md_links(doc, preserve_special=True)
        fix_md_links(doc, preserve_special=False)

    print(f"link_fixer stress complete: {cycles} cycles x {links_per_doc} links")


if __name__ == "__main__":
    main()
