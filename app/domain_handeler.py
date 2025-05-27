from flask import Flask, request, render_template_string, abort
 
app = Flask(__name__)

# Load allowed domains from file
# def load_allowed_domains(file_path="/home/ubuntu/domainChecker/allowed_domains.txt"):
#     with open(file_path, "r") as f:
#         return set(line.strip() for line in f if line.strip())

# ALLOWED_DOMAINS = load_allowed_domains()


@app.route('/')
def index():
    domain = request.host.split(":")[0]  # Remove port if present
    file_path="/home/ubuntu/domainChecker/allowed_domains.txt"
    with open(file_path, "r") as f:
        ALLOWED_DOMAINS = set(line.strip() for line in f if line.strip())
    print(ALLOWED_DOMAINS,"???????????????")
    if domain not in ALLOWED_DOMAINS:
        abort(403)
 
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Welcome to {domain}</title>
    </head>
    <body style="font-family:sans-serif;text-align:center;padding:50px;">
        <h1>Hello from <strong>{domain}</strong>!</h1>
        <p>This page is served via Flask on port 3000.</p>
    </body>
    </html>
    """
    return render_template_string(html)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)

