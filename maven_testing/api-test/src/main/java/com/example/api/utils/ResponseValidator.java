package com.example.api.utils;

import io.restassured.response.Response;
import org.json.JSONObject;

import static org.testng.Assert.assertEquals;
import static org.testng.Assert.assertNotNull;
import static org.testng.Assert.assertTrue;

public class ResponseValidator {
    public static void validateStatusCode(Response response, int expectedStatusCode) {
        assertEquals(response.getStatusCode(), expectedStatusCode, "Status code mismatch!");
    }

    public static void validateJsonField(Response response, String fieldName) {
        JSONObject jsonResponse = new JSONObject(response.asString());
        assertTrue(jsonResponse.has(fieldName), "Field " + fieldName + " is not present in response!");
        assertNotNull(jsonResponse.get(fieldName), "Field " + fieldName + " is null in response!");
    }

    public static void validateJsonFieldWithValue(Response response, String fieldName, Object expectedValue) {
        JSONObject jsonResponse = new JSONObject(response.asString());
        assertTrue(jsonResponse.has(fieldName), "Field " + fieldName + " is not present in response!");
        assertEquals(jsonResponse.get(fieldName), expectedValue, "Field " + fieldName + " value mismatch!");
    }
}