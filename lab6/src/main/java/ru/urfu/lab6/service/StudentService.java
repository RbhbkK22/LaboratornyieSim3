package ru.urfu.lab6.service;

import org.springframework.stereotype.Service;
import ru.urfu.lab6.entity.Student;

import java.util.List;

@Service
public interface StudentService {
    List<Student> getAllStudents();

    Student saveStudent(Student student);

    Student getStudent(int id);

    boolean deleteStudent(int id);
}
