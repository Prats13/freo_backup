package com.example.api.tests;

import com.example.api.utils.ApiUtils;
import com.example.api.utils.ResponseValidator;
import io.restassured.response.Response;
import org.testng.annotations.Test;

public class CurrentBTCPriceTest {

    @Test
    public void testCurrentBTCPrice() {
        Response response = ApiUtils.sendRequest("GET", "https://api.coindesk.com/v1/bpi/currentprice.json", null);
        ResponseValidator.validateStatusCode(response, 200);
        ResponseValidator.validateJsonField(response, "bpi");
        ResponseValidator.validateJsonField(response, "time");
        ResponseValidator.validateJsonField(response, "disclaimer");
    }
}
