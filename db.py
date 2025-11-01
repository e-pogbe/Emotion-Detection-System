import sqlite3
def create_table():
    db = sqlite3.connect("emotions.db")
    c = db.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS emotions
              (result_id TEXT PRIMARY KEY,
              image_path TEXT,
              filename TEXT,
              result TEXT,  
              uploaded_at TEXT)""")
    db.commit()  # Commit the changes
    db.close()  # Ensure the database connection is closed

#result field will have to be converted into a string to be able to put it in the database using json.dumps
def save_result(result_id,image_path,filename,result,uploaded_at):
    try:
        print("Attempting to save with values:")
        print(f"result_id (type: {type(result_id)}): {result_id}")
        print(f"image_path (type: {type(image_path)}): {image_path}")
        print(f"filename (type: {type(filename)}): {filename}")
        print(f"result (type: {type(result)}): {result}")
        print(f"uploaded_at (type: {type(uploaded_at)}): {uploaded_at}")
        
        db = sqlite3.connect("emotions.db")
        c = db.cursor()
        c.execute("""INSERT INTO emotions VALUES(?,?,?,?,?)""",
                (result_id,image_path,filename,result,uploaded_at))
        db.commit()  # Commit the changes
        return True
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        print(f"Values being inserted: result_id={result_id}, image_path={image_path}, filename={filename}, result={result}, uploaded_at={uploaded_at}")
        return False
    finally:
        db.close()  # Ensure the database connection is closed

def get_result(result_id):
    db = sqlite3.connect("emotions.db")
    c = db.cursor()
    c.execute("""SELECT * FROM emotions WHERE result_id = ?""", (result_id,))
    d = c.fetchone()
    return d
#result field will have to be converted into a string to be able to put it in the database using json.dumps
def is_id_present(result_id):
    db = sqlite3.connect("emotions.db")
    c = db.cursor()
    c.execute("SELECT 1 FROM emotions WHERE result_id = ? LIMIT 1", (result_id,))
    exists = c.fetchone()
    if exists:
        return True
    return False
def get_id_data(result_id):
    import json
    db = sqlite3.connect("emotions.db")
    c = db.cursor()
    c.execute("SELECT image_path, filename, result, uploaded_at FROM emotions WHERE result_id = ?", (result_id,))
    raw = c.fetchone()
    ai_result = json.loads(raw[2])
    return_val = {'image_path': raw[0],
                  'filename': raw[1],
                  'result': ai_result,
                  'uploaded_at': raw[3]}

    return return_val
def drop_table():
    db = sqlite3.connect("emotions.db")
    c = db.cursor()
    c.execute("DROP TABLE emotions")
