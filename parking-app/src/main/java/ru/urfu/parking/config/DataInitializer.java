package ru.urfu.parking.config;

import org.springframework.boot.CommandLineRunner;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;
import ru.urfu.parking.entity.Automobile;
import ru.urfu.parking.entity.CarModel;
import ru.urfu.parking.entity.Role;
import ru.urfu.parking.entity.User;
import ru.urfu.parking.repository.AutomobileRepository;
import ru.urfu.parking.repository.CarModelRepository;
import ru.urfu.parking.repository.UserRepository;

import java.time.LocalDate;

/**
 * Заполняет базу тестовыми данными при первом запуске
 */
@Component
public class DataInitializer implements CommandLineRunner {

    private final UserRepository userRepository;
    private final CarModelRepository carModelRepository;
    private final AutomobileRepository automobileRepository;
    private final PasswordEncoder passwordEncoder;

    public DataInitializer(UserRepository userRepository, CarModelRepository carModelRepository,
                           AutomobileRepository automobileRepository, PasswordEncoder passwordEncoder) {
        this.userRepository = userRepository;
        this.carModelRepository = carModelRepository;
        this.automobileRepository = automobileRepository;
        this.passwordEncoder = passwordEncoder;
    }

    @Override
    public void run(String... args) {
        if (userRepository.count() > 0) {
            return; // уже заполнено
        }

        userRepository.save(new User("admin", passwordEncoder.encode("admin"), Role.ADMIN));
        userRepository.save(new User("user", passwordEncoder.encode("user"), Role.USER));
        userRepository.save(new User("guest", passwordEncoder.encode("guest"), Role.READ_ONLY));

        CarModel camry = createModel("Toyota", "Camry", 2020, 2_900_000.0, "admin");
        CarModel solaris = createModel("Hyundai", "Solaris", 2018, 1_200_000.0, "admin");
        CarModel vesta = createModel("Lada", "Vesta", 2022, 1_350_000.0, "user");

        createAuto("А123ВС66", "Иванов И.И.", "белый", 1, LocalDate.now().minusDays(3), camry, "admin");
        createAuto("К777ОР96", "Петров П.П.", "черный", 2, LocalDate.now().minusDays(40), solaris, "admin");
        createAuto("М555ТТ66", "Сидорова А.А.", "серый", 5, LocalDate.now().minusDays(1), vesta, "user");
    }

    private CarModel createModel(String brand, String name, int year, double price, String createdBy) {
        CarModel m = new CarModel();
        m.setBrand(brand);
        m.setModelName(name);
        m.setReleaseYear(year);
        m.setPrice(price);
        m.setCreatedBy(createdBy);
        return carModelRepository.save(m);
    }

    private void createAuto(String plate, String owner, String color, int place, LocalDate date,
                            CarModel model, String createdBy) {
        Automobile a = new Automobile();
        a.setPlateNumber(plate);
        a.setOwnerName(owner);
        a.setColor(color);
        a.setParkingPlace(place);
        a.setArrivalDate(date);
        a.setModel(model);
        a.setCreatedBy(createdBy);
        automobileRepository.save(a);
    }
}
