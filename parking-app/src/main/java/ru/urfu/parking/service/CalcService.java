package ru.urfu.parking.service;

import org.springframework.stereotype.Service;
import ru.urfu.parking.entity.Automobile;

import java.time.LocalDate;
import java.time.temporal.ChronoUnit;

/**
 * Расчет стоимости стоянки и остаточной стоимости автомобиля
 */
@Service
public class CalcService {

    // скидка за долгую стоянку
    private static final int DISCOUNT_DAYS = 30;
    private static final double DISCOUNT_PERCENT = 15;

    // автомобиль дешевеет примерно на 10% в год, но не меньше 20% от цены
    private static final double DEPRECIATION_PER_YEAR = 0.10;
    private static final double MIN_VALUE_PERCENT = 0.20;

    public long countDays(Automobile auto) {
        // день заезда тоже считается
        return ChronoUnit.DAYS.between(auto.getArrivalDate(), LocalDate.now()) + 1;
    }

    public double parkingCost(long days, double tariff) {
        double cost = days * tariff;
        if (days >= DISCOUNT_DAYS) {
            cost = cost - cost * DISCOUNT_PERCENT / 100;
        }
        return Math.round(cost * 100) / 100.0;
    }

    public double carValue(Automobile auto) {
        if (auto.getModel() == null) {
            return 0;
        }
        int age = LocalDate.now().getYear() - auto.getModel().getReleaseYear();
        if (age < 0) {
            age = 0;
        }
        double value = auto.getModel().getPrice() * Math.pow(1 - DEPRECIATION_PER_YEAR, age);
        double min = auto.getModel().getPrice() * MIN_VALUE_PERCENT;
        if (value < min) {
            value = min;
        }
        return Math.round(value);
    }

    public boolean hasDiscount(long days) {
        return days >= DISCOUNT_DAYS;
    }
}
