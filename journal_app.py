from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('journal.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('journal.db')
    c = conn.cursor()
    c.execute('SELECT id, title, content, created FROM entries ORDER BY created DESC')
    entries = c.fetchall()
    conn.close()
    return render_template('journal_index.html', entries=entries)

@app.route('/new', methods=['GET', 'POST'])
def new_entry():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        conn = sqlite3.connect('journal.db')
        c = conn.cursor()
        c.execute('INSERT INTO entries (title, content) VALUES (?, ?)', (title, content))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('journal_new.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
