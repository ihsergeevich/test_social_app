async def check_user(connection, login):
    sql = f"""
        SELECT *
        FROM users
        WHERE
            email='{login}'
        LIMIT 1;
        """
    return await connection.fetchrow(sql)


async def check_user_by_id(connection, user_id):
    sql = f"""
        SELECT *
        FROM users
        WHERE
            id='{user_id}'
        """
    return await connection.fetchrow(sql)


async def create_user(connection, login, password_hash):
    sql = f"""
        INSERT INTO users(email, password_hash, role)
        VALUES
            ('{login}', '{password_hash}', 'USER');
        """
    return await connection.execute(sql)


async def create_profile(connection, firstname, lastname, about_me, user_id):
    sql = f"""
        UPDATE users
        SET
            firstname = '{firstname}',
            lastname = '{lastname}',
            about_me = '{about_me}'
        WHERE
            users.id = {user_id};
        """

    return await connection.execute(sql)
