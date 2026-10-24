package ru.urfu.lab5.service;

import org.junit.jupiter.api.Test;
import ru.urfu.lab5.model.Positions;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

class AnnualBonusServiceImplTest {

    @Test
    void calculate() {

        // given
        Positions position = Positions.HR;
        double bonus = 2.0;
        int workDays = 243;
        double salary = 100000.00;

        // when
        double result = new AnnualBonusServiceImpl().calculate(position, salary, bonus, workDays, 2023);

        // then
        double expected = 360493.8271604938;
        assertThat(result).isEqualTo(expected);
    }

    @Test
    void calculateInLeapYear() {

        // given
        Positions position = Positions.HR;
        double bonus = 2.0;
        int workDays = 243;
        double salary = 100000.00;

        // when
        double result = new AnnualBonusServiceImpl().calculate(position, salary, bonus, workDays, 2024);

        // then
        double expected = 100000.00 * 2.0 * 366 * 1.2 / 243;
        assertThat(result).isEqualTo(expected);
    }

    @Test
    void calculateQuarterlyBonus() {

        // given
        Positions position = Positions.TL;
        double bonus = 2.0;
        int workDays = 243;
        double salary = 100000.00;

        // when
        double result = new AnnualBonusServiceImpl().calculateQuarterlyBonus(position, salary, bonus, workDays);

        // then
        double expected = 390000.0;
        assertThat(result).isEqualTo(expected);
    }

    @Test
    void calculateQuarterlyBonusForNotManager() {

        // given
        Positions position = Positions.DEV;

        // when / then
        assertThatThrownBy(() -> new AnnualBonusServiceImpl()
                .calculateQuarterlyBonus(position, 100000.00, 2.0, 243))
                .isInstanceOf(IllegalArgumentException.class);
    }
}
