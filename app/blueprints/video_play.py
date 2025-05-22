from flask import Blueprint, Flask,jsonify,Response, render_template, request, flash, redirect, url_for, session, current_app
from werkzeug.utils import secure_filename
import os
from app.models import *
import secrets
# import dns.resolver
import subprocess


def generate_verification_token(domain):
    # Combine the domain and a random secure string
    random_string = secrets.token_hex(16)  # 32-char random hex string
    return f"{domain}-{random_string}"

 
video_blueprint = Blueprint('video', __name__)
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'videos/'

# @app.before_request
# def detect_tenant_from_header():
#     tenant = request.headers.get('X-Tenant')
#     if tenant:
#         request.tenant = tenant
#     else:
#         request.tenant = 'default'

    
# @video_blueprint.route('/upload', methods=['POST'])
# def phone_verification():
#     try:
#         video = request.files['video']  
#         filename = secure_filename(video.filename)
#         video.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         return {'message': 'Video uploaded successfully', 'url': f'/videos/{filename}'}
#     except Exception as e:  
#         current_app.logger.error(f"Error: {e}")
#         return jsonify({"status":500,"message": str(e)})

@video_blueprint.route('/upload', methods=['POST'])
def video_upload():
    try:
        data = request.form.to_dict()
        video = request.files.get('video')
        video_name = secure_filename(video.filename)
        thumbnail_img = request.files.get('thumbnail_img')
        thumbnail_name = secure_filename(thumbnail_img.filename)
        video.save(os.path.join(app.config['UPLOAD_FOLDER'], video_name))
        thumbnail_img.save(os.path.join(app.config['UPLOAD_FOLDER'], thumbnail_name))
        video_stream = vidoe_space(
            video_name=video_name,
            thumbnail_img=thumbnail_name,
            vidoe_title=data['vidoe_title']
        )
        db.session.add(video_stream)
        db.session.commit()
        return {
            'message': 'Video uploaded successfully',
            'video_url': f'/videos/{video_name}',
            'thumbnail_url': f'/thumbnails/{thumbnail_name}'
        }
    except Exception as e:  
        current_app.logger.error(f"Error: {e}")
        return jsonify({"status":500,"message": str(e)})
    
@video_blueprint.route('/data', methods=['GET'])
def video_data():
    try:
        video_data = db.session.query(
            vidoe_space.id,
            vidoe_space.video_name,
            vidoe_space.thumbnail_img,
            vidoe_space.vidoe_title
        )
        video_detail_data = [row._asdict() for row in video_data.all()]
        return jsonify({"status":200,"message": "Video Data","data":video_detail_data})
    except Exception as e:  
        current_app.logger.error(f"Error: {e}")
        return jsonify({"status":500,"message": str(e)})
    
@video_blueprint.route('/stream_vid/<filename>', methods=['GET'])
def stream_video(filename):
    def generate():
        with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), "rb") as f:
            chunk = f.read(1024*1024)
            while chunk:
                yield chunk
                chunk = f.read(1024*1024)

    return Response(generate(), mimetype="video/mp4")

# @video_blueprint.route('/position', methods=['POST'])
# def save_position():
#     try:
#         tenant = getattr(request, 'tenant', 'main')
#         data = request.get_json()
#         video = vidoe_space.query.filter_by(id=data['video_id']).first()
#         if not video:
#             return jsonify({"status": 404, "message": "video not found"}), 404 
#         video_position = continue_play(**data)
#         db.session.add(video_position)
#         db.session.commit()
#         return jsonify({"status": 200, "message": "Video continue play created successfully"})
#     except Exception as e:
#         db.session.rollback()
#         current_app.logger.error(f"Error: {e}",exc_info=True)
#         return jsonify({"status": 500, "message": "Something went wrong"}), 500
    
@video_blueprint.route('/position_data', methods=['GET'])
def position_data():
    try:
        # tenant = getattr(request, 'tenant', 'main')
        # print(tenant,"???????????????????")
        save_position_data = db.session.query(
            continue_play.id,
            continue_play.position,
            continue_play.video_id,
            vidoe_space.video_name,
            vidoe_space.vidoe_title,
            vidoe_space.thumbnail_img
        ).join(vidoe_space,continue_play.video_id == vidoe_space.id).all()
        video_data = [row._asdict() for row in save_position_data]
        return jsonify({"status":200,"message": "property Data","data":video_data})
    except Exception as e:
        current_app.logger.error(f"Error: {e}",exc_info=True)
        return jsonify({"status": 500, "message": "Something went wrong"}), 500
    

# @video_blueprint.route('/add-domain', methods=['POST'])
# def add_domain():
#     domain = request.json.get('domain')
#     if not domain:
#         return jsonify({"error": "Domain required"}), 400

#     # 1. Write NGINX config
#     nginx_config = f"""
#         server {{
#             listen 80;
#             server_name {domain};
#             root /var/www/ac.zxy.com;
#         index index.html;

#             location / {{
#                 proxy_pass http://127.0.0.1:5000; 
#             }}
#         }}
#         """
#     config_path = f"/etc/nginx/sites-available/{domain}.conf"
#     with open(config_path, 'w') as f:
#         f.write(nginx_config)

#     # 2. Enable site
#     subprocess.run(["ln", "-s", config_path, f"/etc/nginx/sites-enabled/{domain}.conf"], check=True)

#     # 3. Test and reload NGINX
#     subprocess.run(["nginx", "-t"], check=True)
#     subprocess.run(["systemctl", "reload", "nginx"], check=True)
 
#     # 4. Run Certbot for SSL
#     subprocess.run(["certbot", "--nginx", "-d", domain, "--non-interactive", "--agree-tos", "-m", "admin@example.com"], check=True)

#     return jsonify({"message": f"{domain} added with SSL"}), 200

# UPLOAD_BASE = '/etc/nginx/ssl/custom_domains'
# NGINX_CONFIG_BASE = '/etc/nginx/sites-available/ecpil.com.conf'

# @video_blueprint.route('/upload-ssl', methods=['POST'])
# def upload_ssl():
#     try:
#         domain = request.form.get('domain')
#         cert = request.files.get('cert')
#         key = request.files.get('key')

#         if not domain or not cert or not key:
#             return {'error': 'domain, cert, and key are required'}, 400

#         # Create domain-specific folder
#         domain_folder = os.path.join(UPLOAD_BASE, domain)
#         os.makedirs(domain_folder, exist_ok=True)

#         cert_path = os.path.join(domain_folder, 'cert.crt')
#         key_path = os.path.join(domain_folder, 'key.key')
#         cert.save(cert_path)
#         key.save(key_path)

#         # Create Nginx config
#         nginx_config = f"""
#     server {{
#         listen 443 ssl;
#         server_name {domain};

#         ssl_certificate     {cert_path};
#         ssl_certificate_key {key_path};

#         root /var/www/react-app/build;
#         index index.html;
#         location / {{
#         try_files $uri /index.html;
#         }}
#     }}
#     """

#         with open(NGINX_CONFIG_BASE, 'a') as f:
#             f.write('\n' + nginx_config + '\n')

#         # # Enable site
#         # enabled_path = f"/etc/nginx/sites-enabled/{domain}.conf"
#         # subprocess.run(["ln", "-sf", nginx_config_path, enabled_path])

#         # Reload Nginx
#         result = subprocess.run(["nginx", "-t"], capture_output=True)
#         if result.returncode != 0:
#             return {'error': 'Nginx config test failed', 'output': result.stderr.decode()}, 500

#         subprocess.run(["systemctl", "reload", "nginx"])
     

#         # return {'message': f'SSL configured for {domain}'}, 200
#         return jsonify({"status":200,"message": f'SSL configured for {domain}'})
#     except Exception as e:
#         current_app.logger.error(f"Error: {e}",exc_info=True)
#         return jsonify({"status": 500, "message": "Something went wrong"}), 500


 


# @video_blueprint.route('/upload-ssl', methods=['POST'])
# def upload_ssl():
#     domain = request.form.get('domain')
#     cert = request.files.get('cert')
#     key = request.files.get('key')

#     if not all([domain, cert, key]):
#         return jsonify({"error": "Missing required fields"}), 400

#     safe_domain = domain.replace('.', '_')  # optional safety
#     ssl_dir = f"/etc/ssl/{domain}"
#     conf_dir = "/etc/nginx/stream-conf.d"
#     cert_path = os.path.join(ssl_dir, "fullchain.pem")
#     key_path = os.path.join(ssl_dir, "privkey.pem")
#     socket_path = f"/var/run/sockets/{domain}.sock"
#     conf_path = os.path.join(conf_dir, f"{domain}.conf")

#     try:
#         # 1. Create SSL folder and save cert/key
#         os.makedirs(ssl_dir, exist_ok=True)
#         cert.save(cert_path)
#         key.save(key_path)
#         os.chmod(cert_path, 0o600)
#         os.chmod(key_path, 0o600)

#         # 2. Create NGINX config
#         nginx_conf = f"""
#             server {{
#                 listen 443 ssl;

#                 ssl_certificate {cert_path};
#                 ssl_certificate_key {key_path};

#                 proxy_pass http://unix:{socket_path};
#             }}
#             """

#         os.makedirs(conf_dir, exist_ok=True)
#         with open(conf_path, "w") as f:
#             f.write(nginx_conf.strip())

#         # 3. Optional: Reload NGINX
#         # reload_status = os.system("nginx -t && systemctl reload nginx")

#         # if reload_status != 0:
#         #     return jsonify({"error": "NGINX config failed test or reload"}), 500

#         return jsonify({"message": f"SSL and config added for {domain}"}), 200

#     except PermissionError:
#         return jsonify({"error": "Permission denied writing to system folders"}), 500
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

from app.sockets import start_socket_for_domain

UPLOAD_BASE = "/etc/ssl"

# You may store a base port value to increment from
NEXT_PORT_FILE = "/etc/ssl/next_port.txt"

def get_next_port():
    if not os.path.exists(NEXT_PORT_FILE):
        with open(NEXT_PORT_FILE, 'w') as f:
            f.write("3002")

    with open(NEXT_PORT_FILE, 'r') as f:
        port = int(f.read().strip())

    with open(NEXT_PORT_FILE, 'w') as f:
        f.write(str(port + 1))
    
    return port

@video_blueprint.route('/upload-ssl', methods=['POST'])
def upload_ssl():
    try:
        domain = request.form.get('domain')
        cert = request.files.get('cert')
        key = request.files.get('key')

        # if not domain or not cert or not key:
        #     return jsonify({"error": "Missing domain, cert, or key"}), 400

        domain_dir = os.path.join(UPLOAD_BASE, domain)
        os.makedirs(domain_dir, exist_ok=True)

        cert_path = os.path.join(domain_dir, "fullchain.pem")
        key_path = os.path.join(domain_dir, "privkey.pem")

        cert.save(cert_path)
        key.save(key_path)

        # Get next available port for this domain
        port = get_next_port()

        # Start the socket server on that port
        start_socket_for_domain(domain, port)

        return jsonify({
            "message": f"SSL uploaded and socket started for {domain}",
            "port": port
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

