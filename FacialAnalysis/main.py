from dotenv import load_dotenv
from flask import Flask, request, jsonify
import boto3

# Retrieve AWS access key and secret key from environment variables
aws_access_key_id = ""
aws_secret_access_key = ""

app = Flask(__name__)

# Fungsi untuk melakukan analisis wajah dengan AWS Rekognition
def analyze_face(file_stream):
    rekognition = boto3.client('rekognition', 
                               region_name='', 
                               aws_access_key_id=aws_access_key_id, 
                               aws_secret_access_key=aws_secret_access_key)
    response = rekognition.detect_faces(
        Image={'Bytes': file_stream},
        Attributes=['ALL'] 
    )
    return response

# Endpoint untuk mengunggah gambar dan melakukan analisis wajah
@app.route('/analyze_face', methods=['POST'])
def upload_and_analyze_face():
    try:
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            file_stream = uploaded_file.read()
            response = analyze_face(file_stream)
            print('dapat response')
            return jsonify(response)
        else:
            return jsonify({'error': 'No file uploaded'})
    except Exception as e:
        print('invalid format gambar')
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)