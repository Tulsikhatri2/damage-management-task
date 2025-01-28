from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
from skimage.metrics import structural_similarity as compare_ssim

app = Flask(__name__)
CORS(app)  # Allow requests from React

@app.route('/compare-images', methods=['POST'])
def compare_images():
    try:
        # Get files from the request
        file1 = request.files['image1']
        file2 = request.files['image2']

        # Convert files to images
        img1 = cv2.imdecode(np.frombuffer(file1.read(), np.uint8), cv2.IMREAD_COLOR)
        img2 = cv2.imdecode(np.frombuffer(file2.read(), np.uint8), cv2.IMREAD_COLOR)

        # Resize images
        img1 = cv2.resize(img1, (600, 360))
        img2 = cv2.resize(img2, (600, 360))

        # Grayscale
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        # Find similarity
        (similar, diff) = compare_ssim(gray1, gray2, full=True)
        difference_percentage = (1 - similar) * 100

        return jsonify({
            "similarity": round(similar, 2),
            "differencePercentage": round(difference_percentage, 2)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
