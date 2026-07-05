from flask import (
    Blueprint,
    current_app,
    jsonify,
    render_template,
    request,
)

web_blueprint = Blueprint(
    "web",
    __name__,
)


@web_blueprint.get("/")
def home():
    return render_template("index.html")


@web_blueprint.post("/api/chat")
def chat():

    payload = request.get_json(force=True)

    user_id = payload.get(
        "user_id",
        "anonymous",
    )

    message = payload.get(
        "message",
        "",
    )

    chat_service = current_app.config["chat_service"]

    reply = chat_service.process_chat_request(
        user_id=user_id,
        user_message=message,
    )

    return jsonify(
        {
            "reply": reply,
        }
    )