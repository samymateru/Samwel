from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime, timedelta

from starlette.responses import JSONResponse


class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int = 5, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window = timedelta(seconds=window_seconds)
        self.requests = {}  # key: ip+path -> list of request times

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        endpoint = request.url.path
        key = f"{client_ip}:{endpoint}"

        now = datetime.now()
        request_times = self.requests.get(key, [])

        # Filter timestamps within the current window
        request_times = [t for t in request_times if now - t < self.window]
        request_times.append(now)
        self.requests[key] = request_times

        if len(request_times) > self.max_requests:
            return JSONResponse(
                status_code=429,
                content={"detail": f"Rate limit exceeded for {endpoint}. Try again later."}
            )

        return await call_next(request)


