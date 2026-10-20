package rag;

import io.restassured.RestAssured;
import io.restassured.http.ContentType;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;

import java.util.Map;
import java.util.regex.Pattern;

import static io.restassured.RestAssured.given;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assertions.assertFalse;

class GenerationTest {

    private static final Map<String, String> KNOWN_FAILURES = Map.of();

    @BeforeAll
    static void setup() {
        RestAssured.baseURI = "http://127.0.0.1:8000";
    }

    private static String ask(String question) {
        return given()
                .contentType(ContentType.JSON)
                .body(Map.of("question", question))
                .when()
                .post("/ask")
                .then()
                .statusCode(200)
                .extract().jsonPath().getString("answer");
    }

    private static boolean containsWord(String text, String expected) {
        Pattern pattern = Pattern.compile("\\b" + Pattern.quote(expected) + "\\b", Pattern.CASE_INSENSITIVE);
        return pattern.matcher(text).find();
    }

    @ParameterizedTest(name = "{0}")
    @MethodSource("rag.GoldenDataset#load")
    void answerContainsExpectedFacts(GoldenCase goldenCase) {
        String answer = ask(goldenCase.question()).replace('\u2019', '\'');
        System.out.println(goldenCase.id() + ": " + answer);

        boolean allFound = goldenCase.answerContains().stream()
                .allMatch(expected -> containsWord(answer, expected));

        if (KNOWN_FAILURES.containsKey(goldenCase.id())) {
            System.out.println("  Known failure: " + KNOWN_FAILURES.get(goldenCase.id()));
            assertFalse(allFound, goldenCase.id()
                    + " is a known failure but now passes. Remove it from KNOWN_FAILURES.");
            return;
        }

        assertTrue(allFound, goldenCase.id() + ": expected " + goldenCase.answerContains()
                + " in answer, got: " + answer);
    }
}