from flask import Flask, request, jsonify
import boto3
from dotenv import load_dotenv
import os

load_dotenv()

aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
region = os.getenv("REGION")

app = Flask(__name__)

# Fungsi untuk melakukan analisis wajah dengan AWS Rekognition
def compare_faces(source_file_stream, target_file_stream):
    rekognition = boto3.client('rekognition', 
                               region_name=region, 
                               aws_access_key_id=aws_access_key_id, 
                               aws_secret_access_key=aws_secret_access_key)
    response = rekognition.compare_faces(
        SourceImage={
            'Bytes': source_file_stream
        },
        TargetImage={
            'Bytes': target_file_stream
        },
        SimilarityThreshold=90,
        QualityFilter='HIGH'
    )
    return response

@app.route('/compare_face', methods=['POST'])
def compare_faces_endpoint():
    try:
        source_file = request.files['source_file']
        target_file = request.files['target_file']
        if source_file.filename != '' and target_file.filename != '':
            source_file_stream = source_file.read()
            target_file_stream = target_file.read()
            response = compare_faces(source_file_stream, target_file_stream)
            face_matches = response['FaceMatches']
            if face_matches:
                return jsonify({'result': 'Match'})
            else:
                return jsonify({'result': 'No Match'})
        else:
            return jsonify({'error': 'One or both files are missing'})
    except Exception as e:
        print('invalid format gambar')
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)