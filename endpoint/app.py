from flask import Flask, render_template, request, Response, jsonify
from llm import chain, extract_text
from retriever import retrieve, build_context

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/stream")
def stream():
    user_input = request.args.get("user_input")

    def generate():
        chunks = retrieve(user_input, top_k=2)
        context = build_context(chunks)

        for chunk in chain.stream({"context": context, "question": user_input}):
            text = extract_text(chunk.content)

            if text:
                safe = text.replace("\n", "\\n")
                yield f"data: {safe}\n\n"

    return Response(
        generate(), mimetype="text/event-stream"
    )  # Server‑Sent Events (SSE)


@app.route("/test")
def test():
    user_input = request.args.get("user_input")

    chunks = retrieve(user_input, top_k=2)
    context = build_context(chunks)

    answer = extract_text(
        chain.invoke({"context": context, "question": user_input}).content
    )
    return jsonify(
        {
            "question": user_input,
            "answer": answer,
            "chunks": chunks,
        }
    )
