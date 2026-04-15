# Agent-to-Agent (A2A) Protocol Lab

This repository contains a minimal but fully functional Agent-to-Agent (A2A) system, implementing an A2A Server (FastAPI) and an A2A Client, deployed to Google Cloud.

## Cloud Deployments
* **Cloud Run Service URL:** `https://echo-a2a-agent-837585057784.us-central1.run.app`

## Environment Setup
1. Ensure you have Python 3.10+ installed.
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Mac/Linux
   # or .venv\Scripts\activate # Windows
3. pip install -r server/requirements.txt
   pip install google-cloud-aiplatform google-auth

## How to run locally
cd server
uvicorn main:app --reload --port 8000

## Run the client demo
python client/demo.py