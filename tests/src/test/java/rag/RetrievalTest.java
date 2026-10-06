package rag;

import io.restassured.RestAssured;
import io.restassured.http.ContentType;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

import java.util.List;

import static io.restassured.RestAssured.given;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class RetrievalTest {

    @BeforeAll
    static void setup() {
        RestAssured.baseURI = "http://127.0.0.1:8000";
    }

    @Test
    void gd02_currentLeavePolicyIsRetrievedAndArchivedIsNot() {
        List<String> sources =
                given()
                        .contentType(ContentType.JSON)
                        .body("{\"question\": \"How many annual leave days do employees get?\", \"k\": 3}")
                        .when()
                        .post("/retrieve")
                        .then()
                        .statusCode(200)
                        .extract().jsonPath().getList("hits.source", String.class);

        assertTrue(sources.contains("handbook/leave-policy.md"),
                "Expected current leave policy in top 3, got: " + sources);
        assertFalse(sources.contains("handbook/leave-policy-2023-archived.md"),
                "Archived policy must never be retrieved, got: " + sources);
    }
}