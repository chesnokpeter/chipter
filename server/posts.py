




def get_all_posts(conn, cfg, limit=10, offset=0):
    cur = conn.cursor()
    cur.execute("SELECT * FROM post ORDER BY id DESC LIMIT %s OFFSET %s",
                (limit, offset))
    messages = cur.fetchall()
    cur.close()
    return messages



def send_post(username, content, conn, cfg):
    cur = conn.cursor()
    cur.execute("INSERT INTO post (username, content) VALUES (%s, %s)",
                (username, content))
    conn.commit()
    cur.close()