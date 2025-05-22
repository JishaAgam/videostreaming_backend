# from app import create_app

# # Create app instance
# app = create_app()

# @app.route("/")
# def hello():
#     return "<h1 style='color:blue'>Hello There!</h1>"
 
# if __name__ == '__main__':
#     app.run(host="0.0.0.0", port=5000, debug=True)

# run.py
from app import create_app
from app.sockets import start_socket_for_domain

# Optional: start sockets for pre-registered domains
# e.g., from a database or static list
initial_domains = {
    'urpiq.com': 3000,
}

# 1. Create Flask app
app = create_app()

# 2. Optionally start predefined socket servers
for domain, port in initial_domains.items():
    start_socket_for_domain(domain, port)

# 3. Run with Waitress
if __name__ == '__main__':
    from waitress import serve
    import os

    # Serve Flask app on a public port (e.g., 5000)
    serve(app, host='0.0.0.0', port=5000)

    # Or serve on a Unix socket (optional)
    # sock_path = "/var/run/sockets/flask.sock"
    # if os.path.exists(sock_path):
    #     os.remove(sock_path)
    # serve(app, unix_socket=sock_path)

