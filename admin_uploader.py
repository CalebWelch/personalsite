import ffmpeg
from flask import Flask, session, flash, redirect, url_for
from functools import wraps
from botocore.client import ClientError
from ffmpeg import FFmpeg, Progress
import os


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("is_admin"):
            flash("Admin access required", "error")
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)

    return decorated_function


def reduce_size(path: str):
    ffm = (
        FFmpeg()
        .option("y")
        .input(path)
        .output(f"{path}_reduced.mp4", VideoScale="0.75", VideoEncodingSpeed="Medium")
    )

    @ffmpeg.on("progress")
    def on_progress(progress: Progress):
        print(progress)

    ffm.execute()
