import os

from flask import Flask
from views import PredictDigitView, IndexView

app = Flask(__name__)

# This adds a URL rule to the Flask app so that when a POST request is made to
# /api/predict, the PredictDigitView.post method is called.
app.add_url_rule(
    '/api/predict',
    view_func=PredictDigitView.as_view('predict_digit'),
    methods=['POST']
)

# This adds a URL rule to the Flask app so that when a GET request is made to
# /, the IndexView.dispatch_request method is called.
app.add_url_rule(
    '/',
    view_func=IndexView.as_view('index'),
    methods=['GET']
)

# This checks if this script is being run directly (not being imported as a module
# by another script). If it is, it starts the Flask app on port 5000 (or a port
# specified in the PORT environment variable, if it exists).
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)



