package ru.urfu.parking.entity;

import jakarta.persistence.*;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

/**
 * Модель автомобиля и её стоимость
 */
@Entity
@Table(name = "car_models")
@Getter
@Setter
@NoArgsConstructor
public class CarModel {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @NotBlank(message = "Укажите марку")
    private String brand;

    @NotBlank(message = "Укажите модель")
    @Column(name = "model_name")
    private String modelName;

    @NotNull(message = "Укажите год")
    @Min(value = 1950, message = "Год не может быть меньше 1950")
    @Max(value = 2030, message = "Слишком большой год")
    @Column(name = "release_year")
    private Integer releaseYear;

    @NotNull(message = "Укажите стоимость")
    @Min(value = 0, message = "Стоимость не может быть отрицательной")
    private Double price;

    // кто создал запись (нужно для роли USER)
    @Column(name = "created_by")
    private String createdBy;

    public String getFullName() {
        return brand + " " + modelName + " (" + releaseYear + ")";
    }
}
