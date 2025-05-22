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

app = create_app()

if __name__ == '__main__':
    from waitress import serve
    import os

    serve(app, host='0.0.0.0', port=5000)
