from flask import Flask, jsonify, request, make_response
from pydub import AudioSegment, exceptions
from io import BytesIO

app = Flask(__name__)

@app.route('/convert/alac-to-flac/', methods=['POST'])
def convertAlacToFlac():
    # ファイルが含まれていない場合、エラーとして返す
    if 'file' not in request.files:
        return jsonify({"message": "No file part in the request"}), 400

    # ファイルを取得する
    alacFile = request.files['file']

    try:
        # AudioSegmentを用いてファイルを開く
        segment = AudioSegment.from_file(BytesIO(alacFile.stream.read()), "m4a")

        # メモリーにファイルをエクスポートする
        flacFile = segment.export(format="flac")

        # レスポンスを生成する
        response = make_response()
        response.data = flacFile.read()
        response.headers['Content-Type'] = 'application/octet-stream'
        response.headers['Content-Disposition'] = 'attachment; filename=output.flac'

        return response

    # m4a形式以外のファイルがpostされ、正常にコンバートできなかった場合
    except exceptions.CouldntDecodeError:
        return jsonify({"message": "Can't open this file. Should post file in m4a (Apple lossless) format."}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=14125, debug=True)
