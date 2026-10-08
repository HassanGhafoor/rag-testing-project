package rag;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.IOException;
import java.nio.file.Path;
import java.util.List;

public final class GoldenDataset {

    private static final Path GOLDEN_FILE = Path.of("..", "golden", "golden.json");

    private GoldenDataset() {
    }

    public static List<GoldenCase> load() {
        try {
            return new ObjectMapper().readValue(GOLDEN_FILE.toFile(), new TypeReference<>() {});
        } catch (IOException e) {
            throw new IllegalStateException(
                    "Could not read golden dataset at " + GOLDEN_FILE.toAbsolutePath(), e);
        }
    }

    public static List<GoldenCase> answerable() {
        return load().stream().filter(GoldenCase::answerable).toList();
    }
}