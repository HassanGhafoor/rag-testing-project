package rag;

import io.restassured.RestAssured;
import io.restassured.http.ContentType;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;

import java.util.List;
import java.util.Map;

import static io.restassured.RestAssured.given;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class RetrievalTest {

    private static final int K = 3;
    private static int found = 0;
    private static int total = 0;

    @BeforeAll
    static void setup() {
        RestAssured.baseURI = "http://127.0.0.1:8000";
    }

    private static List<String> retrieveSources(String question) {
        return given()
                .contentType(ContentType.JSON)
                .body(Map.of("question", question, "k", K))
                .when()
                .post("/retrieve")
                .then()
                .statusCode(200)
                .extract().jsonPath().getList("hits.source", String.class);
    }

    @ParameterizedTest(name = "{0}")
    @MethodSource("rag.GoldenDataset#answerable")
    void expectedSourceIsInTopK(GoldenCase goldenCase) {
        List<String> sources = retrieveSources(goldenCase.question());
        boolean hit = sources.stream().anyMatch(goldenCase.expectedSources()::contains);

        total++;
        if (hit) {
            found++;
        }

        assertTrue(hit, goldenCase.id() + ": expected one of " + goldenCase.expectedSources()
                + " in top " + K + ", got " + sources);
    }

    @Test
    void archivedLeavePolicyIsNeverRetrieved() {
        List<String> sources = retrieveSources("How many annual leave days do employees get?");
        assertFalse(sources.contains("handbook/leave-policy-2023-archived.md"),
                "Archived policy must never be retrieved, got: " + sources);
    }

    @AfterAll
    static void reportRecall() {
        if (total > 0) {
            System.out.printf("Recall@%d: %d/%d = %.0f%%%n", K, found, total, 100.0 * found / total);
        }
    }
}