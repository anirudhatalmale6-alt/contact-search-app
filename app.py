from flask import Flask, render_template, request, jsonify
import openpyxl
import json
import os
from datetime import datetime

app = Flask(__name__)

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
CONTACTS_FILE = os.path.join(DATA_DIR, "list.xlsx")
INTERESTED_FILE = os.path.join(DATA_DIR, "interested.json")


def load_contacts():
    if not os.path.exists(CONTACTS_FILE):
        return []
    wb = openpyxl.load_workbook(CONTACTS_FILE, read_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    if not rows:
        return []
    headers = [str(h).strip().lower() if h else f"col_{i}" for i, h in enumerate(rows[0])]
    contacts = []
    for i, row in enumerate(rows[1:], start=1):
        record = {"_id": i}
        for j, val in enumerate(row):
            if j < len(headers):
                record[headers[j]] = str(val).strip() if val is not None else ""
        contacts.append(record)
    wb.close()
    return contacts


def load_interested():
    if not os.path.exists(INTERESTED_FILE):
        return []
    with open(INTERESTED_FILE, "r") as f:
        return json.load(f)


def save_interested(entries):
    with open(INTERESTED_FILE, "w") as f:
        json.dump(entries, f, indent=2)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/contacts")
def get_contacts():
    contacts = load_contacts()
    return jsonify(contacts)


@app.route("/api/interested", methods=["GET"])
def get_interested():
    return jsonify(load_interested())


@app.route("/api/interested", methods=["POST"])
def add_interested():
    data = request.get_json()
    if not data or "contact" not in data:
        return jsonify({"error": "Missing contact data"}), 400
    entry = {
        "contact": data["contact"],
        "comment": data.get("comment", ""),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    entries = load_interested()
    entries.append(entry)
    save_interested(entries)
    return jsonify({"success": True, "entry": entry})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
