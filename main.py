from flask import Flask, render_template, request, session, redirect
from flask_socketio import SocketIO, emit, join_room
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.permanent_session_lifetime = timedelta(minutes=60)
socketio = SocketIO(app)

PASSWORD = "2310"
chat_messages = []

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form.get("password")
        if password == PASSWORD:
            session["authenticated"] = True
            return redirect("/chat")
    return render_template("login.html")

@app.route("/chat")
def chat():
    if not session.get("authenticated"):
        return redirect("/")
    return render_template("chat.html")

@socketio.on("send_message")
def handle_send(data):
    chat_messages.append(data)
    emit("new_message", data, broadcast=True)

@socketio.on("typing")
def handle_typing(data):
    emit("user_typing", data, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
