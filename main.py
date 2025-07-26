from flask import Flask, render_template, request, redirect, session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "supersecretkey"
app.permanent_session_lifetime = timedelta(minutes=60)

PASSWORD = "2310khushi"
chat_messages = []

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        password = request.form.get("password")
        if password == PASSWORD:
            session["authenticated"] = True
            return redirect("/chat")
    return render_template("login.html")

@app.route("/chat", methods=["GET", "POST"])
def chat():
    if not session.get("authenticated"):
        return redirect("/")
    if request.method == "POST":
        message = request.form.get("message")
        if message:
            # Alternate between "You" and "Me"
            if len(chat_messages) % 2 == 0:
                sender = "You"
            else:
                sender = "Me"
            chat_messages.append((sender, message))
    return render_template("chat.html", chat=chat_messages)

@app.route("/get_messages")
def get_messages():
    if not session.get("authenticated"):
        return [], 401
    return chat_messages

@app.route("/logout")
def logout():
    session.pop("authenticated", None)
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)