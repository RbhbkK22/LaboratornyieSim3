package ru.urfu.parking.service;

import org.springframework.security.access.AccessDeniedException;
import org.springframework.stereotype.Service;
import ru.urfu.parking.entity.Automobile;
import ru.urfu.parking.repository.AutomobileRepository;

import java.util.List;

@Service
public class AutomobileService {

    private final AutomobileRepository automobileRepository;

    public AutomobileService(AutomobileRepository automobileRepository) {
        this.automobileRepository = automobileRepository;
    }

    public List<Automobile> findAllForCurrentUser() {
        if (SecurityUtils.isUser()) {
            return automobileRepository.findByCreatedBy(SecurityUtils.currentUsername());
        }
        return automobileRepository.findAll();
    }

    public Automobile findById(Long id) {
        Automobile auto = automobileRepository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("Автомобиль не найден: " + id));
        if (SecurityUtils.isUser() && !SecurityUtils.currentUsername().equals(auto.getCreatedBy())) {
            throw new AccessDeniedException("Нет доступа к чужой записи");
        }
        return auto;
    }

    public void save(Automobile automobile) {
        if (automobile.getId() == null) {
            automobile.setCreatedBy(SecurityUtils.currentUsername());
        } else {
            Automobile old = findById(automobile.getId());
            automobile.setCreatedBy(old.getCreatedBy());
        }
        // TODO: проверять что место на парковке не занято другим авто
        automobileRepository.save(automobile);
    }

    public void delete(Long id) {
        Automobile auto = findById(id);
        automobileRepository.delete(auto);
    }
}
