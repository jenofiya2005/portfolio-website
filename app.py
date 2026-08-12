from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# ---------- MongoDB Connection ----------
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client["portfolio_db"]
projects_col = db["projects"]
messages_col = db["messages"]

# ---------- Seed default projects if DB is empty ----------
def seed_projects():
    if projects_col.count_documents({}) == 0:
        default_projects = [
            {
                "title": "GUVI Full Stack App",
                "description": "Register-Login-Profile system with PHP, MySQL, MongoDB, Redis.",
                "tech": "PHP, MySQL, MongoDB, Redis, Docker",
                "github": "https://github.com/jenofiya2005",
                "live": "",
                "image": "https://via.placeholder.com/400x250?text=GUVI+Project"
            },
            {
                "title": "Online Quiz & Evaluation System",
                "description": "Flask based quiz app with dynamic questions, timer and scoring.",
                "tech": "Flask, Python, Bootstrap",
                "github": "https://github.com/jenofiya2005",
                "live": "",
                "image": "https://via.placeholder.com/400x250?text=Quiz+System"
            },
            {
                "title": "Face Recognition System",
                "description": "PCA and ANN based face recognition built during internship.",
                "tech": "Python, PCA, ANN",
                "github": "https://github.com/jenofiya2005",
                "live": "",
                "image": "https://via.placeholder.com/400x250?text=Face+Recognition"
            }
        ]
        projects_col.insert_many(default_projects)

seed_projects()

# ---------- Frontend Routes ----------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/projects")
def projects_page():
    return render_template("projects.html")

@app.route("/contact")
def contact_page():
    return render_template("contact.html")

# ---------- API Routes ----------
@app.route("/api/projects", methods=["GET"])
def get_projects():
    projects = []
    for p in projects_col.find():
        p["_id"] = str(p["_id"])
        projects.append(p)
    return jsonify(projects)

@app.route("/api/projects", methods=["POST"])
def add_project():
    data = request.get_json()
    required = ["title", "description", "tech"]
    if not all(field in data and data[field] for field in required):
        return jsonify({"error": "title, description and tech are required"}), 400

    project = {
        "title": data.get("title"),
        "description": data.get("description"),
        "tech": data.get("tech"),
        "github": data.get("github", ""),
        "live": data.get("live", ""),
        "image": data.get("image", "https://via.placeholder.com/400x250?text=Project")
    }
    result = projects_col.insert_one(project)
    project["_id"] = str(result.inserted_id)
    return jsonify(project), 201

@app.route("/api/projects/<project_id>", methods=["DELETE"])
def delete_project(project_id):
    projects_col.delete_one({"_id": ObjectId(project_id)})
    return jsonify({"message": "deleted"}), 200

@app.route("/api/contact", methods=["POST"])
def contact():
    data = request.get_json()
    if not data.get("name") or not data.get("email") or not data.get("message"):
        return jsonify({"error": "name, email and message are required"}), 400
    messages_col.insert_one(data)
    return jsonify({"message": "Message received, thank you!"}), 201

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
