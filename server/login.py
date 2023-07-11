




















def logging(username, password, conn, cfg):
    cur = conn.cursor()
    cur.execute('SELECT * FROM `user` WHERE `username` = %s AND `password` = %s',
                (username, password))
    a = cur.fetchone()
    cur.close()
    return a