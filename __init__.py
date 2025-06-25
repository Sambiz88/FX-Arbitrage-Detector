"""
triangular‑arbitrage‑detector package
------------------------------------

A minimal toolkit for fetching FX rates, building a log‑weighted graph,
and detecting triangular‑arbitrage cycles.
"""

from .fetcher import get_rates            # convenience re‑export
from .graph   import build_graph, find_arbitrage_cycle

__all__ = [
    "get_rates",
    "build_graph",
    "find_arbitrage_cycle",
]

__version__ = "0.1.0"
