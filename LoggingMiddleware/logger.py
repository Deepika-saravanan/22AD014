import time
from flask import request, jsonify

logs = []

def log_request(app):
    @app.before_request
    def start_timer():
        from flask import g
        g.start = time.time()

    @app.after_request
    def log_response(response):
        from flask import g
        duration = round(time.time() - g.start, 4)
        log_line = {
            "method": request.method,
            "path": request.path,
            "status": response.status_code,
            "duration": f"{duration}s"
        }
        logs.append(log_line)
        with open("request_logs.txt", "a") as f:
            f.write(f"{log_line}\n")
        return response

    @app.route("/logs", methods=["GET"])
    def get_logs():
        return jsonify(logs), 200