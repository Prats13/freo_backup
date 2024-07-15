package com.example.api.tests;

import com.example.api.utils.ApiUtils;
import com.example.api.utils.ResponseValidator;
import io.restassured.response.Response;
import org.testng.annotations.Test;

public class GetCurrentIPTest {

    @Test
    public void testGetCurrentIP() {
        Response response = ApiUtils.sendRequest("GET", "https://api.ipify.org/?format=json", null);
        ResponseValidator.validateStatusCode(response, 200);
        ResponseValidator.validateJsonField(response, "ip");
    }
}