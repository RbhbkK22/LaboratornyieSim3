package ru.urfu.lab4.service2.service;

import org.springframework.stereotype.Service;
import ru.urfu.lab4.service2.model.Response;

@Service
public interface ModifyResponseService {

    Response modify(Response response);

}
