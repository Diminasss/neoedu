from DataBaseFunk import cursor
from psycopg2 import OperationalError, IntegrityError


def user_is_in_table(login: str) -> bool | None:
    """
    Есть ли пользователь в таблице?
    :param login:
    :return:
    """
    try:
        cursor.execute(f"""SELECT EXISTS(SELECT 1 FROM users WHERE login = %s)""", (login,))
        all_users = cursor.fetchall()
        is_in_column = all_users[0][0]
        return is_in_column
    except OperationalError as e:
        print(f"ошибка обнаружения {e}")
        user_is_in_table(login)


# Метод по инициализации пользователя
def user_initialisation(login: str, password: str, last_name: str, first_name: str, patronymic: str, date_of_birth: str, department: str, is_teacher: bool, current_courses: list, completed_courses: list) -> None:
    if user_is_in_table(login):
        pass
    else:
        try:
            cursor.execute("""INSERT INTO users (login, password, last_name, first_name, patronymic, date_of_birth, department, is_teacher, current_courses, completed_courses) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (login, password, first_name, last_name, patronymic, date_of_birth, department, is_teacher, current_courses, completed_courses))
            print("Успешная ")
        except IntegrityError as e:
            print("Ошибка при инициализации:", e)


def get_all_information_from_user_exclude_password(login: str) -> dict | None:
    if user_is_in_table(login):
        cursor.execute("""SELECT login, password, last_name, first_name, patronymic, date_of_birth, department, is_teacher, current_courses, completed_courses FROM users WHERE login = %s""", (login,))
        data: tuple = cursor.fetchall()[0]
        data_to_send: dict = {"login": data[0], "password": data[1], "last_name": data[2], "first_name": data[3],
                              "patronymic": data[4], "date_of_birth": data[5], "department": data[6],
                              "is_teacher": data[7], "current_courses": data[8], "completed_courses": data[9]}
    else:
        return None
    return data_to_send


def edit_sqlite_table(table_name: str, login: str, what_to_edit: str, value: str | list | int) -> None:
    """
    Таблицы на выбор:\n
    users\n\n
    Поля на выбор:\n
    login\n
    password\n
    first_name\n
    last_name\n
    patronymic\n
    date_of_birth\n
    department\n
    is_teacher\n
    current_courses\n
    completed_courses\n
    :param table_name:
    :param login:
    :param what_to_edit:
    :param value:
    :return:
    """

    if user_is_in_table(login):
        try:
            cursor.execute(f"""UPDATE {table_name} SET {what_to_edit} = %s WHERE login = %s""", (value, login))
        except IntegrityError as e:
            print("Ошибка при редактировании:", e)
    else:
        print("Нет записи по логину")


def get_from_postgresql_table(table_name: str, login: str, what_to_get: str) -> str | list | int | bool | None:
    """Функция возвращает None, если не находит данные\n
    Таблицы на выбор:\n
    users\n\n
    Поля на выбор:\n
    login\n
    password\n
    first_name\n
    last_name\n
    patronymic\n
    date_of_birth\n
    department\n
    is_teacher\n
    current_courses\n
    completed_courses\n
    :param table_name:
    :param login:
    :param what_to_get:
    :return str | list | int | bool"""
    if user_is_in_table(login):
        try:
            cursor.execute(f"""SELECT {what_to_get} FROM {table_name} WHERE login = %s""", (login,))
            value = cursor.fetchone()[0]
            return value if value is not None else None
        except IntegrityError as e:
            print("Ошибка получения данных при подключении:", e)
            return None
    else:
        return None
