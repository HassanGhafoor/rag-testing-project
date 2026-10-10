package rag;

import java.util.List;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

@JsonIgnoreProperties(ignoreUnknown = true)

public record GoldenCase(
        String id,
        String question,
        List<String> expectedSources,
        List<String> answerContains,
        boolean answerable) {

    @Override
    public String toString() {
        return id;
    }
}