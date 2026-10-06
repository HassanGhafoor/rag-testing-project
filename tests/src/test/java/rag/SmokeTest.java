package rag;

import io.restassured.RestAssured;
import io.restassured.http.ContentType;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.emptyOrNullString;
import static org.hamcrest.Matchers.hasSize;
import static org.hamcrest.Matchers.not;

class SmokeTest {

    @BeforeAll
    static void setup() {
        RestAssured.baseURI = "http://127.0.0.1:8000";
    }

    @Test
    void askEndpointReturnsAnAnswerWithThreeSources() {
        given()
                .contentType(ContentType.JSON)
                .body("{\"question\": \"How many annual leave days do employees get?\"}")
                .when()
                .post("/ask")
                .then()
                .statusCode(200)
                .body("answer", not(emptyOrNullString()))
                .body("hits", hasSize(3));
    }
}