async def get_all_users(connection):
    sql = f"""
        SELECT id, email, created, firstname, lastname, about_me FROM users;
        """
    return [dict(x) for x in await connection.fetch(sql)]


async def get_user(connection, user_id):
    sql = f"""
        SELECT * FROM users WHERE users.id = {user_id} LIMIT 1;
        """
    return await connection.fetchrow(sql)


async def edit_user(connection, user_id, email, firstname, lastname):
    sql = f"""
        UPDATE users 
        SET 
            email = '{email}',
            firstname = '{firstname}',
            lastname = '{lastname}'
        WHERE users.id = {user_id};      
        """
    return await connection.execute(sql)
