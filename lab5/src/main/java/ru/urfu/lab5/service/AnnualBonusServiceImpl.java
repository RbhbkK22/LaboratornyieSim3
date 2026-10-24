package ru.urfu.lab5.service;

import org.springframework.stereotype.Service;
import ru.urfu.lab5.model.Positions;

import java.time.Year;

@Service
public class AnnualBonusServiceImpl implements AnnualBonusService {

    @Override
    public double calculate(Positions positions, double salary, double bonus, int workDays) {
        return calculate(positions, salary, bonus, workDays, Year.now().getValue());
    }

    // количество дней в году зависит от того, високосный год или нет
    @Override
    public double calculate(Positions positions, double salary, double bonus, int workDays, int year) {
        int daysInYear = Year.isLeap(year) ? 366 : 365;
        return salary * bonus * daysInYear * positions.getPositionCoefficient() / workDays;
    }

    // квартальная премия рассчитывается только для управленцев (isManager == true)
    @Override
    public double calculateQuarterlyBonus(Positions positions, double salary, double bonus, int workDays) {
        if (!positions.isManager()) {
            throw new IllegalArgumentException("Квартальная премия рассчитывается только для управленцев");
        }
        return salary * bonus * positions.getPositionCoefficient() * 3 / 4;
    }
}
