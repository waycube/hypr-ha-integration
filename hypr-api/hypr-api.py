from fastapi import FastAPI, HTTPException
import subprocess
import os
import json

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
    try:
        # --------------------
        # Workspace (per focused monitor)
        # --------------------
        monitors = subprocess.run(
            [HYPRCTL, "monitors", "-j"],
            check=True,
            capture_output=True,
            text=True,
        )
        monitors_data = json.loads(monitors.stdout)

        active_workspace = None
        for m in monitors_data:
            if m.get("focused"):
                active_workspace = m.get("activeWorkspace", {}).get("id")
                break

        # --------------------
        # Active window (best-effort)
        # --------------------
        app_class = None
        title = None

        try:
            window = subprocess.run(
                [HYPRCTL, "activewindow", "-j"],
                check=True,
                capture_output=True,
                text=True,
            )
            window_data = json.loads(window.stdout)
            app_class = window_data.get("class")
            title = window_data.get("title")
        except Exception:
            # Geen actief window (lege workspace, lockscreen, etc.)
            pass

        return {
            "status": "ok",
            "workspace": active_workspace,
            "app": app_class,
            "title": title,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
