package ru.urfu.parking.service;

import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;

// вспомогательные методы чтобы достать текущего пользователя
public class SecurityUtils {

    public static String currentUsername() {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        return auth.getName();
    }

    public static boolean hasRole(String role) {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        return auth.getAuthorities().stream()
                .anyMatch(a -> a.getAuthority().equals("ROLE_" + role));
    }

    public static boolean isAdmin() {
        return hasRole("ADMIN");
    }

    public static boolean isUser() {
        return hasRole("USER");
    }
}
