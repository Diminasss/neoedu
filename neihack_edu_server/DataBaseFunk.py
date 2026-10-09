import psycopg2
from config import username, password, host, port, database_name


# Инициализация БД
def database_connection() -> psycopg2.connect:
    try:
        connection = psycopg2.connect(user=username, password=password, host=host, port=port,
                                      database=database_name)
        connection.autocommit = True
        cursor = connection.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS users(
        login varchar(100) PRIMARY KEY,
        password varchar(20) NOT NULL,
        last_name varchar(100) NOT NULL,
        first_name varchar(100) NOT NULL,
        patronymic varchar(100) NOT NULL,
        date_of_birth date NOT NULL,
        department varchar(100) NOT NULL,
        is_teacher boolean NOT NULL,
        current_courses VARCHAR(255) ARRAY,
        completed_courses VARCHAR(255) ARRAY)""")

        print("Успешное создание/подключение к таблице пользователя")

        cursor.execute("""CREATE TABLE IF NOT EXISTS course(
        course_id integer PRIMARY KEY,
        course_name varchar(70),
        author varchar(100) NOT NULL,
        access_group varchar(100) ARRAY,
        lectures_inside_course varchar(100) ARRAY,
        tests_inside_course integer ARRAY)""")

        print("Успешное создание/подключение к таблице курса")

        cursor.execute("""CREATE TABLE IF NOT EXISTS tests(
                test_id integer PRIMARY KEY,
                test_name varchar(100),
                test_text varchar(10000) NOT NULL,
                input_data varchar(10000) ARRAY,
                output_data varchar(10000) ARRAY,
                users_with_marks JSONB)""")

        return cursor
    except psycopg2.OperationalError as e:
        print("Ошибка при подключении к базе данных:", e)


cursor = database_connection()









