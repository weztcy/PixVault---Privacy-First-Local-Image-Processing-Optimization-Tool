import json
import uuid
from datetime import datetime
from pathlib import Path


class HistoryManager:
    def __init__(self, storage_path="history/history.json"):

        self.storage_path = Path(storage_path)

        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

        if not self.storage_path.exists():
            self.save([])

    def add(
        self, source, output, format_name, operations, status="success", error=None
    ):

        history = self.get_all()

        record = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "source": str(source),
            "output": str(output),
            "format": format_name,
            "operations": operations,
            "status": status,
            "error": error,
        }

        history.append(record)

        self.save(history)

        return record

    def get_all(self):

        if not self.storage_path.exists():
            return []

        with open(self.storage_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def delete(self, record_id):

        history = self.get_all()

        history = [item for item in history if item["id"] != record_id]

        self.save(history)

    def clear(self):

        self.save([])

    def save(self, data):

        with open(self.storage_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
