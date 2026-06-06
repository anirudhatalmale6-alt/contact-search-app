"""Generate a sample contacts.xlsx for testing."""
import openpyxl

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Contacts"
ws.append(["First Name", "Last Name", "Email", "Phone", "Company"])

contacts = [
    ("John", "Smith", "john.smith@email.com", "+1-555-0101", "Acme Corp"),
    ("Jane", "Doe", "jane.doe@email.com", "+1-555-0102", "Tech Solutions"),
    ("Michael", "Johnson", "m.johnson@email.com", "+1-555-0103", "Global Inc"),
    ("Sarah", "Williams", "s.williams@email.com", "+1-555-0104", "StartupXYZ"),
    ("Robert", "Brown", "r.brown@email.com", "+1-555-0105", "Data Systems"),
    ("Emily", "Davis", "e.davis@email.com", "+1-555-0106", "Creative Labs"),
    ("David", "Miller", "d.miller@email.com", "+1-555-0107", "FinTech Co"),
    ("Lisa", "Wilson", "l.wilson@email.com", "+1-555-0108", "Health Plus"),
    ("James", "Taylor", "j.taylor@email.com", "+1-555-0109", "EduPro"),
    ("Maria", "Garcia", "m.garcia@email.com", "+1-555-0110", "Green Energy"),
    ("Chris", "Martinez", "c.martinez@email.com", "+1-555-0111", "BuildRight"),
    ("Anna", "Anderson", "a.anderson@email.com", "+1-555-0112", "MediaWave"),
    ("Daniel", "Thomas", "d.thomas@email.com", "+1-555-0113", "CloudNine"),
    ("Jennifer", "Jackson", "j.jackson@email.com", "+1-555-0114", "NetSphere"),
    ("Kevin", "White", "k.white@email.com", "+1-555-0115", "AutoDrive"),
]

for c in contacts:
    ws.append(c)

wb.save("contacts.xlsx")
print(f"Created contacts.xlsx with {len(contacts)} contacts")
