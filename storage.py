import os
import json
import uuid
from pathlib import Path
from datetime import datetime

PHOTO_DIR = "photos"
GALLERIES_FILE = "galleries.json"

class GalleryStorage:
    def __init__(self):
        self.photo_path = Path(PHOTO_DIR)
        self.photo_path.mkdir(exist_ok=True)
        self._load_galleries()

    def _load_galleries(self):
        if os.path.exists(GALLERIES_FILE):
            with open(GALLERIES_FILE, "r") as f:
                self.galleries = json.load(f)
        else:
            self.galleries = {}

    def _save_galleries(self):
        with open(GALLERIES_FILE, "w") as f:
            json.dump(self.galleries, f, indent=2)

    def save_photo(self, user_id: int, file_bytes: bytes, ext=".jpg") -> str:
        filename = f"{uuid.uuid4().hex}{ext}"
        filepath = self.photo_path / filename
        with open(filepath, "wb") as f:
            f.write(file_bytes)
        return filename

    def add_temp_photo(self, user_id: int, filename: str):
        temp_file = self.photo_path / f"temp_{user_id}.json"
        if temp_file.exists():
            with open(temp_file, "r") as f:
                photos = json.load(f)
        else:
            photos = []
        photos.append(filename)
        with open(temp_file, "w") as f:
            json.dump(photos, f)

    def get_temp_photos(self, user_id: int):
        temp_file = self.photo_path / f"temp_{user_id}.json"
        if temp_file.exists():
            with open(temp_file, "r") as f:
                return json.load(f)
        return []

    def clear_temp_photos(self, user_id: int):
        temp_file = self.photo_path / f"temp_{user_id}.json"
        if temp_file.exists():
            with open(temp_file, "r") as f:
                photos = json.load(f)
            for p in photos:
                try:
                    (self.photo_path / p).unlink()
                except:
                    pass
            temp_file.unlink()

    def clear_temp_metadata(self, user_id: int):
        temp_file = self.photo_path / f"temp_{user_id}.json"
        if temp_file.exists():
            temp_file.unlink()

    def create_gallery(self, user_id: int) -> str:
        photos = self.get_temp_photos(user_id)
        if not photos:
            return None
        gallery_id = uuid.uuid4().hex
        self.galleries[gallery_id] = {
            "photos": photos,
            "created_by": user_id,
            "created_at": datetime.now().isoformat()
        }
        self._save_galleries()
        self.clear_temp_metadata(user_id)
        return gallery_id

    def get_gallery(self, gallery_id: str):
        return self.galleries.get(gallery_id)

storage = GalleryStorage()