import mysql.connector











def registration(username, password, conn, cfg):
    cur = conn.cursor()
    cur.execute("INSERT INTO user (username, password) VALUES (%s, %s)",
                (username, password))
    conn.commit()
    cur.close()