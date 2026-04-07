import os
import json
from flask import Flask, render_template, abort, send_from_directory

app = Flask(__name__)
PHOTO_DIR = "photos"
GALLERIES_FILE = "galleries.json"

def load_galleries():
    if os.path.exists(GALLERIES_FILE):
        with open(GALLERIES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

@app.route('/gallery/<gallery_id>')
def show_gallery(gallery_id):
    galleries = load_galleries()
    gallery = galleries.get(gallery_id)
    if not gallery:
        abort(404)
    photos = gallery["photos"]
    photo_urls = [f"/photos/{p}" for p in photos]
    return render_template("gallery.html", photos=photo_urls)

@app.route('/photos/<filename>')
def serve_photo(filename):
    return send_from_directory(PHOTO_DIR, filename)

@app.errorhandler(404)
def not_found(e):
    return "<h1>Галерея не найдена</h1>", 404

if __name__ == "__main__":
    os.makedirs(PHOTO_DIR, exist_ok=True)
    app.run(host='0.0.0.0', port=8080, debug=False)