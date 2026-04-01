from flask import Flask, request
from app.logger import log_event, configure_logging
from app.utils import get_request_metadata
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
app.logger = configure_logging()
metrics = PrometheusMetrics(app)

@app.route('/health-check')
def health_check():
    metadata = get_request_metadata()
    log_event(app.logger, "info", "health-check-success", **metadata)
    return "<h1>Hello, I'm Alive!</h1>"

@app.route('/hello')
def hello():
    name = request.args.get("name")
    metadata = get_request_metadata()

    if not name:
        log_event(app.logger, "error", "hello-error", **metadata, error_message="Nome não informado")
        return "Nome não informado", 400
    else:
        log_event(app.logger, "info", "hello-success", **metadata, nome=name)
        return f"Hello, {name}!"

if __name__ == "__main__": # pragma: no cover
    #app.run(debug=True)
    app.run(host='0.0.0.0')