package ru.urfu.parking.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import ru.urfu.parking.entity.Automobile;

import java.util.List;

public interface AutomobileRepository extends JpaRepository<Automobile, Long> {

    List<Automobile> findByCreatedBy(String createdBy);

    List<Automobile> findByModelId(Long modelId);
}
