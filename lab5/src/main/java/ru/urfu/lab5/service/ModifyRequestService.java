package ru.urfu.lab5.service;

import org.springframework.stereotype.Service;
import ru.urfu.lab5.model.Request;

@Service
public interface ModifyRequestService {

    void modify(Request request);

}
