import psycopg2

try:
    conn = psycopg2.connect(host='localhost',dbname='app_database',user='postgres',password='LUG4Z1V4', port=5432)
    print('Established')

    def create_table():

        commands = (
            """
            CREATE TABLE IF NOT EXISTS users(id SERIAL PRIMARY KEY,email VARCHAR NOT NULL UNIQUE,username 
            VARCHAR NOT NULL UNIQUE, password VARCHAR NOT NULL)""",
            """
            CREATE TABLE IF NOT EXISTS question(id SERIAL PRIMARY KEY, title VARCHAR NOT NULL UNIQUE, details VARCHAR
            NOT NULL UNIQUE, date VARCHAR, author VARCHAR NOT NULL, FOREIGN KEY(author) REFERENCES users(username))""",
            """
            CREATE TABLE IF NOT EXISTS answer(answer_id SERIAL PRIMARY KEY, answer VARCHAR(1000) NOT NULL UNIQUE,
            preferred BOOLEAN DEFAULT FALSE, question_id INTEGER NOT NULL, user_name VARCHAR NOT NULL, 
            FOREIGN KEY(user_name)
            REFERENCES users(username),FOREIGN KEY(question_id) REFERENCES question(id) ON DELETE CASCADE)
            """,)
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)
        cur.close()
        conn.commit()
        conn.close()

except:

    print("I am unable to connect to the database")


if __name__ == '__main__':
    create_table()