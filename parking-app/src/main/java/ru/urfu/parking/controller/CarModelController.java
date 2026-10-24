package ru.urfu.parking.controller;

import jakarta.validation.Valid;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;
import ru.urfu.parking.entity.CarModel;
import ru.urfu.parking.service.CarModelService;

@Controller
@RequestMapping("/models")
public class CarModelController {

    private final CarModelService carModelService;

    public CarModelController(CarModelService carModelService) {
        this.carModelService = carModelService;
    }

    @GetMapping
    public String list(Model model) {
        model.addAttribute("models", carModelService.findAllForCurrentUser());
        return "models/list";
    }

    @GetMapping("/new")
    public String newForm(Model model) {
        model.addAttribute("carModel", new CarModel());
        return "models/form";
    }

    @GetMapping("/edit/{id}")
    public String editForm(@PathVariable Long id, Model model) {
        model.addAttribute("carModel", carModelService.findById(id));
        return "models/form";
    }

    @PostMapping("/save")
    public String save(@Valid @ModelAttribute("carModel") CarModel carModel,
                       BindingResult bindingResult,
                       RedirectAttributes redirectAttributes) {
        if (bindingResult.hasErrors()) {
            return "models/form";
        }
        carModelService.save(carModel);
        redirectAttributes.addFlashAttribute("message", "Модель сохранена");
        return "redirect:/models";
    }

    @PostMapping("/delete/{id}")
    public String delete(@PathVariable Long id, RedirectAttributes redirectAttributes) {
        try {
            carModelService.delete(id);
            redirectAttributes.addFlashAttribute("message", "Модель удалена");
        } catch (IllegalStateException e) {
            redirectAttributes.addFlashAttribute("error", e.getMessage());
        }
        return "redirect:/models";
    }
}
