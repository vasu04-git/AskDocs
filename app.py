from flask import Flask, render_template, request, jsonify
import os

from rag.pdf_loader import load_pdf
from rag.chunker import chunk_text
from rag.embedding import generate_embedding
from rag.qdrant_db import create_collection, upload_chunks
from rag.rag_pipeline import ask_document

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def home():
    return render_template("index.html")


# ---------------------------
# Upload Document
# ---------------------------
@app.route("/upload", methods=["POST"])
def upload():

    if "file" not in request.files:
        return jsonify({
            "message": "No file uploaded."
        }), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({
            "message": "Please choose a file."
        }), 400

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)

    file.save(filepath)

    try:

        # Read PDF
        text = load_pdf(filepath)

        # Chunk
        chunks = chunk_text(text)

        # Embeddings
        embeddings = generate_embedding(chunks)

        # Store in Qdrant
        create_collection()
        upload_chunks(chunks,embeddings,file.filename)

        return jsonify({
            "message": "Document uploaded successfully!"
        })

    except Exception as e:

        return jsonify({
            "message": str(e)
        }), 500


# ---------------------------
# Ask Question
# ---------------------------
@app.route("/ask", methods=["POST"])
def ask():

    data = request.get_json()

    question = data.get("question", "").strip()

    if question == "":
        return jsonify({
            "answer": "Please enter a question."
        })

    try:

        answer = ask_document(question)

        return jsonify({
            "answer": answer
        })

    except Exception as e:

        return jsonify({
            "answer": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)