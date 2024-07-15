package com.example.api.tests;

import com.example.api.utils.ApiUtils;
import com.example.api.utils.ResponseValidator;
import io.restassured.response.Response;
import org.testng.annotations.Test;
import static org.testng.Assert.assertNotNull;

public class RandomCatFactsTest {

    @Test
    public void testRandomCatFacts() {
        Response response = ApiUtils.sendRequest("GET", "https://catfact.ninja/fact", null);
        ResponseValidator.validateStatusCode(response, 200);
        ResponseValidator.validateJsonField(response, "fact");
    }
}
