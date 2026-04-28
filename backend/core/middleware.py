import logging
import time

from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger("api")


class RequestLoggingMiddleware(MiddlewareMixin):
    """Logs request method, path, status, and duration for every API call."""

    def process_request(self, request):
        request._start_time = time.time()

    def process_response(self, request, response):
        duration = time.time() - getattr(request, "_start_time", time.time())
        logger.info(
            "%s %s %s %.2fms",
            request.method,
            request.get_full_path(),
            response.status_code,
            duration * 1000,
        )
        return response
