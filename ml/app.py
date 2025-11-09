from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import pickle
import re
import nltk
from nltk.corpus import stopwords

# Initialize Flask
app = Flask(__name__)

# --- Load model and preprocessing tools ---
print("Loading model and preprocessing tools...")
model = load_model("C:\Python\emotion prediction\ml\models\emotion_cnn_model.keras")

with open(r"C:\Python\emotion prediction\ml\models\tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

with open(r"C:\Python\emotion prediction\ml\models\label_encoder.pkl", "rb") as f:
    le = pickle.load(f)

# --- Download stopwords ---
nltk.download("stopwords")
stop_words = set(stopwords.words("english"))

# --- Helper function for cleaning text ---
def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-z\s]", "", text)
    text = " ".join([word for word in text.split() if word not in stop_words])
    return text

# --- API route for prediction ---
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        text = data.get("text", "")

        if not text.strip():
            return jsonify({"error": "No text provided"}), 400

        cleaned = clean_text(text)
        seq = tokenizer.texts_to_sequences([cleaned])
        padded = pad_sequences(seq, maxlen=100, padding="post", truncating="post")

        pred = model.predict(padded)
        emotion = le.classes_[np.argmax(pred)]
        confidence = float(np.max(pred))

        return jsonify({
            "emotion": emotion,
            "confidence": confidence
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- Default route ---
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Emotion Classification API is running!"})


# --- Run the Flask app ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
