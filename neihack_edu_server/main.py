from flask import Flask, request, jsonify, wrappers
from task_checking.run_command_scr import check
import json
from config import *
from CourseBaseFunk import *
from UserBaseFunk import *
from TestBaseFunk import *


app = Flask(__name__)

# user_initialisation("2", "2", "Дима", "Никитин", "Михайлович", "2004-10-21", "ГУАП", False, [100, 101], [])
# user_initialisation("3", "3", "Дима", "Никитин", "Михайлович", "2004-10-21", "ГУАП", False, [100, 101], [])
# user_initialisation("dima88",  "123456qw", "Анна" "Ивановна" "Петрова", "1990-05-15", "Московский университет", True, [100, 101], [])
# user_initialisation("olga95",  "mypassword", "Иван" "Петрович" "Сидоров"," 1985-10-20", "Санкт-Петербургский политехнический университет", True, [100, 101], [])
# user_initialisation("sergey87",  "welcome123", "Зиноида" "Александровна" "Козлова", "1993-03-08", "Московский государственный университет", False, [100, 101], [])
# user_initialisation("natalia9",  "p@ssw0rd", "Дмитрий" "Владимирович" "Иванов", "1988-12-03", "Санкт-Петербургский государственный университет", False, [100, 101], [])
# user_initialisation("alexey98",  "secret987", "Ольга" "Николаевна" "Кузнецова", "1995-07-25", "Российский экономический университет", True, [100, 101], [])
# user_initialisation("maria83",  "ilovecoding", "Алексеевич" "Васильев", "1987-09-12", " МГТУ им. Н.Э. Баумана", True, [100, 101], [])
# user_initialisation("pavel91",  "summer2022", "Наталья" "Павловна" "Смирнова", "1992-02-18", "Санкт-Петербургский государственный университет", False, [100, 101], [])
# user_initialisation("anna1990", "pass1234", "Алексей" "Михайлович" "Попов", "1998-11-30", "Московский технический университет", False, [100, 101], [])
# user_initialisation("ivan85",  "qwerty789", "Мария" "Владимировна" "Новикова", "1983-06-10", "Уральский федеральный университет", True, [100, 101], [])
# user_initialisation("elena93", "abcde567", "Денисович" "Семенов", "1991-04-22", "Новосибирский государственный университет", False, [100, 101], [])
#
course_initialisation("Введение в программирование", "Иванов Иван", ["Группа 1", "Группа 2"], [1, 2], [1, 2])
# course_initialisation("Основы баз данных", "Петрова Ольга", ["Группа 3", "Группа 4"], ["Лекция 3", "Лекция 4"], ["Тест 3", "Тест 4"])
# course_initialisation("Математика для программистов", "Сидоров Петр", ["Группа 5", "Группа 6"], ["Лекция 5", "Лекция 6"], ["Тест 5", "Тест 6"])
# course_initialisation("Алгоритмы и структуры данных", "Козлов Дмитрий", ["Группа 7", "Группа 8"], ["Лекция 7", "Лекция 8"], ["Тест 7", "Тест 8"])
# course_initialisation("Web-разработка", "Новикова Мария", ["Группа 9", "Группа 10"], ["Лекция 9", "Лекция 10"], ["Тест 9", "Тест 10"])
# course_initialisation("Искусственный интеллект", "Васильев Сергей", ["Группа 11", "Группа 12"], ["Лекция 11", "Лекция 12"], ["Тест 11", "Тест 12"])
# course_initialisation("Безопасность в сети", "Кузнецов Алексей", ["Группа 13", "Группа 14"], ["Лекция 13", "Лекция 14"], ["Тест 13", "Тест 14"])
# course_initialisation("Мобильная разработка", "Смирнова Наталья", ["Группа 15", "Группа 16"], ["Лекция 15", "Лекция 16"], ["Тест 15", "Тест 16"])
# course_initialisation("Компьютерная графика", "Попов Павел", ["Группа 17", "Группа 18"], ["Лекция 17", "Лекция 18"], ["Тест 17", "Тест 18"])
# course_initialisation("Основы алгоритмизации", "Новосибирский государственный университет", ["Группа 19", "Группа 20"], ["Лекция 19", "Лекция 20"], ["Тест 19", "Тест 20"])


# edit_sqlite_table("users", "example@mail.com", "first_name", "Максим")
# print(get_from_postgresql_table("users", "example@mail.com", "current_courses"))
# print(user_is_in_table("example@mail.com"))
# get_all_information_from_user_exclude_password("example@mail.com")
# user_initialisation("1", "1", "Дима", "Никитин", "Михайлович", "2004-10-21", "ГУАП", False, [100, 101], [])


# Добавляем обработчик для CORS
@app.after_request
def after_request(response) -> wrappers.Response:
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    return response


@app.route("/person", methods=['POST'])
def get_person() -> tuple[wrappers.Response, int]:
    # Получаем данные из тела запроса в формате JSON
    request_data = request.get_json()

    # Извлекаем значение титла из полученных данных
    login: str = request_data.get('login')
    person_info = get_all_information_from_user_exclude_password(login)
    if person_info is not None:
        return jsonify(person_info), 200
    else:
        return jsonify({"response": "dontwork"}), 201


@app.route('/auth', methods=['POST'])
def auth() -> tuple[wrappers.Response, int]:
    # Получаем данные из тела запроса в формате JSON
    request_data = request.get_json()
    # Извлекаем значение титла из полученных данных
    login: str = request_data.get('login')
    password_from_user: str = request_data.get('password')
    if user_is_in_table(login):
        password = get_from_postgresql_table("users", login, "password")
        if password_from_user == password:
            return jsonify({'response': True}), 200
        else:
            return jsonify({'response': False}), 200
    else:
        return jsonify({'response': False}), 200


@app.route('/course', methods=['POST'])
def course() -> tuple[wrappers.Response, int]:

    request_data = request.get_json()
    login: str = request_data.get('login')
    course_ids = request_data.get('course_id')
    new_mas = []
    for course_id in course_ids:
        course_info: dict = get_all_information_from_course(course_id)
        if not(course_info is None): 
            new_mas.append(course_info)
    course_info: dict = {'login': login, 'courses': new_mas}
    if len(new_mas) > 0:
        print(course_info)
        return jsonify(course_info), 200
    else:
        return jsonify({"response": "dontwork"}), 201


@app.route('/createcourse', methods=['POST'])
def create_course() -> tuple[wrappers.Response, int]:
    course_input_info: dict = request.get_json()

    course_name: str = course_input_info.get('course_name')
    author: str = course_input_info.get('author')
    access_group: list = course_input_info.get('access_group')
    lectures_inside_course: list = course_input_info.get('lectures_inside_course')
    tests_inside_course: list = course_input_info.get('tests_inside_course')

    course_id = course_initialisation(course_name, author, access_group, lectures_inside_course, tests_inside_course, return_id=True)
    for x in access_group:
        available_courses = get_from_postgresql_table("users", x, "current_courses")
        if course_id not in available_courses:
            available_courses.append(str(course_id))
        edit_sqlite_table("users", x, "current_courses", available_courses)
    return jsonify({"response": "success"}), 200


test_initialisation("Python", "Сделайте пацанский тест", ["merge_sort([4, 2, 7, 1, 9, 5, 3, 8, 6])\n", "merge_sort([4, 2, 7, 1, 5, 3, 6])\n", "merge_sort([4, 2, 1, 5, 3, 6])\n"], ["[1, 2, 3, 4, 5, 6, 7, 8, 9]\n", "[1, 2, 3, 4, 5, 6, 7]\n", "[1, 3, 4, 5, 6]\n"])


@app.route('/checkhomework', methods=['POST'])
def check_test() -> tuple[wrappers.Response, int]:
    test_input_info: dict = request.get_json()

    test_id: int = test_input_info.get('test_id')
    user_id: int = test_input_info.get('user_id')
    repo_url: str = test_input_info.get('repo_url')

    task_input: str = get_from_postgresql_test_table("tests", test_id, "input_data")
    expected_output: str = get_from_postgresql_test_table("tests", test_id, "output_data")
    result = check(file_path=repo_url, task_input=task_input, expected_output=expected_output)
    result = str(result.count(True)) + "/" + str(len(result))
    last_result = get_from_postgresql_test_table("tests", test_id, "users_with_marks")
    if last_result is not None:
        if user_id not in last_result:
            last_result[user_id] = result
            edit_test_sqlite_table("tests", test_id, "users_with_marks", json.dumps(last_result))
        else:
            pass
    else:
        new_result = {user_id: result}
        edit_test_sqlite_table("tests", test_id, "users_with_marks", json.dumps(new_result))

    return jsonify({"response": result}), 200


# check_test(1, "2", "https://github.com/lezhev/Neo.edu")


@app.route('/test', methods=['POST'])
def get_test() -> tuple[wrappers.Response, int]:
    test_input_info: dict = request.get_json()

    test_id: int = test_input_info.get('test_id')
    user_id: str = test_input_info.get('user_id')

    test_name: str = get_from_postgresql_test_table("tests", test_id, "test_name")
    test_text: str = get_from_postgresql_test_table("tests", test_id, "test_text")
    users_with_marks: str = get_from_postgresql_test_table("tests", test_id, "users_with_marks")

    if users_with_marks is None:
        pass
    else:
        if user_id in users_with_marks:
            users_with_marks = users_with_marks[user_id]
        else:
            pass
    print(users_with_marks)
    return jsonify({"test_id": test_id, "user_id": user_id, "test_name": test_name, "test_text": test_text, "users_with_marks": users_with_marks}), 200


if __name__ == '__main__':
    app.run(debug=False)
