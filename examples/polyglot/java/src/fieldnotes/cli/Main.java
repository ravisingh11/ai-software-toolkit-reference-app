package fieldnotes.cli;

import fieldnotes.domain.Transition;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;

/** TSV adapter. Domain failures are results; malformed transport input is an error. */
public final class Main {
    private Main() {
    }

    public static void main(String[] args) throws Exception {
        try (BufferedReader reader = new BufferedReader(
                new InputStreamReader(System.in, StandardCharsets.UTF_8))) {
            String line;
            while ((line = reader.readLine()) != null) {
                String[] fields = line.split("\t", -1);
                if (fields.length != 6) {
                    throw new IllegalArgumentException("Expected six TSV fields");
                }
                String result = Transition.apply(fields[1], fields[2], fields[3],
                        fields[4], fields[5]);
                System.out.println(fields[0] + "\t" + result);
            }
        }
    }
}
