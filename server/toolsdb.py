import mysql.connector










def get_id_from_user(username, conn):
    cur = conn.cursor()
    cur.execute('SELECT `id` FROM `user` WHERE `username` = %s', [username])
    a = cur.fetchone()
    cur.close()
    if a == None:
        return False
    return a[0]

