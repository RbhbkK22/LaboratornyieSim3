package ru.urfu.lab6.dao;

import org.springframework.stereotype.Repository;
import ru.urfu.lab6.entity.Student;

import java.util.List;

@Repository
public interface StudentDAO {

    List<Student> getAllStudents();

    Student saveStudent(Student student);

    Student getStudent(int id);

    int deleteStudent(int id);

}
