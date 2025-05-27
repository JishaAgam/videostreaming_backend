from flask import Flask, request

app = Flask(__name__)

#Load allowed domains from a text file
def load_allowed_domains(file_path="/home/ubuntu/domainChecker/allowed_domains.txt"):
    with open(file_path, "r") as file:
        return set(line.strip() for line in file if line.strip())

ALLOWED_DOMAINS = load_allowed_domains()

@app.route("/check-domain")
def check_domain():
    domain = request.args.get("domain", "")
    if domain in ALLOWED_DOMAINS:
        return "", 200
    return "", 403

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
