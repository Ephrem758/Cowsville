# Request Timeout Guide

## 🎯 Problem Statement

Without request timeouts, endpoints can run indefinitely, causing:
- **Server Resource Exhaustion**: Workers get stuck, can't handle new requests
- **Application Crashes**: Memory exhaustion from hanging requests
- **Poor User Experience**: No feedback when requests hang
- **Cascading Failures**: One slow request blocks others

## ✅ Solution: Multi-Layer Timeout Strategy

We've implemented **3 layers of timeout protection**:

### 1. Database Timeout (20 seconds)
- Prevents slow database queries from hanging
- Configured in `DATABASES` settings

### 2. Application Timeout (30 seconds)  
- Middleware that kills requests taking too long
- Logs timeout events for monitoring

### 3. Web Server Timeout (30 seconds)
- Gunicorn/uWSGI kills unresponsive workers
- Most important for production

---

## 📋 Implementation Details

### Layer 1: Database Timeout

**Location**: `settings.py` and `productions_settings.py`

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'CONN_MAX_AGE': 600,  # Connection pooling
        'OPTIONS': {
            'timeout': 20,  # Query timeout in seconds
        }
    }
}
```

**What it does**:
- Kills any database query taking longer than 20 seconds
- Prevents infinite loops in queries
- Returns error instead of hanging

**For MySQL/PostgreSQL**:
```python
'OPTIONS': {
    'connect_timeout': 10,  # Connection timeout
    'read_timeout': 20,     # Query read timeout (MySQL)
    'write_timeout': 20,    # Query write timeout (MySQL)
}
```

### Layer 2: Application Middleware Timeout

**Location**: `FarmManager/middleware.py`

```python
class RequestTimeoutMiddleware:
    """Enforces request-level timeouts"""
    def __init__(self, get_response):
        self.get_response = get_response
        self.timeout = 30  # 30 seconds
```

**Configuration** (`settings.py`):
```python
REQUEST_TIMEOUT = 30  # Max request duration
ENABLE_REQUEST_TIMEOUT = True  # Enable in development
SLOW_REQUEST_THRESHOLD = 2.0  # Warn about slow requests
```

**How it works**:
1. Sets a 30-second alarm for each request
2. If request exceeds 30s, raises `TimeoutException`
3. Returns HTTP 504 (Gateway Timeout) to client
4. Logs the timeout event

**Response Format**:
```json
{
    "error": "Request timeout",
    "detail": "Request took longer than 30 seconds to process",
    "status": "timeout"
}
```

**Limitations**:
- Uses `signal.SIGALRM` (Unix/Linux only, not Windows)
- **Disabled in production** (use Gunicorn timeout instead)
- Good for development and debugging

### Layer 3: Web Server Timeout (Production)

**Location**: `gunicorn_config.py`

```python
# Gunicorn Configuration
timeout = 30              # Kill workers after 30s
graceful_timeout = 30     # Time for graceful shutdown
max_requests = 1000       # Restart workers periodically
max_requests_jitter = 50  # Prevent all workers restarting at once
```

**How it works**:
1. Gunicorn monitors each worker process
2. If worker doesn't respond within 30s, it's killed
3. New worker is spawned automatically
4. Client receives 502/504 error

**Why this is better for production**:
- Works on all platforms (Windows, Linux, macOS)
- More reliable than signal-based timeouts
- Handles truly stuck workers (infinite loops)
- No impact on Django code

**Starting Gunicorn**:
```bash
gunicorn --config gunicorn_config.py \
    --timeout 30 \
    --workers 4 \
    FarmManagerSystem.wsgi:application
```

---

## 🔧 Configuration by Environment

### Development (`settings.py`):
```python
REQUEST_TIMEOUT = 30
ENABLE_REQUEST_TIMEOUT = True  # Use middleware timeout
SLOW_REQUEST_THRESHOLD = 2.0
```

### Production (`productions_settings.py`):
```python
REQUEST_TIMEOUT = 30
ENABLE_REQUEST_TIMEOUT = False  # Disable - use Gunicorn instead
SLOW_REQUEST_THRESHOLD = 1.0    # Stricter threshold
```

### Gunicorn (Production):
```python
# gunicorn_config.py
timeout = 30
graceful_timeout = 30
```

### Nginx (Optional - additional layer):
```nginx
location / {
    proxy_pass http://127.0.0.1:8000;
    proxy_connect_timeout 10s;  # Time to connect to backend
    proxy_send_timeout 30s;     # Time to send request
    proxy_read_timeout 30s;     # Time to read response
}
```

---

## 📊 Timeout Hierarchy

```
Client Request
    ↓
Nginx (30s proxy_read_timeout)
    ↓
Gunicorn (30s worker timeout)  ← Primary protection in production
    ↓
Django Middleware (30s)        ← Active in development only
    ↓
Database (20s query timeout)   ← Last line of defense
    ↓
Response or Timeout Error
```

---

## 🧪 Testing Timeouts

### Test 1: Simulate Slow Endpoint

Create a test view:
```python
# In views.py (for testing only)
from django.http import JsonResponse
import time

@api_view(['GET'])
def slow_endpoint(request):
    """Test endpoint that sleeps for 35 seconds"""
    time.sleep(35)  # Exceeds 30s timeout
    return JsonResponse({"message": "This should timeout"})
```

Test it:
```bash
curl "http://localhost:8000/api/slow-test/"
# Should return 504 Gateway Timeout after 30 seconds
```

### Test 2: Simulate Slow Database Query

```python
# In Django shell
from django.db import connection
import time

try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT *, SLEEP(25) FROM farm_manager_cow;")
        # Should timeout after 20 seconds (database timeout)
except Exception as e:
    print(f"Database timeout: {e}")
```

### Test 3: Production Timeout Test

```bash
# Test with Gunicorn
gunicorn --bind 127.0.0.1:8000 --timeout 5 --workers 2 \
    FarmManagerSystem.wsgi:application

# In another terminal
curl "http://localhost:8000/api/slow-test/"
# Should timeout after 5 seconds
```

### Test 4: Monitor Timeout Logs

```bash
# Watch logs in real-time
tail -f logs/farm_manager.log

# Look for timeout messages:
# ERROR: Request timeout: GET /api/cows/ exceeded 30s
# WARNING: SLOW REQUEST: GET /api/farms/ took 2.5s
```

---

## 🚨 Handling Timeout Errors

### In Your Frontend/Client:

```javascript
// JavaScript example
async function fetchWithTimeout(url, timeout = 30000) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);
    
    try {
        const response = await fetch(url, {
            signal: controller.signal,
            headers: {
                'Authorization': 'Basic ' + btoa('user:pass')
            }
        });
        
        clearTimeout(timeoutId);
        
        if (response.status === 504) {
            throw new Error('Server request timeout');
        }
        
        return await response.json();
        
    } catch (error) {
        if (error.name === 'AbortError') {
            throw new Error('Request timeout - took longer than 30 seconds');
        }
        throw error;
    }
}

// Usage
try {
    const data = await fetchWithTimeout('http://api/farms/');
    console.log(data);
} catch (error) {
    console.error('Request failed:', error.message);
    // Show user-friendly error message
    alert('Request timed out. Please try again or contact support.');
}
```

### In Python Client:

```python
import requests
from requests.exceptions import Timeout, RequestException

def api_call_with_timeout(url, timeout=30):
    """Make API call with timeout handling"""
    try:
        response = requests.get(
            url,
            auth=('username', 'password'),
            timeout=timeout
        )
        
        if response.status_code == 504:
            print("Server timeout - request took too long")
            return None
        
        response.raise_for_status()
        return response.json()
        
    except Timeout:
        print(f"Request timeout after {timeout} seconds")
        return None
        
    except RequestException as e:
        print(f"Request failed: {e}")
        return None

# Usage
data = api_call_with_timeout('http://localhost:8000/api/farms/')
if data:
    print(f"Got {data['count']} farms")
else:
    print("Request failed")
```

---

## 🔍 Debugging Timeout Issues

### Check Which Layer Timed Out:

1. **Database Timeout** (20s):
   ```
   Error: OperationalError: database is locked
   Error: timeout expired
   ```

2. **Middleware Timeout** (30s):
   ```
   ERROR: Request timeout: GET /api/endpoint exceeded 30s
   Response: {"error": "Request timeout", ...}
   ```

3. **Gunicorn Timeout** (30s):
   ```
   [CRITICAL] WORKER TIMEOUT (pid:12345)
   [INFO] Booting worker with pid: 12346
   ```

4. **Nginx Timeout**:
   ```
   504 Gateway Time-out
   nginx/1.18.0
   ```

### Common Causes and Solutions:

| Symptom | Cause | Solution |
|---------|-------|----------|
| All endpoints slow | Database not indexed | Add indexes, use select_related |
| Specific endpoint slow | N+1 queries | Check query count, optimize queries |
| Random timeouts | Database lock contention | Use connection pooling, optimize writes |
| Timeouts during peak | Insufficient workers | Increase Gunicorn workers |
| Memory-related timeouts | Memory leak | Set max_requests in Gunicorn |

### Enable Query Logging:

```python
# In settings.py (temporarily)
LOGGING = {
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
        }
    }
}

ENABLE_QUERY_COUNT_LOGGING = True
```

---

## 📈 Monitoring and Alerts

### Metrics to Track:

1. **Request Duration Distribution**
   - P50 (median)
   - P95 (95th percentile)
   - P99 (99th percentile)

2. **Timeout Rate**
   - Count of 504 responses
   - Percentage of total requests

3. **Slow Requests**
   - Requests > 2 seconds
   - Endpoints by average duration

4. **Worker Restarts**
   - Gunicorn worker timeout count
   - Worker restart frequency

### Set Up Alerts:

```python
# Example: Send alert on timeout
import logging

logger = logging.getLogger(__name__)

def alert_on_timeout(request_path, duration):
    """Send alert when request times out"""
    if duration > 30:
        # Send to monitoring service
        logger.critical(f"TIMEOUT ALERT: {request_path} took {duration}s")
        # Could integrate with: Sentry, DataDog, New Relic, etc.
```

---

## ✅ Best Practices

1. **Set Conservative Timeouts**
   - Start with 30s, adjust based on metrics
   - Most API requests should complete in < 1s

2. **Use Pagination**
   - Already implemented (50 items/page)
   - Prevents large dataset timeouts

3. **Optimize Queries**
   - Use select_related/prefetch_related (done)
   - Add database indexes where needed

4. **Monitor Performance**
   - Track slow requests
   - Set up alerts for timeouts

5. **Graceful Degradation**
   - Return partial data on timeout
   - Provide user-friendly error messages

6. **Background Jobs**
   - Move long-running tasks to Celery/RQ
   - Use async for I/O-bound operations

7. **Cache Expensive Operations**
   - Cache database queries (already configured)
   - Use Redis for distributed caching

---

## 🚀 Production Checklist

- [x] Database timeout configured (20s)
- [x] Middleware timeout implemented (30s)
- [x] Gunicorn timeout configured (30s)
- [x] Slow request logging enabled
- [x] Performance monitoring middleware added
- [ ] Test timeout behavior in staging
- [ ] Set up monitoring/alerts
- [ ] Document timeout handling for team
- [ ] Configure Nginx proxy timeouts (if using)
- [ ] Test with production-like load

---

## 📚 Additional Resources

- [Gunicorn Settings](https://docs.gunicorn.org/en/stable/settings.html)
- [Django Database Timeout](https://docs.djangoproject.com/en/4.1/ref/settings/#conn-max-age)
- [Nginx Timeout Configuration](https://nginx.org/en/docs/http/ngx_http_proxy_module.html)

---

**Summary**: With these 3 layers of timeout protection, your application will never hang indefinitely, preventing crashes and resource exhaustion! 🎉

