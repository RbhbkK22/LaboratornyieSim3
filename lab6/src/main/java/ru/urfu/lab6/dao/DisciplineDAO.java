package ru.urfu.lab6.dao;

import org.springframework.stereotype.Repository;
import ru.urfu.lab6.entity.Discipline;

import java.util.List;

@Repository
public interface DisciplineDAO {

    List<Discipline> getAllDisciplines();

    Discipline saveDiscipline(Discipline discipline);

    Discipline getDiscipline(int id);

    int deleteDiscipline(int id);

}
