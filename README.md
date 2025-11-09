# Emotion Prediction Using CNN

A full‑stack emotion detection application that classifies the dominant emotion expressed in free‑form text.

The system consists of:

- **Flask + TensorFlow backend (`ml/`)**: Loads a pretrained CNN text classification model (`models/emotion_cnn_model.keras`) plus a tokenizer and label encoder to preprocess and infer emotions.
- **Node.js middleware (`server/`)**: Acts as a lightweight proxy between the React client and the Flask model API (helpful for CORS control and future auth / rate limiting).
- **React Vite frontend (`client/`)**: Simple UI for users to enter text and view predicted emotion & confidence.

## ✨ Features

- Clean text preprocessing (lowercasing, URL & punctuation removal, stopword filtering)
- CNN-based multiclass emotion classification
- REST API endpoint: `POST /predict` (Flask) and `POST /analyze` (Node proxy)
- Confidence score returned with predicted label
- Modular 3‑tier architecture (ML service, middleware, UI)

## 🗂 Directory Structure

```
.
├─ ml/
│  ├─ app.py                # Flask API serving the Keras model
│  ├─ requirements.txt      # Python dependencies
│  └─ models/
│     ├─ emotion_cnn_model.keras
│     ├─ tokenizer.pkl
│     └─ label_encoder.pkl
├─ server/
│  ├─ index.js              # Express proxy server
│  ├─ package.json          # Node dependencies (express, cors, node-fetch)
├─ client/
│  ├─ src/                  # React source (Vite)
│  ├─ index.html
│  ├─ package.json
└─ README.md
```

## 🧠 Model Overview

A Convolutional Neural Network (CNN) processes tokenized text sequences (padded to length 100). The tokenizer and label encoder are serialized with pickle for consistent preprocessing and label mapping during inference.

## 🚀 Getting Started (Windows / PowerShell)

### 1. Clone Repository

```powershell
git clone <your-fork-or-origin-url> emotion_prediction_using_cnn
cd emotion_prediction_using_cnn
```

### 2. Start the ML Backend

Create & activate a virtual environment (recommended) then install deps.

```powershell
cd ml
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
python app.py   # runs on http://127.0.0.1:5000
```

> First run will download NLTK stopwords.

### 3. Start the Node Proxy Server

In a new terminal:

```powershell
cd server
npm install
node index.js       # or: npx nodemon index.js (auto‑reload)
# Runs on http://localhost:4000
```

### 4. Start the React Frontend

In another terminal:

```powershell
cd client
npm install
npm run dev         # Vite dev server (default http://localhost:5173)
```

Open the printed URL in your browser.

### 5. Use the App

1. Ensure Flask (5000) and Node (4000) are running.
2. Navigate to the React dev URL.
3. Enter text and click "Analyze Emotion".
4. View predicted emotion & confidence.

## 🔌 API Endpoints

### Flask Service (Internal)

`POST http://127.0.0.1:5000/predict`

```json
Request: { "text": "I am so excited about this!" }
Response: { "emotion": "joy", "confidence": 0.9732 }
```

Errors:

- 400: `{ "error": "No text provided" }`
- 500: `{ "error": "<exception message>" }`

### Node Proxy

`POST http://localhost:4000/analyze`

- Forwards body to Flask and returns same JSON.

## 🧪 Testing Locally

Currently there are no automated tests. Suggested quick manual check:

```powershell
# From repo root (assumes services running)
Invoke-RestMethod -Uri http://127.0.0.1:5000/predict -Method Post -Body (@{ text = 'This is amazing' } | ConvertTo-Json) -ContentType 'application/json'
```

## ⚙️ Configuration & Environment

- Ports are hardcoded (Flask 5000, Node 4000). For customization, edit `ml/app.py` (port) and `server/index.js`.
- Model + artifacts paths are absolute; consider switching to relative paths for portability.

## 🛡 Error Handling & Edge Cases

- Empty or whitespace-only text returns HTTP 400.
- Upstream failures or network issues at Flask layer surface as 500 from Node.
- Confidence is the max softmax probability of model prediction.

## 📦 Dependencies

### Python (`ml/requirements.txt`)

- flask, tensorflow, numpy, nltk, scikit-learn

### Node (`server/package.json`)

- express, cors, node-fetch, nodemon (dev)

### Frontend (`client/package.json`)

- react, react-dom, vite, eslint tooling

## 🔄 Future Improvements

- Add relative model paths & environment config (.env files)
- Containerize with Docker Compose (three services)
- Add unit tests (pytest for ML, Jest/React Testing Library for UI)
- Batch prediction endpoint & streaming support
- Add sentiment / sarcasm / toxicity multi-task models
- Authentication & rate limiting at Node layer
- CI workflow (GitHub Actions) for lint + test

## 🤝 Contributing

1. Fork & branch (`feat/your-feature`)
2. Make changes + add tests
3. Run format/lint (if added later)
4. Open PR describing change & model impact

## 📄 License

Specify a license (e.g., MIT) by adding a `LICENSE` file.

## 🙏 Acknowledgments

- NLTK for stopwords
- TensorFlow / Keras for model training

---

Feel free to adjust model path handling and add more UI styling as you iterate.
