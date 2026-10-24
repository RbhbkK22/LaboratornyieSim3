package ru.urfu.lab4.service1.service;

import org.springframework.stereotype.Service;
import ru.urfu.lab4.service1.model.Response;

@Service
public interface ModifyResponseService {

    Response modify(Response response);

}
