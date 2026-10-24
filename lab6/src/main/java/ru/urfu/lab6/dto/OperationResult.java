package ru.urfu.lab6.dto;

import lombok.AllArgsConstructor;
import lombok.Data;

// Ответ об успехе или неуспехе завершения операции
@Data
@AllArgsConstructor
public class OperationResult<T> {

    private boolean success;
    private String message;
    private T data;

    public static <T> OperationResult<T> success(String message, T data) {
        return new OperationResult<>(true, message, data);
    }

    public static <T> OperationResult<T> failed(String message) {
        return new OperationResult<>(false, message, null);
    }
}
