import os
import psycopg2
from flask import Flask, request, redirect

app = Flask(__name__)

DB_URL = os.getenv("DB_URL", "postgresql://postgres:password@localhost:5432/postgres")

def get_db():
    return psycopg2.connect(DB_URL)

# with get_db() as conn, conn.cursor() as cur:
#     cur.execute("CREATE TABLE IF NOT EXISTS messages (id SERIAL PRIMARY KEY, content TEXT);")
#     conn.commit()

@app.route("/", methods=["GET", "POST"])
def index():
    name = os.getenv("USER_NAME", "Guest")
    
    with get_db() as conn, conn.cursor() as cur:
        if request.method == "POST":
            if "clear" in request.form:
                cur.execute("DELETE FROM messages;")
            else:
                new_text = request.form.get("user_text", "")
                if new_text: 
                    cur.execute("INSERT INTO messages (content) VALUES (%s);", (new_text,))
            
            conn.commit()
            return redirect("/")

        cur.execute("SELECT content FROM messages ORDER BY id DESC LIMIT 10;")
        recent_texts = cur.fetchall()

    list_items = "".join([f"<li>{txt[0]}</li>" for txt in recent_texts])

    return f"""
        <h1>Hi {name}</h1>
        <form method="POST">
            <input type="text" name="user_text" placeholder="Type something..." required>
            <button type="submit">Add to List</button>
        </form>
        
        <h3>Recent Texts:</h3>
        <ul>{list_items or "<li>No entries yet.</li>"}</ul>

        <hr>
        <form method="POST">
            <button type="submit" name="clear" value="true" style="color: red;">Clear All</button>
        </form>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)