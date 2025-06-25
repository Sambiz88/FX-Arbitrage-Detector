import math
from typing import Dict, List, Tuple

# -----------------------------------------------------------------------------
# Graph Construction
# -----------------------------------------------------------------------------

def build_graph(rates: Dict[str, float]) -> Dict[str, object]:
    """Return a log‑weighted complete directed graph derived from a single
    base‑quoted rate table.

    Args:
        rates: Mapping {currency: rate} where *rate* is the price of 1
               BASE currency in *currency* units. One of the entries must have
               value 1, indicating the *base* currency used by the provider.

    Returns:
        dict with keys:
            vertices: List[str]                   # all currency codes
            edges:    Dict[(str,str), float]      # weight = -ln(rate)
            base:     str                         # detected base currency
    """
    # --- Detect the base currency (rate == 1) ---------------------------------
    try:
        base_currency = next(k for k, v in rates.items() if v == 1)
    except StopIteration:
        raise ValueError("No base currency (rate == 1) found in rates table")

    currencies: List[str] = list(rates.keys())
    edges: Dict[Tuple[str, str], float] = {}

    # --- Fill a complete graph of synthetic cross‑rates -----------------------
    for u in currencies:
        for v in currencies:
            if u == v:
                continue

            # Compute u→v effective rate using the single‑base table
            if u == base_currency:
                rate = rates[v]                         # BASE → v
            elif v == base_currency:
                rate = 1.0 / rates[u]                   # u → BASE
            else:
                rate = rates[v] / rates[u]              # u → BASE → v

            # Convert to log‑space weight
            edges[(u, v)] = -math.log(rate)

    return {
        "vertices": currencies,
        "edges": edges,
        "base": base_currency,
    }

# -----------------------------------------------------------------------------
# Bellman–Ford‑based Arbitrage Detection
# -----------------------------------------------------------------------------

def find_arbitrage_cycle(graph: Dict[str, object], start: str | None = None) -> List[str] | None:
    """Bellman–Ford negative‑cycle detector.

    Args:
        graph: Output of :func:`build_graph`.
        start: Optional starting vertex. If *None*, a dummy super‑source is
               used; otherwise Bellman–Ford is rooted at *start*.

    Returns:
        List of vertices forming an arbitrage cycle in order (e.g.
        ["USD", "EUR", "JPY"]). Returns *None* if no such cycle exists.
    """
    vertices: List[str] = graph["vertices"]
    edges: Dict[Tuple[str, str], float] = graph["edges"]

    # ---------------------------------------------------------------------
    # Add a dummy source that connects to every vertex with zero weight so
    # we can detect a cycle regardless of chosen start.
    # ---------------------------------------------------------------------
    super_source = "__SRC__"
    all_vertices = vertices + [super_source]

    dist = {v: float("inf") for v in all_vertices}
    pred = {v: None for v in all_vertices}
    dist[super_source] = 0.0

    # Edges including super‑source
    all_edges = list(edges.items()) + [((super_source, v), 0.0) for v in vertices]

    # |V| - 1 relaxation passes
    for _ in range(len(all_vertices) - 1):
        updated = False
        for (u, v), w in all_edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                pred[v] = u
                updated = True
        if not updated:
            break  # early exit

    # One more pass to look for a tighter relaxation => negative cycle exists
    for (u, v), w in all_edges:
        if dist[u] + w < dist[v]:
            # Found a vertex *v* that is part of, or reachable to, a neg cycle
            # Walk predecessors |V| times to guarantee landing inside the cycle
            x = v
            for _ in range(len(all_vertices)):
                x = pred[x]

            # Recover the cycle
            cycle = [x]
            y = pred[x]
            while y != x and y not in cycle:
                cycle.append(y)
                y = pred[y]
            cycle.append(x)
            cycle.reverse()

            # Remove the super‑source if somehow included
            cycle = [c for c in cycle if c != super_source]
            return cycle

    return None
