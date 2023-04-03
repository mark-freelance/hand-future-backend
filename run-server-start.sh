source venv/bin/activate
pip install -r requirements.txt
HTTPS_PROXY=http://localhost:7890 python -m uvicorn main:app --port 3366 --host 0.0.0.0
