import datetime
import logging
from django.utils.deprecation import MiddlewareMixin


logging.basicConfig(filename="requests.log", level=logging.INFO, format="%(message)s")


class RequestLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user = request.user if request.user.is_authenticated else "Not know"
        log_entry = f"{datetime.datetime.now()} - User: {user} - Path: {request.path}"
        logging.info(log_entry)
