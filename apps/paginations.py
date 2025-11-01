from rest_framework.pagination import CursorPagination
from rest_framework.response import Response


class CustomCursorPagination(CursorPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    ordering = '-created_at'

    def get_paginated_response(self, data):
        # total = self.

        return Response({
            # 'total page': total,
            'next page': self.get_next_link(),
            'previous page' : self.get_previous_link(),
            "data" :data,
        })