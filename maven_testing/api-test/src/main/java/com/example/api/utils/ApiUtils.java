package com.example.api.utils;

import io.restassured.RestAssured;
import io.restassured.response.Response;
import io.restassured.specification.RequestSpecification;

public class ApiUtils {
    public static Response sendRequest(String method, String url, String body) {
        RequestSpecification request = RestAssured.given();

        switch (method.toUpperCase()) {
            case "GET":
                return request.get(url);
            case "POST":
                return request.body(body).post(url);
            case "PUT":
                return request.body(body).put(url);
            case "DELETE":
                return request.delete(url);
            default:
                throw new IllegalArgumentException("Invalid HTTP method: " + method);
        }
    }
}
