import os
from flask import Flask, render_template, url_for
app = Flask(__name__)

app.config["VIDEO_FOLDER"] = os.path.join('static','videos')

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

@app.route('/')
def index():
    videos = VIDEOS
    video_data = []
    headerImage = url_for("static", filename="logo_actual_white.jpg")
    for v in videos:
        vUrl = url_for("static", filename=f"videos/{v['filename']}")
        video_data.append({
            "title": v['title'],
            'url': vUrl
        })
    return render_template('artist_spa.html', videos=video_data, logo=headerImage)

if __name__ == '__main__':
    app.debug = True
    app.run()