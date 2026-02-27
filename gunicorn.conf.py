# Gunicorn configuration file
import multiprocessing

# Bind to 0.0.0.0:8000
bind = "0.0.0.0:8000"

# Number of workers (2-4 x CPU cores)
workers = multiprocessing.cpu_count() * 2 + 1

# Worker class
worker_class = "sync"

# Timeout for workers
timeout = 120

# Keep alive connections
keepalive = 5

# Max requests per worker before restart (prevents memory leaks)
max_requests = 1000
max_requests_jitter = 100

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Process naming
proc_name = "library_project"

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190
