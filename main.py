import os
import traceback
from flask import Flask, render_template, url_for, jsonify
import boto3

app = Flask(__name__)
app.config["VIDEO_FOLDER"] = os.path.join('static', 'videos')
BUCKET = "visuals-images"

VIDEOS = [
    {"id": 1, "title": "Space Laces - This Way", "filename": "thisway.mp4"},
    {"id": 2, "title": "Skrillex, Hamdi, TAICHU & OFFAIAH - Push (Aero Soul Flip)", "filename": "push.mp4"},
    {"id": 3, "title": "Cure97 - Darkside", "filename": "darkside.mp4"},
    {"id": 4, "title": "Vier - Control", "filename": "control.mp4"},
    {"id": 5, "title": "Silcrow - Take Me Down (VIP)", "filename": "silcrow.mp4"}
]

@app.route('/debug')
def debug():
    """Debug endpoint to check if the app is working"""
    return jsonify({
        "status": "ok",
        "app_running": True,
        "template_dir_exists": os.path.isdir("templates"),
        "static_dir_exists": os.path.isdir("static"),
        "videos_dir_exists": os.path.isdir(app.config["VIDEO_FOLDER"]),
        "cwd": os.getcwd(),
        "user": os.getenv("USER"),
        "s3_functions_exists": os.path.isfile("s3_functions.py")
    })

@app.route('/ping')
def ping():
    """Simple ping endpoint"""
    return "pong"

@app.route('/')
def index():
    try:
        # Import s3_functions only when needed to avoid startup errors
        from s3_functions import show_image
        
        videos = VIDEOS
        video_data = []
        headerImage = url_for("static", filename="logo_actual_white.jpg")
        
        try:
            contents = show_image(BUCKET)
            for v in contents:
                video_data.append({
                    "title": "test",
                    'url': v
                })
        except Exception as e:
            # Handle S3 errors gracefully
            app.logger.error(f"S3 error: {e}")
            app.logger.error(traceback.format_exc())
            video_data = [{"title": "Error loading videos", "url": "#"}]
            
        return render_template('artist_spa.html', videos=video_data, logo=headerImage)

    except Exception as e:
        # Return detailed error for debugging
        error_details = {
            "error": str(e),
            "traceback": traceback.format_exc()
        }
        app.logger.error(f"Error in index route: {e}")
        app.logger.error(traceback.format_exc())
        return jsonify(error_details), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
