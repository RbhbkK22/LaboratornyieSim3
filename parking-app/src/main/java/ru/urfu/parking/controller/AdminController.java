package ru.urfu.parking.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;
import ru.urfu.parking.entity.Role;
import ru.urfu.parking.service.UserService;

/**
 * Форма назначения ролей. Доступна только ADMIN (см. SecurityConfig)
 */
@Controller
@RequestMapping("/admin")
public class AdminController {

    private final UserService userService;

    public AdminController(UserService userService) {
        this.userService = userService;
    }

    @GetMapping("/users")
    public String users(Model model) {
        model.addAttribute("users", userService.findAll());
        model.addAttribute("roles", Role.values());
        return "admin/users";
    }

    @PostMapping("/users/{id}/role")
    public String changeRole(@PathVariable Long id, @RequestParam Role role,
                             RedirectAttributes redirectAttributes) {
        userService.changeRole(id, role);
        // новая роль применится после повторного входа пользователя
        redirectAttributes.addFlashAttribute("message", "Роль изменена на " + role);
        return "redirect:/admin/users";
    }
}
