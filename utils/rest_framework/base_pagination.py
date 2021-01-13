from rest_framework import pagination
from rest_framework.response import Response
from collections import OrderedDict

class NewPagination(pagination.PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'size'
    max_page_size = 30  # 最大限制

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('code', 2000),
            ('count', self.page.paginator.count),
            ('data', data)
        ]))

