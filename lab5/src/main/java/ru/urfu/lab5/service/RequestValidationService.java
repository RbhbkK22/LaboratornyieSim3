package ru.urfu.lab5.service;

import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.validation.BindingResult;
import ru.urfu.lab5.exception.UnsupportedCodeException;
import ru.urfu.lab5.exception.ValidationFailedException;
import ru.urfu.lab5.model.Request;

@Slf4j
@Service
public class RequestValidationService implements ValidationService {

    @Override
    public void isValid(BindingResult bindingResult) throws ValidationFailedException {
        if (bindingResult.hasErrors()) {
            bindingResult.getFieldErrors().forEach(error ->
                    log.error("Ошибка в bindingResult: поле '{}' - {}",
                            error.getField(), error.getDefaultMessage()));
            throw new
                    ValidationFailedException(bindingResult.getFieldError().toString());
        }
    }

    @Override
    public void checkUid(Request request) throws UnsupportedCodeException {
        if ("123".equals(request.getUid())) {
            log.error("Получен неподдерживаемый uid: {}", request.getUid());
            throw new UnsupportedCodeException("uid 123 не поддерживается");
        }
    }
}
