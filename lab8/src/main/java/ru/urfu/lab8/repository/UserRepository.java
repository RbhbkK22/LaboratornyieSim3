package ru.urfu.lab8.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import ru.urfu.lab8.entity.User;

public interface UserRepository extends JpaRepository<User, Long> {
    User findByEmail(String email);
}
