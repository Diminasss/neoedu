import 'package:flutter/material.dart';
import 'package:flutter_web_plugins/flutter_web_plugins.dart';
import 'package:neohack_edu_client/colorscheme/color_schemes.g.dart';
import 'package:neohack_edu_client/pages/student/student_course.dart';
import 'package:neohack_edu_client/pages/login_page.dart';
import 'package:neohack_edu_client/pages/main_page.dart';
import 'package:neohack_edu_client/pages/student/student_courses_page.dart';
import 'package:neohack_edu_client/pages/student/student_test_page.dart';
import 'package:neohack_edu_client/pages/teacher/add_course.dart';
import 'package:neohack_edu_client/pages/teacher/teacher_course.dart';
import 'package:neohack_edu_client/pages/teacher/teacher_course_homework.dart';
import 'package:neohack_edu_client/pages/teacher/teacher_courses_page.dart';

void main() {
  setUrlStrategy(PathUrlStrategy());
  runApp(MaterialApp(
    debugShowCheckedModeBanner: false,
    theme: ThemeData(useMaterial3: true, colorScheme: lightColorScheme),
    darkTheme: ThemeData(useMaterial3: true, colorScheme: darkColorScheme),
    home: MainPage(),
    initialRoute: '/main',
    routes: {
      '/main': (context) => MainPage(),
      '/login': (context) => const LoginPage(),
      '/student_courses': (context) => CoursesPage(),
      '/teacher_courses': (context) => TeachCoursesPage(),
      '/teacher_courses/course': (context) => TeacherCourse(),
      '/teacher_courses/course/homework': (context) => HomeworkStatistic(),
      '/teacher/add_course': (context) => TeacherAddCourse(),
      '/student_courses/course': (context) => StudentCourse(),
      '/student_courses/course/homework': (context) => StudentTestPage(),
    },
  ));
}
