# Парковка (курсовой проект, вариант 7)

Веб-приложение для учета автомобилей на парковке и справочника моделей автомобилей со стоимостью.

## Технологии
- Java 17, Spring Boot 3.5
- Spring MVC + Thymeleaf, Bootstrap 5
- Spring Security
- Spring Data JPA, H2 (файл `./data/parking`)
- Lombok
- Spring Boot Actuator

## Запуск

```
mvnw.cmd spring-boot:run
```

Приложение откроется на http://localhost:8080

## Тестовые пользователи

| логин | пароль | роль      |
|-------|--------|-----------|
| admin | admin  | ADMIN     |
| user  | user   | USER      |
| guest | guest  | READ_ONLY |

Новые пользователи после регистрации получают роль READ_ONLY.

## Полезные адреса
- http://localhost:8080/h2-console - консоль БД (только ADMIN), JDBC URL: `jdbc:h2:file:./data/parking;AUTO_SERVER=TRUE`, user `sa`
- http://localhost:8080/actuator/health - состояние приложения
- http://localhost:8080/actuator - остальные эндпоинты (только ADMIN)
