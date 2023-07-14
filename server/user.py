import mysql.connector








def get_posts_from_userid(userid, conn, cfg):
    cur = conn.cursor()
    cur.execute('SELECT * FROM `user` WHERE `id` = %s', 
                [userid])
    a = cur.fetchone()
    if not a:
        return False
    print(a)
    username = a[1]
    cur.execute('SELECT * FROM `post` WHERE `username` = %s', 
            [username])
    posts = cur.fetchall()
    print(posts)
    if not posts:
        return False
    return posts

