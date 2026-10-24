package ru.urfu.lab4.service1.service;

import org.springframework.stereotype.Service;
import ru.urfu.lab4.service1.model.Request;

@Service
public interface ModifyRequestService {

    void modify(Request request);

}
