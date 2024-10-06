from flask import render_template, request, Response
from flask.views import MethodView, View

from repo import ClassifierRepo
from services import PredictDigitService
from settings import CLASSIFIER_STORAGE

import base64
import re

# Add the missing IndexView
class IndexView(View):
    def dispatch_request(self):
        return render_template('index.html')

class NumberIdentificationView(View):
    def dispatch_request(self):
        return render_template('number_identification.html')

class PredictDigitView(MethodView):
    def post(self):
        repo = ClassifierRepo(CLASSIFIER_STORAGE)
        service = PredictDigitService(repo)

        # Get the image data URI from the request
        image_data_uri = request.json.get('image')

        if not image_data_uri:
            return Response("No image data provided", status=400)

        # Extract base64 data from the data URI (assuming "data:image/png;base64," prefix)
        image_data = re.sub('^data:image/.+;base64,', '', image_data_uri)

        # Decode the base64 string
        image_binary = base64.b64decode(image_data)

        # Print binary data in the terminal
        print(image_binary)

        # Optionally save to a file to verify
        with open("decoded_image.png", "wb") as f:
            f.write(image_binary)

        # Process the image using the service
        prediction = service.handle(image_data_uri)

        return Response(str(prediction).encode(), status=200)
