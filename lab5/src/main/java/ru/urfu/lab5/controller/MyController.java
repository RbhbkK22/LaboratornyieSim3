package ru.urfu.lab5.controller;

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
import ru.urfu.lab5.exception.UnsupportedCodeException;
import ru.urfu.lab5.exception.ValidationFailedException;
import ru.urfu.lab5.model.Codes;
import ru.urfu.lab5.model.ErrorCodes;
import ru.urfu.lab5.model.ErrorMessages;
import ru.urfu.lab5.model.Request;
import ru.urfu.lab5.model.Response;
import ru.urfu.lab5.service.AnnualBonusService;
import ru.urfu.lab5.service.ModifyRequestService;
import ru.urfu.lab5.service.ModifyResponseService;
import ru.urfu.lab5.service.ValidationService;
import ru.urfu.lab5.util.DateTimeUtil;

import java.util.Date;

@Slf4j
@RestController
public class MyController {

    private final ValidationService validationService;
    private final ModifyResponseService modifyResponseService;
    private final ModifyRequestService modifySourceRequestService;
    private final ModifyRequestService modifySystemNameRequestService;
    private final AnnualBonusService annualBonusService;

    @Autowired
    public MyController(ValidationService validationService,
                        @Qualifier("ModifySystemTimeResponseService") ModifyResponseService modifyResponseService,
                        @Qualifier("ModifySourceRequestService") ModifyRequestService modifySourceRequestService,
                        @Qualifier("ModifySystemNameRequestService") ModifyRequestService modifySystemNameRequestService,
                        AnnualBonusService annualBonusService) {
        this.validationService = validationService;
        this.modifyResponseService = modifyResponseService;
        this.modifySourceRequestService = modifySourceRequestService;
        this.modifySystemNameRequestService = modifySystemNameRequestService;
        this.annualBonusService = annualBonusService;
    }

    @PostMapping(value = "/feedback")
    public ResponseEntity<Response> feedback(@Valid @RequestBody Request request,
                                             BindingResult bindingResult) {

        String receivedTime = DateTimeUtil.getCustomFormat().format(new Date());
        log.info("request: {}", request);

        Response response = createResponse(request);

        try {
            validationService.isValid(bindingResult);
            validationService.checkUid(request);
            calculateBonuses(request, response);
        } catch (ValidationFailedException e) {
            log.error("Ошибка валидации: {}", e.getMessage());
            return failed(response, ErrorCodes.VALIDATION_EXCEPTION, ErrorMessages.VALIDATION, HttpStatus.BAD_REQUEST);
        } catch (UnsupportedCodeException e) {
            log.error("Неподдерживаемый код: {}", e.getMessage());
            return failed(response, ErrorCodes.UNSUPPORTED_EXCEPTION, ErrorMessages.UNSUPPORTED, HttpStatus.BAD_REQUEST);
        } catch (Exception e) {
            log.error("Непредвиденная ошибка: {}", e.getMessage(), e);
            return failed(response, ErrorCodes.UNKNOWN_EXCEPTION, ErrorMessages.UNKNOWN, HttpStatus.INTERNAL_SERVER_ERROR);
        }

        modifyResponseService.modify(response);
        log.info("итоговый response: {}", response);

        request.setSystemTime(receivedTime);
        modifySourceRequestService.modify(request);
        modifySystemNameRequestService.modify(request);

        return new ResponseEntity<>(response, HttpStatus.OK);
    }

    private Response createResponse(Request request) {
        Response response = Response.builder()
                .uid(request.getUid())
                .operationUid(request.getOperationUid())
                .systemTime(DateTimeUtil.getCustomFormat().format(new Date()))
                .code(Codes.SUCCESS)
                .errorCode(ErrorCodes.EMPTY)
                .errorMessage(ErrorMessages.EMPTY)
                .build();
        log.info("response создан: {}", response);
        return response;
    }

    private void calculateBonuses(Request request, Response response) {
        response.setAnnualBonus(annualBonusService.calculate(request.getPosition(),
                request.getSalary(), request.getBonus(), request.getWorkDays()));
        if (request.getPosition().isManager()) {
            response.setQuarterlyBonus(annualBonusService.calculateQuarterlyBonus(request.getPosition(),
                    request.getSalary(), request.getBonus(), request.getWorkDays()));
        }
        log.info("response после расчёта премий: {}", response);
    }

    private ResponseEntity<Response> failed(Response response, ErrorCodes errorCode,
                                            ErrorMessages errorMessage, HttpStatus status) {
        response.setCode(Codes.FAILED);
        response.setErrorCode(errorCode);
        response.setErrorMessage(errorMessage);
        log.info("response после ошибки: {}", response);
        return new ResponseEntity<>(response, status);
    }
}
