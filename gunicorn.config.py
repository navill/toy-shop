from multiprocessing import cpu_count

workers = cpu_count() * 2 + 1
max_requests = 3000
max_requests_jitter = 1500
timeout = 300
