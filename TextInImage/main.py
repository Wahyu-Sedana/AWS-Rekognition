from flask import Flask, request, jsonify
import boto3
from dotenv import load_dotenv
import os

load_dotenv()

aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
region = os.getenv("REGION")

app = Flask(__name__)


def detectText(file_stream):
    rekognition = boto3.client('rekognition', 
                               region_name=region, 
                               aws_access_key_id=aws_access_key_id, 
                               aws_secret_access_key=aws_secret_access_key)
    response = rekognition.detect_text(
        Image={
            'Bytes': file_stream
        }
    )
    return response

@app.route('/detect_text', methods=['POST'])
def detectTextEndpoint():
    try:
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            file_stream = uploaded_file.read()
            response = detectText(file_stream)
            detected_text = []

            # Mengambil teks yang terdeteksi dari respons AWS Rekognition
            for item in response['TextDetections']:
                detected_text.append(item['DetectedText'])

            return jsonify({'detected_text': detected_text})
        else:
            return jsonify({'error': 'No file uploaded'})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)