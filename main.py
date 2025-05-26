import logging
import os
import traceback
from flask import Flask, render_template, url_for, jsonify
import boto3

app = Flask(__name__)
logger = logging.getLogger(__name__)
app.config["VIDEO_FOLDER"] = os.path.join("static", "videos")
BUCKET = "visuals-images"



@app.route("/debug")
def debug():
    """Debug endpoint to check if the app is working"""
    return jsonify(
        {
            "status": "ok yes",
            "app_running": True,
            "template_dir_exists": os.path.isdir("templates"),
            "static_dir_exists": os.path.isdir("static"),
            "videos_dir_exists": os.path.isdir(app.config["VIDEO_FOLDER"]),
            "cwd": os.getcwd(),
            "user": os.getenv("USER"),
            "s3_functions_exists": os.path.isfile("s3_functions.py"),
        }
    )

@app.route("/")
def index():
    try:
        # Import s3_functions only when needed to avoid startup errors
        from s3_functions import list_videos

        local_videos = []
        videos = list_videos(BUCKET)

        if videos:
            app.logger.info("Grabbed videos with length {0}".format(len(videos)))
        else:
            # Fall back to local videos if S3 returns empty
            app.logger.warning("S3 returned empty contents, using local videos")
            videos= local_videos

    except Exception as e:
        app.logger(e)
    try:
        # Log that we're entering the index route
        app.logger.info("Entering index route")

        # Check if template exists
        if not os.path.exists(os.path.join("templates", "artist_spa.html")):
            app.logger.error("Template file not found")
            return "Template file not found", 404

        # Try to get header image
        try:
            headerImage = url_for("static", filename="logo_actual_white.jpg")
            app.logger.info(f"Logo URL: {headerImage}")
        except Exception as e:
            app.logger.error(f"Error getting logo URL: {e}")
            headerImage = "#"  # Fallback

        # Try rendering template
        app.logger.info("Attempting to render template")
        return render_template("artist_spa.html", logo=headerImage, videos=videos)
    except Exception as e:
        # Return detailed error for debugging
        error_details = {"error": str(e), "traceback": traceback.format_exc()}
        app.logger.error(f"Error in index route: {e}")
        app.logger.error(traceback.format_exc())
        return jsonify(error_details), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
