sudo pacman -S python python-virtualenv

python -m venv ~/.venvs/hypr-agent
source ~/.venvs/hypr-agent/bin/activate
pip install fastapi uvicorn

---
start with:

source ~/.venvs/hypr-agent/bin/activate
uvicorn main:app

---

Verander workspace:
curl -X POST http://127.0.0.1:8129/workspace/1

Open programma:
curl -X POST "http://127.0.0.1:8129/exec?command=firefox"