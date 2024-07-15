package com.example.api.base;

import io.restassured.RestAssured;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.testng.annotations.BeforeClass;

import com.example.api.utils.ConfigManager;

public class BaseTest {
    protected static final Logger logger = LoggerFactory.getLogger(BaseTest.class);

    @BeforeClass
    public void setup() {
        RestAssured.baseURI = ConfigManager.getProperty("baseURI");
        logger.info("Base URI set to: {}", RestAssured.baseURI);
    }
}
