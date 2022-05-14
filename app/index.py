from flask import Flask, jsonify, request, make_response
from pydub import AudioSegment, exceptions
from io import BytesIO
from PIL import Image

app = Flask(__name__)

# mp3ファイルからアートワークを取得する
def extractCoverMp3(file):
    from mutagen.id3 import ID3
    tags = ID3(file)
    apic = tags.get("APIC:")
    if apic is not None:
        return Image.open(BytesIO(apic.data))

# alacファイルからアートワークを取得する
def extractCoverAlac(file):
    from mutagen.mp4 import MP4
    metadata = MP4(file)
    cover = metadata["covr"]
    return Image.open(BytesIO(cover[0]))

@app.route('/init/getAlbumArtwork', methods = ['POST'])
def getAlbumArtwork():
    if 'file' not in request.files:
        return jsonify({"message": "No file part included in the request"}), 400
    if 'album' not in request.form:
        return jsonify({"message": "No album title included in the request"}), 400
    if 'extension' not in request.form:
        return jsonify({"message": "No track type included in the request"}), 400

    track = request.files['file']
    album = request.form['album']
    extension = request.form['extension']

    # ファイルのタイプに応じて画像取得メソッドを変更する
    artwork = None
    if extension == "mp3":
        artwork = extractCoverMp3(track)
    elif extension == "m4a":
        artwork = extractCoverAlac(track)
    else:
        return jsonify({"message": f"No support file type. {extension}"}), 400

    output = BytesIO()
    artwork.save(output, format="jpeg")

    # レスポンスを生成する
    response = make_response()
    response.data = output.getvalue()
    response.headers['Content-Type'] = 'image/jpeg'
    response.headers['Content-Disposition'] = f"attachment; filename={album}.jpg"

    return response


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
