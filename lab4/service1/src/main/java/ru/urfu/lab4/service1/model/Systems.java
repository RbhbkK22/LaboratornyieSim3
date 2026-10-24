package ru.urfu.lab4.service1.model;

import lombok.Getter;

@Getter
public enum Systems {

    ERP("Enterprise Resource Planning"),
    CRM("Customer Relationship Management"),
    WMS("Warehouse Management System"),
    SERVICE_1("Service 1");

    private final String description;

    Systems(String description) {
        this.description = description;
    }

}
