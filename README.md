# Contact Search Web App

Lightweight single-page web app for searching contacts from an Excel file and marking contacts as "Interested" with optional comments.

## Quick Start

1. Install Python dependencies:
   ```
   pip install flask openpyxl
   ```

2. Place your Excel file as `contacts.xlsx` in this folder.
   - The first row should be headers (e.g., First Name, Last Name, Email, Phone, Company)
   - Any column names containing "first", "last", or "name" are used for search
   - All other columns are displayed as contact details

3. Run the app:
   ```
   python app.py
   ```

4. Open http://localhost:5000 on your phone or computer.

## Features

- Instant search as you type (searches first/last name, partial matches)
- Landscape-optimized two-column grid layout for phone use
- "INTERESTED" button with optional comment per contact
- All submissions saved to `interested.json` with timestamps
- No login or authentication required

## Files

- `app.py` - Flask backend (reads Excel, serves API, saves interested contacts)
- `templates/index.html` - Frontend (search UI, cards, comment flow)
- `contacts.xlsx` - Your contact list (replace with your own)
- `interested.json` - Auto-created file with saved interested contacts
- `create_sample.py` - Helper to generate a sample contacts.xlsx for testing
- `requirements.txt` - Python dependencies

## Interested Data Format

Each entry in `interested.json`:
```json
{
  "contact": { "first name": "Jane", "last name": "Doe", "email": "...", ... },
  "comment": "User's comment here",
  "timestamp": "2026-06-06 12:30:45"
}
```
