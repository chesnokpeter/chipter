




















def logging(username, conn, cfg):
    cur = conn.cursor()
    cur.execute('SELECT * FROM `user` WHERE `username` = %s',
                [username])
    a = cur.fetchone()
    cur.close()
    return a[2]