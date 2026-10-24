package ru.urfu.lab5.service;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpMethod;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;
import ru.urfu.lab5.model.Request;
import ru.urfu.lab5.model.Systems;

@Slf4j
@Service
@Qualifier("ModifySystemNameRequestService")
public class ModifySystemNameRequestService implements ModifyRequestService {

    @Override
    public void modify(Request request) {
        request.setSystemName(Systems.SERVICE_1);
        log.info("request после изменения systemName: {}", request);

        HttpEntity<Request> httpEntity = new HttpEntity<>(request);

        log.info("Отправка request в Сервис 2: {}", request);
        try {
            new RestTemplate().exchange("http://localhost:8084/feedback",
                    HttpMethod.POST,
                    httpEntity,
                    new ParameterizedTypeReference<>() {
                    });
        } catch (RestClientException e) {
            log.error("Не удалось отправить request в Сервис 2: {}", e.getMessage());
        }
    }
}
