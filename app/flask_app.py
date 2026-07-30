import requests
from flask import Flask, render_template, request, redirect, url_for, session, flash
from app.config import API_BASE_URL, FLASK_SECRET_KEY

flask_app = Flask(__name__)
flask_app.secret_key = FLASK_SECRET_KEY


def api_headers():
    token = session.get("token")
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"} if token else {}


def safe_json(resp):
    try:
        return resp.json()
    except Exception:
        return {"detail": f"Server error ({resp.status_code})"}


@flask_app.route("/")
def home():
    if "token" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@flask_app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = {
            "name": request.form["name"],
            "email": request.form["email"],
            "password": request.form["password"],
        }
        resp = requests.post(f"{API_BASE_URL}/api/auth/register", json=data)
        if resp.status_code == 200:
            body = safe_json(resp)
            session["token"] = body["token"]
            session["user"] = body["user"]
            flash("Registration successful!", "success")
            return redirect(url_for("dashboard"))
        flash(safe_json(resp).get("detail", "Registration failed"), "danger")
    return render_template("auth/register.html")


@flask_app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = {"email": request.form["email"], "password": request.form["password"]}
        resp = requests.post(f"{API_BASE_URL}/api/auth/login", json=data)
        if resp.status_code == 200:
            body = safe_json(resp)
            session["token"] = body["token"]
            session["user"] = body["user"]
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))
        flash(safe_json(resp).get("detail", "Invalid credentials"), "danger")
    return render_template("auth/login.html")


@flask_app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully", "success")
    return redirect(url_for("login"))


@flask_app.route("/dashboard")
def dashboard():
    if "token" not in session:
        return redirect(url_for("login"))
    resp = requests.get(f"{API_BASE_URL}/api/applications/dashboard", headers=api_headers())
    stats = safe_json(resp) if resp.status_code == 200 else {}
    return render_template("dashboard.html", stats=stats, user=session.get("user"))


@flask_app.route("/applications")
def list_applications():
    if "token" not in session:
        return redirect(url_for("login"))
    search = request.args.get("search", "")
    status_filter = request.args.get("status", "")
    params = {}
    if search:
        params["search"] = search
    if status_filter:
        params["status"] = status_filter
    resp = requests.get(f"{API_BASE_URL}/api/applications", headers=api_headers(), params=params)
    apps = safe_json(resp) if resp.status_code == 200 else []
    return render_template("applications/list.html", applications=apps, user=session.get("user"),
                           search=search, status_filter=status_filter)


@flask_app.route("/applications/add", methods=["GET", "POST"])
def add_application():
    if "token" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        data = {
            "company_name": request.form["company_name"],
            "role": request.form["role"],
            "application_date": request.form["application_date"],
            "source": request.form.get("source", ""),
            "status": request.form.get("status", "Applied"),
            "notes": request.form.get("notes", ""),
        }
        resp = requests.post(f"{API_BASE_URL}/api/applications", json=data, headers=api_headers())
        if resp.status_code == 200:
            flash("Application added successfully!", "success")
            return redirect(url_for("list_applications"))
        flash(safe_json(resp).get("detail", "Failed to add application"), "danger")
    return render_template("applications/form.html", user=session.get("user"), application=None)


@flask_app.route("/applications/<int:app_id>")
def view_application(app_id):
    if "token" not in session:
        return redirect(url_for("login"))
    resp = requests.get(f"{API_BASE_URL}/api/applications/{app_id}", headers=api_headers())
    if resp.status_code != 200:
        flash("Application not found", "danger")
        return redirect(url_for("list_applications"))
    app_data = safe_json(resp)
    rounds_resp = requests.get(f"{API_BASE_URL}/api/interviews/{app_id}", headers=api_headers())
    rounds = safe_json(rounds_resp) if rounds_resp.status_code == 200 else []
    return render_template("applications/detail.html", application=app_data, rounds=rounds, user=session.get("user"))


@flask_app.route("/applications/<int:app_id>/edit", methods=["GET", "POST"])
def edit_application(app_id):
    if "token" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        data = {
            "company_name": request.form["company_name"],
            "role": request.form["role"],
            "application_date": request.form["application_date"],
            "source": request.form.get("source", ""),
            "status": request.form.get("status", "Applied"),
            "notes": request.form.get("notes", ""),
        }
        resp = requests.put(f"{API_BASE_URL}/api/applications/{app_id}", json=data, headers=api_headers())
        if resp.status_code == 200:
            flash("Application updated successfully!", "success")
            return redirect(url_for("view_application", app_id=app_id))
        flash(safe_json(resp).get("detail", "Failed to update application"), "danger")
    resp = requests.get(f"{API_BASE_URL}/api/applications/{app_id}", headers=api_headers())
    if resp.status_code != 200:
        flash("Application not found", "danger")
        return redirect(url_for("list_applications"))
    return render_template("applications/form.html", user=session.get("user"), application=safe_json(resp))


@flask_app.route("/applications/<int:app_id>/delete", methods=["POST"])
def delete_application(app_id):
    if "token" not in session:
        return redirect(url_for("login"))
    resp = requests.delete(f"{API_BASE_URL}/api/applications/{app_id}", headers=api_headers())
    if resp.status_code == 200:
        flash("Application deleted successfully!", "success")
    else:
        flash("Failed to delete application", "danger")
    return redirect(url_for("list_applications"))


@flask_app.route("/applications/<int:app_id>/interviews/add", methods=["GET", "POST"])
def add_interview_round(app_id):
    if "token" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        data = {
            "round_number": int(request.form["round_number"]),
            "round_type": request.form.get("round_type", ""),
            "interview_date": request.form.get("interview_date") or None,
            "result": request.form.get("result", "Awaiting Result"),
            "notes": request.form.get("notes", ""),
        }
        resp = requests.post(f"{API_BASE_URL}/api/interviews/{app_id}", json=data, headers=api_headers())
        if resp.status_code == 200:
            flash("Interview round added!", "success")
            return redirect(url_for("view_application", app_id=app_id))
        flash(safe_json(resp).get("detail", "Failed to add interview round"), "danger")
    return render_template("interviews/form.html", user=session.get("user"), application_id=app_id, round=None)


@flask_app.route("/applications/<int:app_id>/interviews/<int:round_id>/edit", methods=["GET", "POST"])
def edit_interview_round(app_id, round_id):
    if "token" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        data = {
            "round_number": int(request.form["round_number"]),
            "round_type": request.form.get("round_type", ""),
            "interview_date": request.form.get("interview_date") or None,
            "result": request.form.get("result", "Awaiting Result"),
            "notes": request.form.get("notes", ""),
        }
        resp = requests.put(f"{API_BASE_URL}/api/interviews/{app_id}/{round_id}", json=data, headers=api_headers())
        if resp.status_code == 200:
            flash("Interview round updated!", "success")
            return redirect(url_for("view_application", app_id=app_id))
        flash(safe_json(resp).get("detail", "Failed to update interview round"), "danger")
    rounds_resp = requests.get(f"{API_BASE_URL}/api/interviews/{app_id}", headers=api_headers())
    rounds = safe_json(rounds_resp) if rounds_resp.status_code == 200 else []
    current_round = next((r for r in rounds if r["round_id"] == round_id), None)
    if not current_round:
        flash("Interview round not found", "danger")
        return redirect(url_for("view_application", app_id=app_id))
    return render_template("interviews/form.html", user=session.get("user"), application_id=app_id, round=current_round)


@flask_app.route("/applications/<int:app_id>/interviews/<int:round_id>/delete", methods=["POST"])
def delete_interview_round(app_id, round_id):
    if "token" not in session:
        return redirect(url_for("login"))
    resp = requests.delete(f"{API_BASE_URL}/api/interviews/{app_id}/{round_id}", headers=api_headers())
    if resp.status_code == 200:
        flash("Interview round deleted!", "success")
    else:
        flash("Failed to delete interview round", "danger")
    return redirect(url_for("view_application", app_id=app_id))