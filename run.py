import os
import sys
import subprocess
import time

def main():
    print("==========================================================")
    print("       Fact Knowledge Layer - Application Launcher        ")
    print("==========================================================")
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(base_dir, "backend")
    frontend_dir = os.path.join(base_dir, "frontend")
    
    print("[1/2] Starting FastAPI Backend on http://127.0.0.1:8000 ...")
    backend_cmd = [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000", "--reload"]
    backend_process = subprocess.Popen(backend_cmd, cwd=backend_dir)
    
    time.sleep(3)
    
    print("[2/2] Starting React Frontend on http://localhost:5173 ...")
    npm_cmd = "npm.cmd" if sys.platform == "win32" else "npm"
    frontend_cmd = [npm_cmd, "run", "dev"]
    frontend_process = subprocess.Popen(frontend_cmd, cwd=frontend_dir)
    
    print("\n----------------------------------------------------------")
    print(" Application Successfully Running!")
    print(" Web Interface:  http://localhost:5173")
    print(" API Docs:       http://127.0.0.1:8000/docs")
    print(" Press Ctrl+C to stop servers.")
    print("----------------------------------------------------------\n")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down servers...")
        backend_process.terminate()
        frontend_process.terminate()
        sys.exit(0)

if __name__ == "__main__":
    main()
