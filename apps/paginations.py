from rest_framework.pagination import CursorPagination
from rest_framework.response import Response


class CustomCursorPagination(CursorPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    ordering = '-created_at'

    def get_paginated_response(self, data):
        return Response({
            'next_page': self.get_next_link(),
            'previous_page': self.get_previous_link(),
            "data": data,
        })