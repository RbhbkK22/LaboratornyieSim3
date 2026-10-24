package ru.urfu.parking.entity;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.springframework.format.annotation.DateTimeFormat;

import java.time.LocalDate;

/**
 * Автомобиль на парковке
 */
@Entity
@Table(name = "automobiles")
@Getter
@Setter
@NoArgsConstructor
public class Automobile {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @NotBlank(message = "Укажите госномер")
    @Column(name = "plate_number")
    private String plateNumber;

    @NotBlank(message = "Укажите владельца")
    @Column(name = "owner_name")
    private String ownerName;

    private String color;

    @NotNull(message = "Укажите место")
    @Column(name = "parking_place")
    private Integer parkingPlace;

    @NotNull(message = "Укажите дату заезда")
    @DateTimeFormat(pattern = "yyyy-MM-dd")
    @Column(name = "arrival_date")
    private LocalDate arrivalDate;

    @ManyToOne
    @JoinColumn(name = "model_id")
    private CarModel model;

    @Column(name = "created_by")
    private String createdBy;
}
