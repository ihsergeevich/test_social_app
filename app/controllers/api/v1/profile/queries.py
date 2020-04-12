async def get_all_users(connection, user_id):
    sql = f"""
        SELECT firstname, lastname,  about_me FROM users WHERE id != {user_id};
        """
    return [dict(x) for x in await connection.fetch(sql)]


async def get_user(connection, user_id):
    sql = f"""
        SELECT firstname, lastname,  about_me FROM users WHERE id={user_id};
        """
    return await connection.fetchrow(sql)
