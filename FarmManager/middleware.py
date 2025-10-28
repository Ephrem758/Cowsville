"""
Custom middleware for FarmManager application

This module provides middleware for:
- Request timeout enforcement
- Query count monitoring (development)
- Performance tracking
"""

import logging
import signal
import threading
import time
from django.http import JsonResponse
from django.conf import settings
from django.db import connection

logger = logging.getLogger(__name__)


class TimeoutException(Exception):
    """Exception raised when a request times out"""
    pass


def timeout_handler(signum, frame):
    """Handler for timeout signal"""
    raise TimeoutException("Request processing timed out")


class RequestTimeoutMiddleware:
    """
    Middleware to enforce request-level timeouts.
    
    Prevents requests from running indefinitely and consuming server resources.
    Default timeout: 30 seconds (configurable via settings.REQUEST_TIMEOUT)
    
    Note: This uses signal.SIGALRM which only works on Unix-based systems.
    For Windows or production with Gunicorn, rely on server-level timeouts.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Get timeout from settings, default to 30 seconds
        self.timeout = getattr(settings, 'REQUEST_TIMEOUT', 30)
        self.enabled = getattr(settings, 'ENABLE_REQUEST_TIMEOUT', True)
    
    def __call__(self, request):
        # Only enable on Unix-based systems and main thread
        if (
            not self.enabled
            or not hasattr(signal, 'SIGALRM')
            or threading.current_thread() is not threading.main_thread()
        ):
            return self.get_response(request)
        
        # Don't timeout admin or static requests
        if request.path.startswith('/admin/') or request.path.startswith('/static/'):
            return self.get_response(request)
        
        # Set the timeout
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(self.timeout)
        
        try:
            response = self.get_response(request)
            # Cancel the alarm
            signal.alarm(0)
            return response
            
        except TimeoutException:
            # Request timed out
            signal.alarm(0)  # Cancel the alarm
            logger.error(f"Request timeout: {request.method} {request.path} exceeded {self.timeout}s")
            
            return JsonResponse({
                'error': 'Request timeout',
                'detail': f'Request took longer than {self.timeout} seconds to process',
                'status': 'timeout'
            }, status=504)  # Gateway Timeout
            
        except Exception as e:
            # Other exception - make sure to cancel alarm
            signal.alarm(0)
            raise
        
        finally:
            # Ensure alarm is always cancelled
            signal.alarm(0)


class QueryCountDebugMiddleware:
    """
    Middleware to log database query count per request.
    
    Useful for identifying endpoints with N+1 query problems.
    Only enable in development or when debugging performance issues.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Only enable if DEBUG is True or explicitly enabled
        self.enabled = getattr(settings, 'DEBUG', False) or getattr(
            settings, 'ENABLE_QUERY_COUNT_LOGGING', False
        )
        # Threshold for warning logs (default: 20 queries)
        self.warning_threshold = getattr(settings, 'QUERY_COUNT_WARNING_THRESHOLD', 20)
    
    def __call__(self, request):
        if not self.enabled:
            return self.get_response(request)
        
        # Reset query log
        if hasattr(connection, 'queries_log'):
            connection.queries_log.clear()
        
        # Track timing
        start_time = time.time()
        
        # Process request
        response = self.get_response(request)
        
        # Calculate metrics
        duration = time.time() - start_time
        query_count = len(connection.queries)
        
        # Log results
        if query_count > self.warning_threshold:
            logger.warning(
                f"HIGH QUERY COUNT: {request.method} {request.path} - "
                f"{query_count} queries in {duration:.3f}s"
            )
        else:
            logger.info(
                f"{request.method} {request.path} - "
                f"{query_count} queries in {duration:.3f}s"
            )
        
        # Add headers for debugging
        response['X-Query-Count'] = str(query_count)
        response['X-Response-Time'] = f"{duration:.3f}s"
        
        return response


class PerformanceMonitoringMiddleware:
    """
    Middleware to track request performance metrics.
    
    Logs slow requests and can be extended to send metrics to monitoring services.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Threshold for slow request warnings (default: 2 seconds)
        self.slow_threshold = getattr(settings, 'SLOW_REQUEST_THRESHOLD', 2.0)
    
    def __call__(self, request):
        start_time = time.time()
        
        # Process request
        response = self.get_response(request)
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Log slow requests
        if duration > self.slow_threshold:
            logger.warning(
                f"SLOW REQUEST: {request.method} {request.path} took {duration:.3f}s "
                f"(threshold: {self.slow_threshold}s)"
            )
        
        # Add response time header
        response['X-Response-Time'] = f"{duration:.3f}s"
        
        return response

