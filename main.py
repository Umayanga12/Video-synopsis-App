import flask
from bg_generator import GenerateBackground
from flask import request, jsonify
from obj_det import obj_det

app = flask.Flask(__name__)

@app.route('/generateBackImg', method = ['GET'])
async def generateback():
    videopath = request.args.get('videopath')
    await GenerateBackground(videopath)
    return jsonify({"message":"Background Image Generated"})


@app.route('detobj', method = ['GET'])
async def detectobj():
    videopath = request.args.get('videopath')
    await obj_det(videopath)
    return jsonify({"message":"Object Detection Completed"})
    
if __name__ == "__main__":
    app.run(debug=True,port=6700)