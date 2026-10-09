from DataBaseFunk import cursor
from psycopg2 import IntegrityError, OperationalError


def test_initialisation(test_name: str, test_text: str, input_data: list, output_data: list) -> None:
    try:
        cursor.execute("""SELECT EXISTS (SELECT 1 FROM tests);""")
    except OperationalError as e:
        print("Ошибка доступа к базе в инициализации", e)
    table_is_empty: bool = not (cursor.fetchone()[0])
    if table_is_empty:
        test_id = 1
    else:
        cursor.execute("""SELECT MAX(test_id) FROM tests;""")
        test_id = cursor.fetchone()[0] + 1
    try:
        cursor.execute(
            """INSERT INTO tests (test_id, test_name, test_text, input_data, output_data) VALUES (%s, %s, %s, %s, %s)""",
            (test_id, test_name, test_text, input_data, output_data))
    except IntegrityError as e:
        print(e)


def edit_test_sqlite_table(table_name: str, key: int, what_to_edit: str, value) -> None:
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
    :param key:
    :param what_to_edit:
    :param value:
    :return:
    """
    try:
        cursor.execute(f"""UPDATE {table_name} SET {what_to_edit} = %s WHERE test_id = %s""", (value, key))
    except IntegrityError as e:
        print("Ошибка при редактировании:", e)


def get_from_postgresql_test_table(table_name: str, key: int, what_to_get: str) -> str | list | int | bool | None:
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
    :param key:
    :param what_to_get:
    :return str | list | int | bool"""
    try:
        cursor.execute(f"""SELECT {what_to_get} FROM {table_name} WHERE test_id = %s""", (key,))
        value = cursor.fetchone()[0]
        return value if value is not None else None
    except IntegrityError as e:
        print("Ошибка получения данных при подключении:", e)
        return None