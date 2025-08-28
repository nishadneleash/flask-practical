from flask import (
    Flask, render_template, request, redirect,
    url_for, session, jsonify, abort
)
from datetime import timedelta
from flask import Blueprint

app = Flask(__name__)
app.secret_key = "change-me"                  # ⚠️ use env var in real apps
app.permanent_session_lifetime = timedelta(days=7)

# 1) Basic app + 4) Render template (home page)
@app.route("/")
def home():
    return render_template("index.html")

# 2) Static files + another template example
@app.route("/about")
def about():
    return render_template("index.html", page="about")

# 3) Routes with HTTP methods  + 6/7) Forms & validation
@app.route("/form", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if not name:  # 7) validate
            return render_template("form.html", error="Name is required!")
        session["user"] = name  # 8) session
        return redirect(url_for("profile", username=name))  # 9) redirect
    return render_template("form.html")

# 5) url_for demo links
@app.route("/links")
def links():
    return (
        f'<a href="{url_for("home")}">Home</a> | '
        f'<a href="{url_for("about")}">About</a> | '
        f'<a href="{url_for("profile", username="neleash")}">Profile</a>'
    )

# 8) Sessions (login/logout/me)
@app.route("/login")
def login():
    session.permanent = True
    session["user"] = "Neleash"
    return "Logged in!"

@app.route("/me")
def me():
    return f"Current user: {session.get('user','(none)')}"

@app.route("/logout")
def logout():
    session.clear()
    return "Logged out!"

# 9) redirect to home
@app.route("/go-home")
def go_home():
    return redirect(url_for("home"))

# 10) error handling (404)
@app.errorhandler(404)
def not_found(e):
    # custom template; falls back to plain text if template missing
    try:
        return render_template("404.html"), 404
    except Exception:
        return "Page not found", 404

@app.route("/boom")
def boom():
    abort(404)

# 11) Blueprints (simple demo in same file)
admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/")
def admin_home():
    return "Admin dashboard (Blueprint)"

app.register_blueprint(admin_bp)

# 12) Custom Jinja filter
@app.template_filter("caps")
def caps(s):
    return (s or "").capitalize()

# 13) Query parameters: /search?q=flask
@app.route("/search")
def search():
    q = request.args.get("q", "")
    return f"Search term: {q}"

# 14) JSON response
@app.route("/api/ping")
def api_ping():
    return jsonify(ok=True, message="pong")

# 15) URL parameters
@app.route("/user/<username>")
def profile(username):
    return f"Profile page for {username}"

if __name__ == "__main__":
    app.run(debug=True)



