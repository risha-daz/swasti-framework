from . import blueprint
import flask
from flask import request, jsonify
from gtts import gTTS

@blueprint.route("/get_audio/")
def streamwav():
    date=str(request.args["date"])
    param=str(request.args["params"])
    val=str(request.args["val"])
    mytext = 'The ' + param +' on '+ date + " is : " + val
    print(mytext)
    language = 'en'
    myobj = gTTS(text=mytext, lang=language, slow=False)
    myobj.save("./static/audio/welcome.mp3")
    def generate():
        with open("./static/audio/welcome.mp3", "rb") as fwav:
            data = fwav.read(1024)
            while data:
                yield data
                data = fwav.read(1024)
    return flask.Response(generate(), mimetype="audio/mp3")