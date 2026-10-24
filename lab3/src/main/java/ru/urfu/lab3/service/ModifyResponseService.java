package ru.urfu.lab3.service;

import org.springframework.stereotype.Service;
import ru.urfu.lab3.model.Response;

@Service
public interface ModifyResponseService {

    Response modify(Response response);

}
