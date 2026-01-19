from fastapi import FastAPI, HTTPException
import subprocess
import os

app = FastAPI()
HYPRCTL = "hyprctl"

def hypr(args):
    try:
        subprocess.run(
            [HYPRCTL] + args,
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=e.stderr)

@app.get("/status")
def status():
    return {"status": "ok"}

@app.post("/workspace/{num}")
def set_workspace(num: int):
    hypr(["dispatch", "workspace", str(num)])
    return {"ok": True}

@app.post("/exec")
def exec_app(command: str):
    hypr(["dispatch", "exec", command])
    return {"ok": True}

@app.post("/notify")
def notify(message: str, timeout: int = 3000):
    hypr(["notify", "1", str(timeout), message])
    return {"ok": True}
