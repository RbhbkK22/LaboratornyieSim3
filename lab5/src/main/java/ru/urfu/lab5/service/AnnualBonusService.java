package ru.urfu.lab5.service;

import org.springframework.stereotype.Service;
import ru.urfu.lab5.model.Positions;

@Service
public interface AnnualBonusService {

    double calculate(Positions positions, double salary, double bonus, int workDays);

    double calculate(Positions positions, double salary, double bonus, int workDays, int year);

    double calculateQuarterlyBonus(Positions positions, double salary, double bonus, int workDays);

}
