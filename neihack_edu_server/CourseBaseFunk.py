from DataBaseFunk import cursor
from psycopg2 import IntegrityError, OperationalError


def course_initialisation(course_name: str, author: str, access_group: list, lectures_inside_course: list, tests_inside_course: list, return_id: bool = False) -> None | int:
    """
    Функция инициализации курса
    :param course_name:
    :param author:
    :param access_group:
    :param lectures_inside_course:
    :param tests_inside_course:
    :param return_id:
    :return:
    """
    try:
        cursor.execute("""SELECT EXISTS (SELECT 1 FROM course);""")
    except OperationalError as e:
        print("Ошибка доступа к базе в инициализации")
    table_is_empty: bool = not (cursor.fetchone()[0])
    if table_is_empty:
        course_id = 1
    else:
        cursor.execute("""SELECT MAX(course_id) FROM course;""")
        course_id = cursor.fetchone()[0] + 1
    try:
        cursor.execute(
            """INSERT INTO course (course_id, course_name, author, access_group, lectures_inside_course, tests_inside_course) VALUES (%s, %s, %s, %s, %s, %s)""",
            (course_id, course_name, author, access_group, lectures_inside_course, tests_inside_course))
    except IntegrityError as e:
        print(e)

    if return_id:
        return course_id


def course_is_in_table(course_id: int) -> bool:
    """
    Есть ли курс в таблице?
    :param course_id:
    :return:
    """
    try:
        cursor.execute(f"""SELECT EXISTS(SELECT 1 FROM course WHERE course_id = %s)""", (course_id,))
        all_users = cursor.fetchall()
        is_in_column = all_users[0][0]
        return is_in_column
    except OperationalError as e:
        print(f"ошибка обнаружения курса {e}")
        course_is_in_table(course_id)


def get_all_information_from_course(course_id: int) -> dict | None:
    if course_is_in_table(course_id):
        try:
            cursor.execute("""SELECT course_id, course_name, author, access_group, lectures_inside_course, tests_inside_course FROM course WHERE course_id = %s""", (course_id,))
        except OperationalError as e:
            print(e)
        data: tuple = cursor.fetchall()[0]
        print(data)
        data_to_send: dict = {"course_id": data[0], "course_name": data[1], "author": data[2], "access_group": data[3], "lectures_inside_course": data[4], "tests_inside_course": data[5]}
        print(data_to_send)
        return data_to_send
    else:
        return 
