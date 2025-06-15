from rest_framework.pagination import PageNumberPagination


class MessagePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        return {
            "count": self.page.paginator.count,
            "result": data,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
        }
