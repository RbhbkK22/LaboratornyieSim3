package ru.urfu.lab4.service2.controller;

import jakarta.validation.Valid;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import ru.urfu.lab4.service2.exception.UnsupportedCodeException;
import ru.urfu.lab4.service2.exception.ValidationFailedException;
import ru.urfu.lab4.service2.model.Codes;
import ru.urfu.lab4.service2.model.ErrorCodes;
import ru.urfu.lab4.service2.model.ErrorMessages;
import ru.urfu.lab4.service2.model.Request;
import ru.urfu.lab4.service2.model.Response;
import ru.urfu.lab4.service2.service.ModifyResponseService;
import ru.urfu.lab4.service2.service.ValidationService;
import ru.urfu.lab4.service2.util.DateTimeUtil;

import java.text.ParseException;
import java.util.Date;

@Slf4j
@RestController
public class MyController {

    private final ValidationService validationService;
    private final ModifyResponseService modifyResponseService;

    @Autowired
    public MyController(ValidationService validationService,
                        @Qualifier("ModifySystemTimeResponseService") ModifyResponseService modifyResponseService) {
        this.validationService = validationService;
        this.modifyResponseService = modifyResponseService;
    }

    @PostMapping(value = "/feedback")
    public ResponseEntity<Response> feedback(@Valid @RequestBody Request request,
                                             BindingResult bindingResult) {

        Date receivedDate = new Date();
        log.info("request: {}", request);
        logTimeDifference(request, receivedDate);

        Response response = Response.builder()
                .uid(request.getUid())
                .operationUid(request.getOperationUid())
                .systemTime(DateTimeUtil.getCustomFormat().format(new Date()))
                .code(Codes.SUCCESS)
                .errorCode(ErrorCodes.EMPTY)
                .errorMessage(ErrorMessages.EMPTY)
                .build();
        log.info("response создан: {}", response);

        try {
            validationService.isValid(bindingResult);
            validationService.checkUid(request);
        } catch (ValidationFailedException e) {
            log.error("Ошибка валидации: {}", e.getMessage());
            response.setCode(Codes.FAILED);
            response.setErrorCode(ErrorCodes.VALIDATION_EXCEPTION);
            response.setErrorMessage(ErrorMessages.VALIDATION);
            log.info("response после ошибки валидации: {}", response);
            return new ResponseEntity<>(response, HttpStatus.BAD_REQUEST);
        } catch (UnsupportedCodeException e) {
            log.error("Неподдерживаемый код: {}", e.getMessage());
            response.setCode(Codes.FAILED);
            response.setErrorCode(ErrorCodes.UNSUPPORTED_EXCEPTION);
            response.setErrorMessage(ErrorMessages.UNSUPPORTED);
            log.info("response после ошибки UnsupportedCodeException: {}", response);
            return new ResponseEntity<>(response, HttpStatus.BAD_REQUEST);
        } catch (Exception e) {
            log.error("Непредвиденная ошибка: {}", e.getMessage(), e);
            response.setCode(Codes.FAILED);
            response.setErrorCode(ErrorCodes.UNKNOWN_EXCEPTION);
            response.setErrorMessage(ErrorMessages.UNKNOWN);
            log.info("response после непредвиденной ошибки: {}", response);
            return new ResponseEntity<>(response, HttpStatus.INTERNAL_SERVER_ERROR);
        }

        modifyResponseService.modify(response);
        log.info("итоговый response: {}", response);

        return new ResponseEntity<>(response, HttpStatus.OK);
    }

    // systemTime содержит время получения request Сервисом 1
    private void logTimeDifference(Request request, Date receivedDate) {
        try {
            Date service1Date = DateTimeUtil.getCustomFormat().parse(request.getSystemTime());
            long difference = receivedDate.getTime() - service1Date.getTime();
            log.info("Время от получения request Сервисом 1 до получения Сервисом 2: {} мс", difference);
        } catch (ParseException | NullPointerException e) {
            log.error("Не удалось вычислить разницу времени, systemTime: {}", request.getSystemTime());
        }
    }
}
