package ru.urfu.lab8.service;

import ru.urfu.lab8.dto.UserDto;
import ru.urfu.lab8.entity.User;

import java.util.List;

public interface UserService {
    void saveUser(UserDto userDto);

    User findUserByEmail(String email);

    List<UserDto> findAllUsers();
}
