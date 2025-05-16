import os
from s3_functions import show_image
from flask import Flask, render_template, url_for
import boto3
app = Flask(__name__)

app.config["VIDEO_FOLDER"] = os.path.join('static','videos')

BUCKET = "visuals-images"
VIDEOS = [
    {
        "id": 1,
        "title": "Space Laces - This Way",
        "filename": "thisway.mp4"
    },
    {
        "id": 2,
        "title": "Skrillex, Hamdi, TAICHU & OFFAIAH - Push (Aero Soul Flip)",
        "filename": "push.mp4"
    },
    {
        "id": 3,
        "title": "Cure97 - Darkside",
        "filename": "darkside.mp4"
    },
    {
        "id": 5,
        "title": "Vier - Control",
        "filename": "control.mp4"
    },
    {
        "id": 4,
        "title": "Silcrow - Take Me Down (VIP)",
        "filename": "silcrow.mp4"
    }
]

def grab_videos(bucket):
    s3_client = boto3.client("s3")

def list_files(bucket):
    s3 = boto3.client("s3")
    contents = []
    for item in s3.list_objects(bucket)['Contents']:
        contents.append(item)
    return contents

@app.route('/')
def index():
    videos = VIDEOS
    video_data = []

    headerImage = url_for("static", filename="logo_actual_white.jpg")
    contents = show_image(BUCKET)
    for v in contents:
        video_data.append({
            "title": "test",
            'url': v
        })

    return render_template('artist_spa.html', videos=video_data, logo=headerImage)

if __name__ == '__main__':
    app.run(debug=True)