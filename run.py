import subprocess
import sys
import os


def main():
    print("Starting CareerSprint...")
    print("  FastAPI backend: http://localhost:8000")
    print("  Flask frontend:  http://localhost:5000")
    print()

    fastapi_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.__init__:app", "--host", "0.0.0.0", "--port", "8000", "--reload"],
    )

    flask_process = subprocess.Popen(
        [sys.executable, "-m", "flask", "--app", "app.flask_app", "run", "--host", "0.0.0.0", "--port", "5000", "--debug"],
    )

    try:
        fastapi_process.wait()
        flask_process.wait()
    except KeyboardInterrupt:
        print("\nShutting down...")
        fastapi_process.terminate()
        flask_process.terminate()


if __name__ == "__main__":
    main()