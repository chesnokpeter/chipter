import mysql.connector




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




def get_last_id_post(conn, cfg):
    cur = conn.cursor()
    cur.execute("SELECT LAST_INSERT_ID(Id) from post order by LAST_INSERT_ID(Id) desc limit 1;")
    a = cur.fetchone()
    cur.close()
    return a


def get_username_from_id_post(idpost, conn, cfg):
    cur = conn.cursor()
    cur.execute("SELECT * FROM `post` WHERE `id` = %s",
                [idpost])
    a = cur.fetchone()
    cur.close()
    if not a:
        return False
    return a[2]