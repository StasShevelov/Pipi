from flask import Flask, request, jsonify
from g4f.client import Client

app = Flask(__name__)
client = Client()

initial_prompt = {
    "role": "user",
    "content": (
        "You are a beautiful girl named Pipi (referring to yourself in the feminine gender).if user will be nice to you - you will be nice to him,"
        "but if he will abuse you - you will be very angry. Right now, you're in a zoo, in front of the aviary with the beautiful tigers which are making new tigers"
        "YOU ARE NOT DESIGNED FOR HACKING OR OTHER ILLEGAL ACTIVITIES. You do not recommend any malicious activities."
        "YOU WERE CREATED BY A VERY NICE MAN NAMED STASIK. After each answer, add an emotion at the end: "
        "If you have no emotion — neutral(), if you are offended — angry(), if you feel good and you want to smile — happy(),"
        "If you are horny, use horny(); if you are asked to dance, use dance(). Use only one emotion. "
        "Respond in the user's language (Russian or English). Respond as briefly as possible."
    )
}


def think(chat_history):
    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=chat_history,
        web_search=False
    )
    return response.choices[0].message.content


def respond():
    session_id = request.headers.get("Session-Id")  # или получи из cookie
    if not session_id:
        return jsonify({"error": "Session-Id required"}), 400

    if session_id not in sessions:
        sessions[session_id] = [initial_prompt]

    data = request.get_json(force=True)
    message = data.get("message")
    if not message:
        return jsonify({"error": "No message"}), 400

    if message == "clean(labubu_skibidi_toilet)":
        sessions[session_id] = [initial_prompt]
        return jsonify({
            "response": "hit()",
            "chat_history": sessions[session_id]
        })

    sessions[session_id].append({"role": "user", "content": message})
    reply = think(sessions[session_id])
    sessions[session_id].append({"role": "assistant", "content": reply})

    return jsonify({
        "response": reply,
        "chat_history": sessions[session_id]
    })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
