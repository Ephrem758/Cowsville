"""
Custom pagination classes for FarmManager API

This module provides flexible pagination options for API endpoints.
"""

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardResultsSetPagination(PageNumberPagination):
    """
    Standard pagination class with configurable page size.
    
    Default: 50 items per page
    Max: 100 items per page
    
    Clients can specify page size using ?page_size=N query parameter
    """
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 100
    
    def get_paginated_response(self, data):
        """
        Return a paginated response with metadata
        """
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'page_size': self.page_size,
            'results': data
        })


class LargeResultsSetPagination(PageNumberPagination):
    """
    Pagination for large datasets (e.g., messages, medical records)
    
    Default: 100 items per page
    Max: 500 items per page
    """
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 500


class SmallResultsSetPagination(PageNumberPagination):
    """
    Pagination for small datasets or detailed views
    
    Default: 20 items per page
    Max: 50 items per page
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 50

