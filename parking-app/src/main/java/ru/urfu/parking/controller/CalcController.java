package ru.urfu.parking.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import ru.urfu.parking.entity.Automobile;
import ru.urfu.parking.service.AutomobileService;
import ru.urfu.parking.service.CalcService;

/**
 * Форма расчета: сколько стоит стоянка и сколько сейчас стоит машина
 */
@Controller
@RequestMapping("/calc")
public class CalcController {

    private final AutomobileService automobileService;
    private final CalcService calcService;

    public CalcController(AutomobileService automobileService, CalcService calcService) {
        this.automobileService = automobileService;
        this.calcService = calcService;
    }

    @GetMapping
    public String form(Model model) {
        model.addAttribute("automobiles", automobileService.findAllForCurrentUser());
        model.addAttribute("tariff", 300.0);
        return "calc";
    }

    @PostMapping
    public String calculate(@RequestParam Long autoId,
                            @RequestParam(defaultValue = "300") Double tariff,
                            Model model) {
        model.addAttribute("automobiles", automobileService.findAllForCurrentUser());
        model.addAttribute("tariff", tariff);
        model.addAttribute("autoId", autoId);

        if (tariff < 0) {
            model.addAttribute("error", "Тариф не может быть отрицательным");
            return "calc";
        }

        Automobile auto = automobileService.findById(autoId);
        long days = calcService.countDays(auto);

        model.addAttribute("auto", auto);
        model.addAttribute("days", days);
        model.addAttribute("discount", calcService.hasDiscount(days));
        model.addAttribute("parkingCost", calcService.parkingCost(days, tariff));
        model.addAttribute("carValue", calcService.carValue(auto));
        return "calc";
    }
}
