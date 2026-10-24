package ru.urfu.lab6.service;

import org.springframework.stereotype.Service;
import ru.urfu.lab6.entity.Discipline;

import java.util.List;

@Service
public interface DisciplineService {
    List<Discipline> getAllDisciplines();

    Discipline saveDiscipline(Discipline discipline);

    Discipline getDiscipline(int id);

    boolean deleteDiscipline(int id);
}
