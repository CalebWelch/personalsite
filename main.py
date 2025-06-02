import logging
import os
import traceback
import uuid
from s3_functions import upload_to_s3
from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
    jsonify,
)
from admin_uploader import admin_required
from werkzeug.utils import secure_filename
import secrets
import boto3

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
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


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "pass":
            session["is_admin"] = True
            flash("logged in", "success")
            return redirect(url_for("upload_page"))
        else:
            flash("Invalid credentials", "error")
    return render_template("admin_login.html")


@app.route("/admin/upload", methods=["GET", "POST"])
@admin_required
def upload_page():
    if request.method == "POST":
        if "video_file" not in request.files:
            flash("no file selected", "error")
            return redirect(request.url)
        file = request.files["video_file"]
        if file.filename == "":
            flash("no file selected", "error")
            return redirect(request.url)

        if file:
            filename = secure_filename(file.filename)
            artist = request.form.get('Artist', '').strip()
            title = request.form.get('Title', '').strip()

            metadata = {
                "x-amz-meta-artist": artist,
                "x-amz-meta-title": title
            }
            file_extension = filename.rsplit(".", 1)[1].lower()
            unique_filename = f"{uuid.uuid4()}.{file_extension}"
            folder_prefex = request.form.get("folder", "").strip()
            if folder_prefex:
                s3_key = f"{secure_filename(folder_prefex)}/{unique_filename}"
            else:
                s3_key = unique_filename
            if upload_to_s3(file, BUCKET, s3_key, metadata):
                flash(f"Video uploaded as {s3_key}", "success")
            else:
                flash("error uploading to s3", "error")
        else:
            flash("Invalid file type", "error")
    return render_template("upload_page.html")


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
            videos = local_videos

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
