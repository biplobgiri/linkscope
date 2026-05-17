from prometheus_client import Counter, Histogram, Gauge

total_clicks=Counter(
    "linkscope_total_clicks",
    "Total number of link clicks",
    ["slug"]
)

cache_hits=Counter(
    "linkscope_cache_hits",
    "Number of Redis cache hits on redirect"
)

cache_misses=Counter(
    "linkscope_cache_misses",
    "Number of Redis cache misses on redirect"
)

links_created=Counter(
    "linkscope_links_created",
    "Total number of short links created"
)

expired_link_hits=Counter(
    "linkscope_expired_link_hits",
    "Number of hits on expired or inactive links"
)

active_links=Gauge(
    "linkscope_active_links",
    "Current number of active links in the system"
)

redirect_latency=Histogram(
    "linkscope_redirect_latency_seconds",
    "Time taken to process a redirect",
    buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5]
)