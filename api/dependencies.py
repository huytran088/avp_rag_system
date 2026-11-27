import logging
import os

from slowapi import Limiter
from slowapi.util import get_remote_address
from starlette.requests import Request

logger = logging.getLogger(__name__)

# Where the rate limiter gets the client's address. Only trust a header that
# the deployment's own proxy sets: otherwise a client can send it and get a
# fresh limit per request. RATE_LIMIT_IP_SOURCE picks one:
#
# - "x-real-ip" (default): the capstone nginx is the single trusted upstream.
#   It sets X-Real-IP to $remote_addr and overwrites any client value.
# - "x-forwarded-for": HF Spaces. Its proxy appends the address it saw, so the
#   entries a client can forge are on the left. Use the FORWARDED_TRUSTED_HOPS-th
#   entry from the right (default 1: the one HF's proxy appended).
# - "peer": the socket address only (direct exposure, local dev).
#
# Every source falls back to the socket peer when its header is missing (local
# dev and the test client). If a CDN (e.g. Cloudflare) is put in front of
# nginx again, add a cf-connecting-ip source.
SOURCES = ("x-real-ip", "x-forwarded-for", "peer")

# Log the X-Forwarded-For shape (entry count, never addresses) once, so the
# hop count can be checked in the deployment's logs
_logged_forwarded_shape = False


def _forwarded_client(request: Request) -> str | None:
    global _logged_forwarded_shape
    header = request.headers.get("x-forwarded-for")
    entries = [e.strip() for e in (header or "").split(",") if e.strip()]
    if not entries:
        return None

    hops = max(int(os.environ.get("FORWARDED_TRUSTED_HOPS", "1")), 1)
    if not _logged_forwarded_shape:
        _logged_forwarded_shape = True
        logger.info(
            "Rate limit key: X-Forwarded-For has %d entries; using entry %d from the right",
            len(entries),
            hops,
        )
    return entries[max(len(entries) - hops, 0)]


def client_ip(request: Request) -> str:
    source = os.environ.get("RATE_LIMIT_IP_SOURCE", "x-real-ip").strip().lower()
    if source not in SOURCES:
        raise ValueError(f"RATE_LIMIT_IP_SOURCE must be one of {SOURCES}, not {source!r}")

    if source == "x-real-ip":
        ip = request.headers.get("x-real-ip")
        if ip and ip.strip():
            return ip.strip()
    elif source == "x-forwarded-for":
        ip = _forwarded_client(request)
        if ip:
            return ip
    return get_remote_address(request)


limiter = Limiter(key_func=client_ip)
