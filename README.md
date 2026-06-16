# DentAI — Frontend

Streamlit frontend for DentAI, an AI-powered tool for detecting oral conditions from photographs. Upload a dental photo, click Predict, and get a list of detected conditions with confidence scores alongside an annotated image.

**Live:** https://dentai.streamlit.app/

## What it detects

Calculus · Cavity · Discoloration · Gingivitis · Hypodontia · Ulcer

Powered by the [DentAI API](https://github.com/nirjalalala/DentAI_api) (FastAPI + custom-trained YOLOv5).

## Run locally

```bash
pip install -r requirements.txt
streamlit run main.py
```

App will open at `http://localhost:8501`. The frontend points to the hosted API at `https://dentai.onrender.com` — no local API setup needed.
