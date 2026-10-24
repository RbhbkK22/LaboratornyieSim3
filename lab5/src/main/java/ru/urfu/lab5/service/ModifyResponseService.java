package ru.urfu.lab5.service;

import org.springframework.stereotype.Service;
import ru.urfu.lab5.model.Response;

@Service
public interface ModifyResponseService {

    Response modify(Response response);

}
