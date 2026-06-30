from slowapi import Limiter
from slowapi.util import get_remote_address
from starlette.requests import Request

# The capstone nginx is the single trusted upstream. It is configured to set
# X-Real-IP to $remote_addr (the real client as nginx sees it) and to overwrite
# the header, so clients cannot spoof it. We deliberately do NOT trust a
# client-supplied X-Forwarded-For: nginx is the public edge, so a client could
# inject a fake first hop to dodge the per-client rate limit. The fallback to the
# direct peer covers local/dev and the test client (which sends no headers).
#
# If a CDN (e.g. Cloudflare) is ever placed in front of nginx again, add a
# cf-connecting-ip check ahead of X-Real-IP.


def client_ip(request: Request) -> str:
    ip = request.headers.get("x-real-ip")
    if ip:
        return ip.strip()
    return get_remote_address(request)


limiter = Limiter(key_func=client_ip)
