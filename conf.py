# pylint: skip-file
import os
import ast
import multiprocessing

# Gunicorn config variables
loglevel = "info"
errorlog = "-"  # stderr
accesslog = "-"  # stdout
worker_tmp_dir = "/dev/shm"
graceful_timeout = 120
timeout = 120
keepalive = 3
host = "0.0.0.0"
port = "8080"

bind = f"{host}:{port}"

worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
threads = 400

preload_app = True
workers = ast.literal_eval(os.environ.get("WORKERS", f"{multiprocessing.cpu_count() * 2 + 1}"))