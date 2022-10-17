"""
Main file
"""
# pylint: disable=import-error
# pylint: disable=missing-function-docstring
from __future__ import division, print_function

import json
import argparse
import threading
import cv2
from flask import Flask, render_template, Response
from waitress import serve
from sources.Manager import GameManager

# Initialize the Flask app
app = Flask(__name__)


def start_flask():
    serve(app, host="0.0.0.0", port=5000)


def main():
    """
    Create Manager instance and start the game
    :return: nothing
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--settings", help="json file with settings")
    parser.add_argument("--local", help="enable local video creating")
    args = parser.parse_args()
    local = args.local

    manager = None

    if args.settings:
        try:
            with open(args.settings, "r", encoding="utf-8") as file_sett:
                manager = GameManager(json.load(file_sett), local=local)

        except FileNotFoundError as error:
            print(f"Can not open settings file : {error}. Loading default settings")

        except json.decoder.JSONDecodeError as error:
            print(f"Cannot convert json to dict : {error}. Loading default settings")

    if not manager:
        manager = GameManager(local=local)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/video_feed')
    def video_feed():
        return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

    @app.route('/stats')
    def stats():
        return Response(get_stat(), mimetype='text/plain; boundary=frame')

    def gen_frames():
        while True:
            if manager:
                frame = manager.getCurrentImage()
                _, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                if frame:
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n'
                           + frame + b'\r\n')  # concat frame one by one and show result
    def get_stat():
        return manager.statistic

    manager.start()


if __name__ == "__main__":
    flask_thrd = threading.Thread(target=start_flask)
    flask_thrd.start()
    main()
