package ru.urfu.parking.controller;

import jakarta.validation.Valid;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;
import ru.urfu.parking.entity.Automobile;
import ru.urfu.parking.repository.CarModelRepository;
import ru.urfu.parking.service.AutomobileService;

import java.time.LocalDate;

@Controller
@RequestMapping("/automobiles")
public class AutomobileController {

    private final AutomobileService automobileService;
    private final CarModelRepository carModelRepository;

    public AutomobileController(AutomobileService automobileService, CarModelRepository carModelRepository) {
        this.automobileService = automobileService;
        this.carModelRepository = carModelRepository;
    }

    @GetMapping
    public String list(Model model) {
        model.addAttribute("automobiles", automobileService.findAllForCurrentUser());
        return "automobiles/list";
    }

    @GetMapping("/new")
    public String newForm(Model model) {
        Automobile automobile = new Automobile();
        automobile.setArrivalDate(LocalDate.now());
        model.addAttribute("automobile", automobile);
        model.addAttribute("models", carModelRepository.findAll());
        return "automobiles/form";
    }

    @GetMapping("/edit/{id}")
    public String editForm(@PathVariable Long id, Model model) {
        model.addAttribute("automobile", automobileService.findById(id));
        model.addAttribute("models", carModelRepository.findAll());
        return "automobiles/form";
    }

    @PostMapping("/save")
    public String save(@Valid @ModelAttribute("automobile") Automobile automobile,
                       BindingResult bindingResult,
                       @RequestParam(required = false) Long modelId,
                       Model model,
                       RedirectAttributes redirectAttributes) {
        if (modelId == null) {
            bindingResult.rejectValue("model", "model.empty", "Выберите модель");
        }
        if (bindingResult.hasErrors()) {
            model.addAttribute("models", carModelRepository.findAll());
            return "automobiles/form";
        }

        automobile.setModel(carModelRepository.findById(modelId).orElse(null));
        automobileService.save(automobile);
        redirectAttributes.addFlashAttribute("message", "Автомобиль сохранен");
        return "redirect:/automobiles";
    }

    @PostMapping("/delete/{id}")
    public String delete(@PathVariable Long id, RedirectAttributes redirectAttributes) {
        automobileService.delete(id);
        redirectAttributes.addFlashAttribute("message", "Автомобиль удален");
        return "redirect:/automobiles";
    }
}
