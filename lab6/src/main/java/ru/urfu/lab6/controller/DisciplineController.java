package ru.urfu.lab6.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import ru.urfu.lab6.dto.OperationResult;
import ru.urfu.lab6.entity.Discipline;
import ru.urfu.lab6.service.DisciplineService;

import java.util.List;

@RestController
@RequestMapping("/api")
public class DisciplineController {

    @Autowired
    private DisciplineService disciplineService;

    @GetMapping("/disciplines")
    public ResponseEntity<OperationResult<List<Discipline>>> allDisciplines() {
        List<Discipline> allDisciplines = disciplineService.getAllDisciplines();
        return ResponseEntity.ok(OperationResult.success("Найдено дисциплин: " + allDisciplines.size(), allDisciplines));
    }

    @GetMapping("/disciplines/{id}")
    public ResponseEntity<OperationResult<Discipline>> getDiscipline(@PathVariable("id") int id) {
        Discipline discipline = disciplineService.getDiscipline(id);
        if (discipline == null) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND)
                    .body(OperationResult.failed("Дисциплина с id=" + id + " не найдена"));
        }
        return ResponseEntity.ok(OperationResult.success("Дисциплина найдена", discipline));
    }

    @PostMapping("/disciplines")
    public ResponseEntity<OperationResult<Discipline>> saveDiscipline(@RequestBody Discipline discipline) {
        Discipline saved = disciplineService.saveDiscipline(discipline);
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(OperationResult.success("Дисциплина добавлена", saved));
    }

    @PutMapping("/disciplines")
    public ResponseEntity<OperationResult<Discipline>> updateDiscipline(@RequestBody Discipline discipline) {
        if (disciplineService.getDiscipline(discipline.getId()) == null) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND)
                    .body(OperationResult.failed("Дисциплина с id=" + discipline.getId() + " не найдена"));
        }
        Discipline updated = disciplineService.saveDiscipline(discipline);
        return ResponseEntity.ok(OperationResult.success("Дисциплина изменена", updated));
    }

    @DeleteMapping("/disciplines/{id}")
    public ResponseEntity<OperationResult<Void>> deleteDiscipline(@PathVariable("id") int id) {
        if (!disciplineService.deleteDiscipline(id)) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND)
                    .body(OperationResult.failed("Дисциплина с id=" + id + " не найдена"));
        }
        return ResponseEntity.ok(OperationResult.success("Дисциплина с id=" + id + " удалена", null));
    }
}
