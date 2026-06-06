"""Build a single self-contained index.html with embedded contact data."""
import json

with open("contacts.json", "r") as f:
    contacts_json = f.read()

html = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>Contact Search</title>
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --bg: #f5f5f7;
  --card: #ffffff;
  --text: #1d1d1f;
  --muted: #6e6e73;
  --accent: #0071e3;
  --accent-hover: #0077ed;
  --green: #30d158;
  --green-hover: #28b84c;
  --border: #d2d2d7;
  --radius: 12px;
  --shadow: 0 1px 3px rgba(0,0,0,0.08);
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
  min-height: 100dvh;
  padding: 12px;
  -webkit-text-size-adjust: 100%;
}

.header {
  position: sticky;
  top: 0;
  z-index: 10;
  background: var(--bg);
  padding: 8px 0 4px;
}

.search-bar input {
  width: 100%;
  padding: 14px 16px;
  font-size: 17px;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: var(--card);
  outline: none;
  transition: border-color 0.2s;
}

.search-bar input:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px rgba(0,113,227,0.15);
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 4px;
}

.stats {
  font-size: 13px;
  color: var(--muted);
}

.btn-export {
  display: none;
  padding: 6px 12px;
  font-size: 12px;
  font-weight: 600;
  border: 1px solid var(--accent);
  border-radius: 8px;
  background: transparent;
  color: var(--accent);
  cursor: pointer;
  transition: all 0.2s;
}

.btn-export:hover {
  background: var(--accent);
  color: #fff;
}

.btn-export.visible { display: inline-block; }

.results {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.contact-card {
  background: var(--card);
  border-radius: var(--radius);
  padding: 14px 16px;
  box-shadow: var(--shadow);
  display: flex;
  flex-wrap: wrap;
}

.contact-row {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  width: 100%;
}

.contact-info {
  flex: 1;
  min-width: 0;
}

.contact-name {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 1px;
  word-break: break-word;
}

.contact-title {
  font-size: 13px;
  color: var(--accent);
  margin-bottom: 4px;
}

.contact-company {
  font-size: 13px;
  font-weight: 500;
  margin-bottom: 4px;
}

.contact-meta {
  font-size: 12px;
  color: var(--muted);
  line-height: 1.5;
  word-break: break-word;
}

.contact-meta span {
  display: inline-block;
  margin-right: 10px;
}

.contact-actions {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 6px;
  flex-shrink: 0;
}

.btn-interested {
  padding: 8px 14px;
  font-size: 13px;
  font-weight: 600;
  border: none;
  border-radius: 8px;
  background: var(--green);
  color: #fff;
  cursor: pointer;
  white-space: nowrap;
  transition: background 0.2s;
}

.btn-interested:hover { background: var(--green-hover); }
.btn-interested:disabled {
  background: var(--border);
  color: var(--muted);
  cursor: default;
}

.comment-area {
  display: none;
  flex-direction: column;
  gap: 6px;
  width: 100%;
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px solid var(--border);
}

.comment-area.open { display: flex; }

.comment-area textarea {
  width: 100%;
  padding: 8px 12px;
  font-size: 14px;
  border: 1px solid var(--border);
  border-radius: 8px;
  resize: vertical;
  min-height: 40px;
  font-family: inherit;
  outline: none;
}

.comment-area textarea:focus { border-color: var(--accent); }

.comment-btns {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
}

.btn-submit {
  padding: 8px 16px;
  font-size: 13px;
  font-weight: 600;
  border: none;
  border-radius: 8px;
  background: var(--accent);
  color: #fff;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-submit:hover { background: var(--accent-hover); }

.btn-cancel {
  padding: 8px 16px;
  font-size: 13px;
  font-weight: 500;
  border: 1px solid var(--border);
  border-radius: 8px;
  background: var(--card);
  color: var(--text);
  cursor: pointer;
}

.toast {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%) translateY(80px);
  background: #1d1d1f;
  color: #fff;
  padding: 10px 20px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 500;
  opacity: 0;
  transition: all 0.3s ease;
  z-index: 100;
  pointer-events: none;
}

.toast.show {
  transform: translateX(-50%) translateY(0);
  opacity: 1;
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: var(--muted);
  font-size: 15px;
  line-height: 1.6;
}

.marked-badge {
  display: inline-block;
  font-size: 11px;
  font-weight: 600;
  color: var(--green);
  background: rgba(48,209,88,0.1);
  padding: 2px 8px;
  border-radius: 6px;
  margin-top: 4px;
}

mark {
  background: rgba(0,113,227,0.15);
  color: inherit;
  padding: 0 1px;
  border-radius: 2px;
}

@media (orientation: landscape) {
  body { padding: 8px 16px; }
  .results {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
    gap: 8px;
  }
  .contact-card { padding: 12px 14px; }
}

@media (min-width: 768px) {
  body { max-width: 1000px; margin: 0 auto; padding: 16px 24px; }
  .results {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(420px, 1fr));
    gap: 10px;
  }
}
</style>
</head>
<body>

<div class="header">
  <div class="search-bar">
    <input type="text" id="searchInput" placeholder="Type at least 3 characters to search..." autocomplete="off" autofocus>
  </div>
  <div class="toolbar">
    <div class="stats" id="stats"></div>
    <button class="btn-export" id="exportBtn" onclick="exportInterested()">Export Interested List</button>
  </div>
</div>
<div class="results" id="results">
  <div class="empty-state">Type at least 3 characters to search.</div>
</div>
<div class="toast" id="toast"></div>

<script>
const allContacts = CONTACT_DATA_PLACEHOLDER;

let interestedMap = {};
try {
  interestedMap = JSON.parse(localStorage.getItem('interested') || '{}');
} catch(e) {}

function updateExportBtn() {
  const btn = document.getElementById('exportBtn');
  const count = Object.keys(interestedMap).length;
  if (count > 0) {
    btn.classList.add('visible');
    btn.textContent = 'Export Interested (' + count + ')';
  } else {
    btn.classList.remove('visible');
  }
}

function saveInterested() {
  localStorage.setItem('interested', JSON.stringify(interestedMap));
  updateExportBtn();
}

function escHtml(s) {
  const d = document.createElement('div');
  d.textContent = s;
  return d.innerHTML;
}

function highlight(text, query) {
  if (!query || !text) return escHtml(text || '');
  const terms = query.split(/\\s+/).filter(Boolean);
  let result = escHtml(text);
  terms.forEach(term => {
    const escaped = term.replace(/[.*+?^${}()|[\\]\\\\]/g, '\\\\$&');
    result = result.replace(new RegExp('(' + escaped + ')', 'gi'), '<mark>$1</mark>');
  });
  return result;
}

function val(contact, key) {
  return (contact[key] || '').trim();
}

function render(contacts, query) {
  const container = document.getElementById('results');
  const stats = document.getElementById('stats');

  if (!query) {
    container.innerHTML = '<div class="empty-state">Type at least 3 characters to search.</div>';
    stats.textContent = allContacts.length.toLocaleString() + ' contacts loaded';
    return;
  }

  stats.textContent = contacts.length + ' result' + (contacts.length !== 1 ? 's' : '') + ' found';

  if (contacts.length === 0) {
    container.innerHTML = '<div class="empty-state">No contacts match your search.</div>';
    return;
  }

  container.innerHTML = contacts.map(c => {
    const firstName = val(c, 'first name');
    const lastName = val(c, 'last name');
    const fullName = [firstName, lastName].filter(Boolean).join(' ') || val(c, 'contact name') || 'Unnamed';
    const title = val(c, 'title');
    const company = val(c, 'company name');
    const email = val(c, 'email');
    const phone = val(c, 'phone');
    const city = val(c, 'city');
    const country = val(c, 'country');
    const location = [city, country].filter(Boolean).join(', ');
    const isMarked = !!interestedMap[c._id];

    return '<div class="contact-card" data-id="' + c._id + '">' +
      '<div class="contact-row">' +
        '<div class="contact-info">' +
          '<div class="contact-name">' + highlight(fullName, query) + '</div>' +
          (title ? '<div class="contact-title">' + escHtml(title) + '</div>' : '') +
          (company ? '<div class="contact-company">' + escHtml(company) + '</div>' : '') +
          '<div class="contact-meta">' +
            (email ? '<span>' + escHtml(email) + '</span>' : '') +
            (phone ? '<span>' + escHtml(phone) + '</span>' : '') +
            (location ? '<span>' + escHtml(location) + '</span>' : '') +
          '</div>' +
          (isMarked ? '<span class="marked-badge">INTERESTED</span>' : '') +
        '</div>' +
        '<div class="contact-actions">' +
          '<button class="btn-interested" onclick="toggleComment(' + c._id + ')" ' + (isMarked ? 'disabled' : '') + '>' +
            (isMarked ? 'Saved' : 'INTERESTED') +
          '</button>' +
        '</div>' +
      '</div>' +
      '<div class="comment-area" id="comment-' + c._id + '">' +
        '<textarea placeholder="Add a comment (optional)..." id="textarea-' + c._id + '"></textarea>' +
        '<div class="comment-btns">' +
          '<button class="btn-cancel" onclick="toggleComment(' + c._id + ')">Cancel</button>' +
          '<button class="btn-submit" onclick="submitInterested(' + c._id + ')">Submit</button>' +
        '</div>' +
      '</div>' +
    '</div>';
  }).join('');
}

function toggleComment(id) {
  const el = document.getElementById('comment-' + id);
  el.classList.toggle('open');
  if (el.classList.contains('open')) {
    el.querySelector('textarea').focus();
  }
}

function submitInterested(id) {
  const contact = allContacts.find(c => c._id === id);
  if (!contact) return;
  const comment = document.getElementById('textarea-' + id).value.trim();
  const now = new Date();
  const timestamp = now.getFullYear() + '-' +
    String(now.getMonth()+1).padStart(2,'0') + '-' +
    String(now.getDate()).padStart(2,'0') + ' ' +
    String(now.getHours()).padStart(2,'0') + ':' +
    String(now.getMinutes()).padStart(2,'0') + ':' +
    String(now.getSeconds()).padStart(2,'0');

  interestedMap[id] = {
    contact: {
      name: [val(contact,'first name'), val(contact,'last name')].filter(Boolean).join(' '),
      title: val(contact,'title'),
      company: val(contact,'company name'),
      email: val(contact,'email'),
      phone: val(contact,'phone'),
      city: val(contact,'city'),
      country: val(contact,'country'),
      linkedin: val(contact,'person linkedin url')
    },
    comment: comment,
    timestamp: timestamp
  };
  saveInterested();
  showToast('Contact saved!');
  const query = document.getElementById('searchInput').value.trim().toLowerCase();
  if (query) render(filterContacts(query), query);
}

function filterContacts(query) {
  const terms = query.split(/\\s+/);
  return allContacts.filter(c => {
    const searchable = [
      (c['first name'] || ''),
      (c['last name'] || ''),
      (c['contact name'] || '')
    ].join(' ').toLowerCase();
    return terms.every(t => searchable.includes(t));
  });
}

function exportInterested() {
  const entries = Object.values(interestedMap);
  if (entries.length === 0) return;

  let csv = 'Name,Title,Company,Email,Phone,City,Country,LinkedIn,Comment,Timestamp\\n';
  entries.forEach(e => {
    const c = e.contact;
    const row = [c.name, c.title, c.company, c.email, c.phone, c.city, c.country, c.linkedin, e.comment, e.timestamp];
    csv += row.map(v => '"' + (v||'').replace(/"/g, '""') + '"').join(',') + '\\n';
  });

  const blob = new Blob([csv], { type: 'text/csv' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'interested_contacts.csv';
  a.click();
  URL.revokeObjectURL(url);
  showToast('CSV downloaded!');
}

let debounceTimer;
document.getElementById('searchInput').addEventListener('input', function() {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(() => {
    const query = this.value.trim().toLowerCase();
    if (query.length >= 3) {
      render(filterContacts(query), query);
    } else {
      render([], '');
    }
  }, 100);
});

function showToast(msg) {
  const toast = document.getElementById('toast');
  toast.textContent = msg;
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 2000);
}

document.getElementById('stats').textContent = allContacts.length.toLocaleString() + ' contacts loaded';
updateExportBtn();
</script>
</body>
</html>'''

html = html.replace('CONTACT_DATA_PLACEHOLDER', contacts_json)

with open("index.html", "w") as f:
    f.write(html)

import os
size = os.path.getsize("index.html")
print(f"Built index.html: {size:,} bytes ({size/1024/1024:.1f} MB)")
