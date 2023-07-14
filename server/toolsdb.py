import mysql.connector










def get_id_from_user(username, conn):
    cur = conn.cursor()
    cur.execute('SELECT `id` FROM `user` WHERE `username` = %s', [username])
    a = cur.fetchone()
    cur.close()
    if a == None:
        return False
    return a[0]



def get_post_from_id(idpost, conn):
    cur = conn.cursor()
    cur.execute('SELECT * FROM `post` WHERE `id` = %s', [idpost])
    a = cur.fetchone()
    cur.close()
    if a == None:
        return False
    return a