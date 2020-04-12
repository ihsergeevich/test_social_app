async def get_admin(connection, login):
    sql = f"""
        SELECT id, password_hash, role FROM users WHERE email='{login}';
        """
    return await connection.fetchrow(sql)
