package ru.urfu.parking.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import ru.urfu.parking.entity.CarModel;

import java.util.List;

public interface CarModelRepository extends JpaRepository<CarModel, Long> {

    List<CarModel> findByCreatedBy(String createdBy);
}
