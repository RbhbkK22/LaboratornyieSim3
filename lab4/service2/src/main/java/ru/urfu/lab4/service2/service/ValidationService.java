package ru.urfu.lab4.service2.service;

import org.springframework.stereotype.Service;
import org.springframework.validation.BindingResult;
import ru.urfu.lab4.service2.exception.UnsupportedCodeException;
import ru.urfu.lab4.service2.exception.ValidationFailedException;
import ru.urfu.lab4.service2.model.Request;

@Service
public interface ValidationService {

    void isValid(BindingResult bindingResult) throws ValidationFailedException;

    void checkUid(Request request) throws UnsupportedCodeException;
}
