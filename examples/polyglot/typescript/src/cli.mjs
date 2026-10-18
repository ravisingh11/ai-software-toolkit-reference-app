import { readFileSync } from "node:fs";
import { transitionIssue } from "./domain.ts";

for (const line of readFileSync(0, "utf8").split("\n").filter(Boolean)) {
  const fields = line.split("\t");
  if (fields.length !== 6) throw new Error("Expected six TSV fields.");
  const [id, role, session, issue, current, requested] = fields;
  process.stdout.write(
    `${id}\t${transitionIssue(role, session, issue, current, requested)}\n`,
  );
}
