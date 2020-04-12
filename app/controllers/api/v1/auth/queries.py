async def get_user(cursor, login):
    sql = f"""
        SELECT id, password_hash
        FROM users
        WHERE
            users.email='{login}'
        LIMIT 1;            
        """
    return await cursor.fetchrow(sql)
