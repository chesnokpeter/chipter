







def get_all_comments(idpost, conn, cfg):
    cur = conn.cursor()
    cur.execute("SELECT * FROM `comment` WHERE `idpost` = %s ORDER BY id DESC;",
                [idpost])
    messages = cur.fetchall()
    cur.close()
    return messages


def send_comment(idpost, iduser, username, text, conn, cfg):
    cur = conn.cursor()
    cur.execute("INSERT INTO `comment` (`commentText`, `idauthor`, `idpost`, `author`) VALUES (%s, %s, %s, %s);",
                (text, iduser, idpost, username))
    conn.commit()
    cur.close()