from flask import Blueprint, Flask,jsonify,Response, render_template, request, flash, redirect, url_for, session, current_app
from werkzeug.utils import secure_filename
import os
from app.models import *

video_blueprint = Blueprint('video', __name__)
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'videos/'


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

@video_blueprint.route('/position', methods=['POST'])
def save_position():
    try:
        data = request.get_json()
        video = vidoe_space.query.filter_by(id=data['video_id']).first()
        if not video:
            return jsonify({"status": 404, "message": "video not found"}), 404 
        video_position = continue_play(**data)
        db.session.add(video_position)
        db.session.commit()
        return jsonify({"status": 200, "message": "Video continue play created successfully"})
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error: {e}",exc_info=True)
        return jsonify({"status": 500, "message": "Something went wrong"}), 500
    
@video_blueprint.route('/position_data', methods=['GET'])
def position_data():
    try:
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