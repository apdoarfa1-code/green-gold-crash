import subprocess
import time
import webbrowser
import sys
import os

def run_local():
    print("==================================================")
    print("   Starting Green Gold Cloud Local Environment... ")
    print("==================================================")

    # 1. Start FastAPI Backend via uvicorn
    print("[1/3] Starting FastAPI Backend on http://localhost:8000 ...")
    backend_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"],
        cwd="/home/apdo/Desktop/كراش/backend"
    )

    # Wait for backend to boot up
    time.sleep(3)

    # 2. Start Streamlit Dashboard
    print("[2/3] Starting Streamlit Dashboard on http://localhost:8501 ...")
    streamlit_process = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "dashboard/streamlit_app.py", "--server.port=8501", "--server.headless=true"],
        cwd="/home/apdo/Desktop/كراش"
    )

    # Wait for streamlit to boot up
    time.sleep(3)

    # 3. Open Web Browser automatically
    print("[3/3] Opening browser at http://localhost:8501 ...")
    webbrowser.open("http://localhost:8501")

    print("\n--------------------------------------------------")
    print("🟢 Green Gold Cloud is running successfully!")
    print("Press Ctrl+C in this terminal to stop all services.")
    print("--------------------------------------------------\n")

    try:
        backend_process.wait()
        streamlit_process.wait()
    except KeyboardInterrupt:
        print("\nStopping services gracefully...")
        backend_process.terminate()
        streamlit_process.terminate()
        backend_process.wait()
        streamlit_process.wait()
        print("All services stopped. Goodbye!")

if __name__ == "__main__":
    run_local()
