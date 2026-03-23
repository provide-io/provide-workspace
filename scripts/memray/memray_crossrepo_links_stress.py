#!/usr/bin/env python3
"""Memray stress test for crossrepo_links plugin hot paths."""

import os

os.environ.setdefault("LOG_LEVEL", "ERROR")

from provide.foundry.mkdocs_plugins.crossrepo_links import CrossRepoLinksPlugin


def _build_markdown_with_crossrepo_links(num_links: int) -> str:
    """Build markdown with cross-repo links to transform."""
    packages = [
        "pyvider",
        "pyvider-cty",
        "pyvider-hcl",
        "pyvider-rpcplugin",
        "provide-foundation",
        "provide-testkit",
        "flavorpack",
        "wrknv",
        "supsrc",
        "plating",
        "tofusoup",
    ]
    lines = ["# Cross-Repo Document\n"]
    for i in range(num_links):
        pkg = packages[i % len(packages)]
        if i % 4 == 0:
            lines.append(f"[{pkg} docs](../{pkg}/guide/page{i}.md)")
        elif i % 4 == 1:
            lines.append(f"[nested](/pyvider-framework/{pkg}/docs/page{i}.md)")
        elif i % 4 == 2:
            lines.append(f"[relative]({pkg}/api/ref{i}.md#method)")
        else:
            lines.append(f"[plain link](page{i}.md)")
    return "\n".join(lines)


def main() -> None:
    cycles = 300
    links_per_doc = 200

    # Warmup
    plugin = CrossRepoLinksPlugin()
    plugin.config = {"enabled": True, "verbose": False}
    doc = _build_markdown_with_crossrepo_links(links_per_doc)
    for _ in range(3):
        plugin._strip_md_extensions(doc)
        plugin._transform_package_links(doc)
        plugin._fix_nested_paths(doc)

    # Stress: N cycles
    for _ in range(cycles):
        result = doc
        result, _ = plugin._strip_md_extensions(result)
        result, _ = plugin._transform_package_links(result)
        result, _ = plugin._fix_nested_paths(result)

    print(f"crossrepo_links stress complete: {cycles} cycles x {links_per_doc} links")


if __name__ == "__main__":
    main()
