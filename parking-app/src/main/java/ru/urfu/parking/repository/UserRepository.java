package ru.urfu.parking.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import ru.urfu.parking.entity.User;

import java.util.Optional;

public interface UserRepository extends JpaRepository<User, Long> {

    Optional<User> findByUsername(String username);

    boolean existsByUsername(String username);
}
