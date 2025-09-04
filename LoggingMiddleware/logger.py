import time
from flask import request

def log_request(app):
    @app.before_request
    def start_timer():
        from flask import g
        g.start = time.time()

    @app.after_request
    def log_response(response):
        from flask import g
        duration = round(time.time() - g.start, 4)
        log_line = f"{request.method} {request.path} {response.status_code} {duration}s\n"
        with open("request_logs.txt", "a") as f:
            f.write(log_line)
        return response