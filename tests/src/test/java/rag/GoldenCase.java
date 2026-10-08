package rag;

import java.util.List;

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