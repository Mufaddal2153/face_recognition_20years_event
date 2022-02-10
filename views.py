from flask import render_template, request, url_for, Response
from config import face
from camera import Video


def gen(camera):
    while True:
        img= camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-type:   image/jpg\r\n\r\n'+img +
              b'\r\n\r\n')


@face.route("/video")
def video():
    return Response(gen(Video()), mimetype='multipart/x-mixed-replace; boundary=frame')


@face.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


if __name__ == "__main__":
    face.run(debug=True)
