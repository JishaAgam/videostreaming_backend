from flask import Blueprint, Flask,jsonify,Response, render_template, request, flash, redirect, url_for, session, current_app
from werkzeug.utils import secure_filename
import os

video_blueprint = Blueprint('video', __name__)
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'videos/'

@video_blueprint.route('/upload', methods=['POST'])
def phone_verification():
    try:
        video = request.files['video']  
        filename = secure_filename(video.filename)
        video.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return {'message': 'Video uploaded successfully', 'url': f'/videos/{filename}'}
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
