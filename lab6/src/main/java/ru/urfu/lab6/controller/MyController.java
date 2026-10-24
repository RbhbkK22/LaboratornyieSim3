package ru.urfu.lab6.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import ru.urfu.lab6.dto.OperationResult;
import ru.urfu.lab6.entity.Student;
import ru.urfu.lab6.service.StudentService;

import java.util.List;

@RestController
@RequestMapping("/api")
public class MyController {

    @Autowired
    private StudentService studentService;

    @GetMapping("/students")
    public ResponseEntity<OperationResult<List<Student>>> allStudents() {
        List<Student> allStudents = studentService.getAllStudents();
        return ResponseEntity.ok(OperationResult.success("Найдено студентов: " + allStudents.size(), allStudents));
    }

    @GetMapping("/students/{id}")
    public ResponseEntity<OperationResult<Student>> getStudent(@PathVariable("id") int id) {
        Student student = studentService.getStudent(id);
        if (student == null) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND)
                    .body(OperationResult.failed("Студент с id=" + id + " не найден"));
        }
        return ResponseEntity.ok(OperationResult.success("Студент найден", student));
    }

    @PostMapping("/students")
    public ResponseEntity<OperationResult<Student>> saveStudent(@RequestBody Student student) {
        Student saved = studentService.saveStudent(student);
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(OperationResult.success("Студент добавлен", saved));
    }

    @PutMapping("/students")
    public ResponseEntity<OperationResult<Student>> updateStudent(@RequestBody Student student) {
        if (studentService.getStudent(student.getId()) == null) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND)
                    .body(OperationResult.failed("Студент с id=" + student.getId() + " не найден"));
        }
        Student updated = studentService.saveStudent(student);
        return ResponseEntity.ok(OperationResult.success("Студент изменён", updated));
    }

    @DeleteMapping("/students/{id}")
    public ResponseEntity<OperationResult<Void>> deleteStudent(@PathVariable("id") int id) {
        if (!studentService.deleteStudent(id)) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND)
                    .body(OperationResult.failed("Студент с id=" + id + " не найден"));
        }
        return ResponseEntity.ok(OperationResult.success("Студент с id=" + id + " удалён", null));
    }
}
