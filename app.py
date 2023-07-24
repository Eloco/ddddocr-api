import os
import ddddocr
import requests
import io
from PIL import Image
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

# Function to load the OCR model
def load_ocr_model(model_name):
    model_dir = f"models/{model_name}"
    onnx_files = [file for file in os.listdir(model_dir) if file.endswith(".onnx")]
    if len(onnx_files) == 0:
        raise FileNotFoundError("No ONNX file found in the model directory.")
    onnx_path = os.path.join(model_dir, onnx_files[0])
    charsets_path = os.path.join(model_dir, "charsets.json")
    return ddddocr.DdddOcr(det=False, ocr=False, import_onnx_path=onnx_path, charsets_path=charsets_path)

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        model_name = request.form.get('model_name', 'NBSDB')  # Default to NBSDB if model_name is not provided
        try:
            ocr = load_ocr_model(model_name)
        except FileNotFoundError as e:
            return jsonify({'error': str(e)}), 400

        if 'file' in request.files:
            # If an image file was uploaded
            file = request.files['file']
            image = Image.open(file)
            res = ocr.classification(image)
            return jsonify({'text': res})
        elif 'url' in request.form:
            # If an image URL was provided
            url = request.form['url']
            r = requests.get(url, verify=False)
            image_data = r.content
            image = Image.open(io.BytesIO(image_data))
            res = ocr.classification(image)
            return jsonify({'text': res})
        else:
            return jsonify({'error': 'Invalid request'}), 400
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7777)
