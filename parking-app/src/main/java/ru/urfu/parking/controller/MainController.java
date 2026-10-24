package ru.urfu.parking.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import ru.urfu.parking.service.AutomobileService;
import ru.urfu.parking.service.CarModelService;

@Controller
public class MainController {

    private final AutomobileService automobileService;
    private final CarModelService carModelService;

    public MainController(AutomobileService automobileService, CarModelService carModelService) {
        this.automobileService = automobileService;
        this.carModelService = carModelService;
    }

    @GetMapping("/")
    public String index(Model model) {
        // немного статистики на главную
        model.addAttribute("autoCount", automobileService.findAllForCurrentUser().size());
        model.addAttribute("modelCount", carModelService.findAllForCurrentUser().size());
        return "index";
    }

    @GetMapping("/about")
    public String about() {
        return "about";
    }

    // RequestMapping, а не GetMapping - сюда может прийти и POST (например удаление без прав)
    @RequestMapping("/access-denied")
    public String accessDenied() {
        return "access-denied";
    }
}
