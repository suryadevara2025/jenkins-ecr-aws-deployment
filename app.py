import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    version = os.getenv("APP_VERSION", "Local")

    return f"""
    <html>
        <head>
            <title>DevOps CI/CD Project</title>
        </head>
        <body>
            <h1>Welcome to My AWS ECR Project!</h1>
            <h2>Jenkins + Docker + GitHub + AWS</h2>
            <h3>Deployment Version: {version}</h3>
            <p>Application deployed successfully.</p>
        </body>
    </html>
    """

@app.route("/health")
def health():
    return jsonify(status="healthy"), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
