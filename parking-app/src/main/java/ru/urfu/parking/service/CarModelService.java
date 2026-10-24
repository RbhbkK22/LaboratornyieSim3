package ru.urfu.parking.service;

import org.springframework.security.access.AccessDeniedException;
import org.springframework.stereotype.Service;
import ru.urfu.parking.entity.CarModel;
import ru.urfu.parking.repository.AutomobileRepository;
import ru.urfu.parking.repository.CarModelRepository;

import java.util.List;

@Service
public class CarModelService {

    private final CarModelRepository carModelRepository;
    private final AutomobileRepository automobileRepository;

    public CarModelService(CarModelRepository carModelRepository, AutomobileRepository automobileRepository) {
        this.carModelRepository = carModelRepository;
        this.automobileRepository = automobileRepository;
    }

    /**
     * Список моделей с учетом роли:
     * USER видит только свои, ADMIN и READ_ONLY - все
     */
    public List<CarModel> findAllForCurrentUser() {
        if (SecurityUtils.isUser()) {
            return carModelRepository.findByCreatedBy(SecurityUtils.currentUsername());
        }
        return carModelRepository.findAll();
    }

    // для выпадающего списка в форме автомобиля - отдаем все модели (это справочник)
    public List<CarModel> findAll() {
        return carModelRepository.findAll();
    }

    public CarModel findById(Long id) {
        CarModel model = carModelRepository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("Модель не найдена: " + id));
        checkAccess(model);
        return model;
    }

    public void save(CarModel model) {
        if (model.getId() == null) {
            model.setCreatedBy(SecurityUtils.currentUsername());
        } else {
            CarModel old = findById(model.getId());
            model.setCreatedBy(old.getCreatedBy());
        }
        carModelRepository.save(model);
    }

    public void delete(Long id) {
        CarModel model = findById(id);
        if (!automobileRepository.findByModelId(id).isEmpty()) {
            throw new IllegalStateException("Нельзя удалить модель, к ней привязаны автомобили");
        }
        carModelRepository.delete(model);
    }

    private void checkAccess(CarModel model) {
        if (SecurityUtils.isUser() && !SecurityUtils.currentUsername().equals(model.getCreatedBy())) {
            throw new AccessDeniedException("Нет доступа к чужой записи");
        }
    }
}
