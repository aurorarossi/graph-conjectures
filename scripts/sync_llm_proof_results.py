#!/usr/bin/env python3
"""Import literature resolutions found by Graph-Theory-LLM-Proofs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REPOSITORY_URL = "https://github.com/graph-theory-AI/Graph-Theory-LLM-Proofs"

DISPROVED_IDS = {
    "1407.5833__00", "1806.00825__01", "1905.12142__00",
    "2201.08204__01", "2208.06629__00", "2410.16495__00",
}

RESOLUTION_ARTICLES = {
    "0911.0885__00": ("Three-coloring triangle-free graphs on surfaces V. Coloring planar graphs with distant anomalies", "https://arxiv.org/abs/0911.0885"),
    "1302.2158__00": ("3 List Coloring Graphs of Girth at least Five on Surfaces", "https://arxiv.org/abs/1710.06898"),
    "1407.5833__00": ("Identifying codes in hereditary classes of graphs and VC-dimension", "https://arxiv.org/abs/1407.5833"),
    "1709.09050__03": ("Topological directions in Cops and Robbers", "https://arxiv.org/abs/1709.09050"),
    "1710.06282__01": ("A tight Erdős–Pósa function for planar minors", "https://arxiv.org/abs/1807.04969"),
    "1802.03727__01": ("Dense induced bipartite subgraphs in triangle-free graphs", "https://arxiv.org/abs/1810.12144"),
    "1802.03727__03": ("Dense induced bipartite subgraphs in triangle-free graphs", "https://arxiv.org/abs/1810.12144"),
    "1802.04179__01": ("Planar graphs without cycles of length 4 or 5 are (7m:2m)-DP-colorable", "https://arxiv.org/abs/2511.12914"),
    "1806.00825__01": ("Short rainbow cycles in graphs and matroids", "https://arxiv.org/abs/1806.00825"),
    "1806.09726__02": ("Bounds on Ramsey Games via Alterations", "https://arxiv.org/abs/1909.02691"),
    "1905.12142__00": ("Combinatorial anti-concentration inequalities, with applications", "https://arxiv.org/abs/1905.12142"),
    "1912.11246__02": ("Graphs with polynomially many minimal separators", "https://arxiv.org/abs/2005.05042"),
    "2001.01607__00": ("Induced subgraphs and tree decompositions XI. Local structure in even-hole-free graphs of large treewidth", "https://arxiv.org/abs/2309.04390"),
    "2006.09269__00": ("Recolouring planar graphs of girth at least five", "https://arxiv.org/abs/2112.00631"),
    "2103.17094__00": ("Weak Coloring Numbers of Intersection Graphs", "https://arxiv.org/abs/2103.17094"),
    "2105.07370__00": ("Strengthening Rödl's theorem", "https://arxiv.org/abs/2105.07370"),
    "2201.08204__01": ("Digraphs with all induced directed cycles of the same length are not dichromatically bounded", "https://arxiv.org/abs/2203.15575"),
    "2208.06629__00": ("Perfect shuffling with fewer lazy transpositions", "https://arxiv.org/abs/2208.06629"),
    "2208.06630__01": ("Short reachability networks", "https://arxiv.org/abs/2208.06630"),
    "2212.02737__00": ("Induced subgraphs and tree decompositions XIII. Basic obstructions in H-free graphs for finite H", "https://arxiv.org/abs/2311.05066"),
    "2401.06062__00": ("On prime Cayley graphs", "https://arxiv.org/abs/2401.06062"),
    "2401.06062__01": ("On prime Cayley graphs", "https://arxiv.org/abs/2401.06062"),
    "2401.06062__02": ("On prime Cayley graphs", "https://arxiv.org/abs/2401.06062"),
    "2410.13008__01": ("When all directed cycles have the same weight", "https://arxiv.org/abs/2601.12746"),
    "2410.16495__00": ("Every Graph is Essential to Large Treewidth", "https://arxiv.org/abs/2502.14775"),
}


def collect_known_resolutions(source_dir: Path) -> dict:
    attacks_dir = source_dir / "attacks"
    if not attacks_dir.is_dir():
        raise FileNotFoundError(f"attack directory not found: {attacks_dir}")
    results = []
    for verdict_path in sorted(attacks_dir.glob("*/verdict.json")):
        attack = json.loads(verdict_path.read_text(encoding="utf-8"))
        review_id = attack.get("id") or verdict_path.parent.name
        if attack.get("verdict") != "already_resolved":
            continue
        if review_id != verdict_path.parent.name:
            raise ValueError(
                f"verdict id {review_id!r} does not match {verdict_path.parent.name!r}"
            )
        article_title, article_url = RESOLUTION_ARTICLES[review_id]
        results.append({
            "id": review_id,
            "site_status": "disproved" if review_id in DISPROVED_IDS else "solved",
            "confidence": attack.get("confidence", "unknown"),
            "one_line": attack.get("one_line", ""),
            "caveats": attack.get("caveats", ""),
            "model": attack.get("model", ""),
            "assessed_at": attack.get("when", ""),
            "article_title": article_title,
            "article_url": article_url,
            "audit_url": f"{REPOSITORY_URL}/tree/main/attacks/{review_id}",
        })

    return {
        "schema_version": 2,
        "source_repository": REPOSITORY_URL,
        "disclaimer": (
            "These status corrections report results attributed to existing papers "
            "or to the final source version. Graph-Theory-LLM-Proofs located and "
            "checked the implication; it is not credited as the author of the result."
        ),
        "results": results,
    }


def main() -> int:
    project = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", type=Path,
                        default=project.parent / "Graph-Theory-LLM-Proofs")
    parser.add_argument("--output", type=Path,
                        default=project / "data" / "llm_proof_results.json")
    args = parser.parse_args()
    payload = collect_known_resolutions(args.source_dir)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"wrote {len(payload['results'])} known resolution(s) to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
