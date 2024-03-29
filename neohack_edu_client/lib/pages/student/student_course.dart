import 'dart:convert';
import 'dart:developer';
import 'package:http/http.dart' as http;
import 'package:flutter/material.dart';
import 'package:gradient_borders/box_borders/gradient_box_border.dart';
import 'package:neohack_edu_client/classes/person.dart';

class StudentCourse extends StatelessWidget {
  StudentCourse({super.key, person, courseId});

  Person? person;

  int? courseId;

  @override
  Widget build(BuildContext context) {
    final arguments = (ModalRoute.of(context)?.settings.arguments ??
        {'person': null, 'id': 0}) as Map<String, dynamic>;

    if (arguments['person'] == null ||
        arguments['id'] == 0 ||
        arguments['id'] == null) {
      return _notLogged(context);
    }

    person = arguments['person'];
    courseId = arguments['id'];

    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        surfaceTintColor: Colors.transparent,
        shadowColor: Colors.transparent,
        foregroundColor: Colors.transparent,
        flexibleSpace: Container(
          height: 100,
          decoration: const BoxDecoration(
              gradient: LinearGradient(
                  begin: Alignment.topCenter,
                  end: Alignment.bottomCenter,
                  colors: <Color>[
                Color.fromRGBO(40, 1, 84, 1),
                Color.fromRGBO(75, 0, 95, 81),
              ])),
        ),
        title: SizedBox(
          width: MediaQuery.of(context).size.width,
          height: 60,
          child: FittedBox(
            fit: BoxFit.contain,
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.end,
              children: [
                Image.asset(
                  '../assets/icons/neoflex_logo.png',
                  fit: BoxFit.fitHeight,
                  height: 80,
                ),
                const SizedBox(width: 10),
                const Text(
                  'Neo.edu',
                  style: TextStyle(fontSize: 60, color: Colors.white),
                ),
                SizedBox(
                  width: MediaQuery.of(context).size.width - 300,
                ),
                Text('${person!.firstName} ${person!.lastName}',
                    style: const TextStyle(
                      fontSize: 40,
                      color: Colors.white,
                    )),
              ],
            ),
          ),
        ),
        automaticallyImplyLeading: false,
        toolbarHeight: 100,
      ),
      backgroundColor: Colors.white,
      body: SafeArea(
        minimum: const EdgeInsets.only(left: 30, right: 30),
        child: ListView(
          children: [
            const SizedBox(
              height: 60,
            ),
            FutureBuilder(
              future: getCoursesName('l', courseId),
              builder: (context, snapshot) {
                if (snapshot.connectionState != ConnectionState.done) {
                  return const CircularProgressIndicator();
                }
                if (snapshot.hasError) {
                  return Text(snapshot.error.toString());
                }
                var courseInfo = snapshot.data[0];
                return Column(
                  children: [
                    FittedBox(
                      fit: BoxFit.scaleDown,
                      child: UnconstrainedBox(
                        child: Container(
                          height: 150,
                          width: 500,
                          decoration: BoxDecoration(
                            borderRadius: BorderRadius.circular(40),
                            gradient: const LinearGradient(
                                begin: Alignment.topCenter,
                                end: Alignment.bottomCenter,
                                colors: <Color>[
                                  Color.fromRGBO(115, 57, 130, 1),
                                  Color.fromRGBO(254, 73, 154, 1),
                                ]),
                          ),
                          alignment: Alignment.center,
                          child: Text(
                            courseInfo['course_name'],
                            textAlign: TextAlign.center,
                            style: const TextStyle(
                              color: Colors.white,
                              fontSize: 30,
                            ),
                          ),
                        ),
                      ),
                    ),
                    const SizedBox(
                      height: 50,
                    ),
                    _myListView(courseInfo, person!),
                  ],
                );
              },
            ),
          ],
        ),
      ),
    );
  }
}

AlertDialog _notLogged(BuildContext context) {
  return AlertDialog(
    content: const Text('you are not logged in, please try again'),
    title: const Text('Error'),
    actions: [
      TextButton(
          onPressed: () {
            Navigator.pushNamedAndRemoveUntil(
                context, '/main', (route) => false);
          },
          child: const Text('Go to main'))
    ],
  );
}

Future<dynamic> getCoursesName(login, courseId) async {
  final response = await http.post(
    Uri.parse('http://localhost:5000/course'),
    headers: <String, String>{
      'Content-Type': 'application/json; charset=UTF-8',
    },
    body: jsonEncode(<String, dynamic>{
      'login': login,
      'course_id': [courseId],
    }),
  );

  if (response.statusCode == 200) {
    var answer = List.from(jsonDecode(response.body)['courses']);
    return answer;
  } else {
    throw Exception('Failed to fetch data.');
  }
}

Widget _myListView(Map<dynamic, dynamic> courseInfo, Person person) {
  String str = (courseInfo['tests_inside_course']);
  // Удаляем фигурные скобки и разделяем строку по запятым
  List<String> parts = str.replaceAll("{", "").replaceAll("}", "").split(",");

  // Преобразуем каждую часть в целое число и создаем список
  List<int> numbers = parts.map((e) => int.parse(e.trim())).toList();

  log(numbers.length.toString());

  final List<ListItem> items = List<ListItem>.generate(numbers.length * 3, (i) {
    if (i % 3 == 0) {
      return MessageHeader(
          message: courseInfo['lectures_inside_course'][i ~/ 3].toString());
    } else if (i % 3 == 1) {
      return MessageLectureItem();
    } else {
      return MessageTestItem(testId: numbers[i ~/ 3]);
      //return MessageTestItem(testId: courseInfo['tests_inside_course'][i ~/ 3]);
    }
  });
  return ListView.builder(
    itemCount: numbers.length * 3,
    scrollDirection: Axis.vertical,
    shrinkWrap: true,
    itemBuilder: ((context, index) {
      final item = items[index];

      if (item is MessageHeader) {
        return Column(
          children: [
            ListTile(
              title: Text(
                item.message.replaceAll(RegExp(r"[']"), ''),
                style: const TextStyle(color: Colors.pink, fontSize: 30),
              ),
            ),
            Divider(
              color: Colors.pink[300],
              height: 0,
              thickness: 3,
              indent: 10,
              endIndent: 10,
            )
          ],
        );
      }
      if (item is MessageLectureItem) {
        return const ListTile(
          leading: Icon(Icons.import_contacts),
          title: Text(
            'Теоретическая часть',
            style: TextStyle(color: Colors.purple, fontSize: 20),
          ),
        );
      }
      if (item is MessageTestItem) {
        return GestureDetector(
          onTap: () {
            Navigator.pushNamed(context, '/student_courses/course/homework',
                arguments: {'person': person, 'id': item.testId});
          },
          child: const ListTile(
            leading: Icon(Icons.laptop_mac),
            title: Text(
              'Домашнее задание',
              style: TextStyle(color: Colors.purple, fontSize: 20),
            ),
          ),
        );
      }
    }),
  );
}

abstract class ListItem {}

class MessageHeader implements ListItem {
  final String message;
  MessageHeader({required this.message});
}

class MessageLectureItem implements ListItem {
  MessageLectureItem();
}

class MessageTestItem implements ListItem {
  final int testId;
  MessageTestItem({required this.testId});
}
