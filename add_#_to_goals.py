import re
from pathlib import Path


def rename_gl_goals(text: str, suffix: str = "-#001") -> str:
    # Matcher tokens der starter med gl- og fortsætter indtil whitespace,
    # parentes, semikolon eller anden tydelig separator.
    pattern = re.compile(r'gl-[^\s()";]+')

    def repl(match: re.Match) -> str:
        name = match.group(0)

        # Undgå at sætte suffix på flere gange
        if name.endswith(suffix):
            return name

        return f"{name}{suffix}"

    return pattern.sub(repl, text)


def process_file(
    input_path: str, output_path: str | None = None, suffix: str = "-#001"
) -> None:
    input_file = Path(input_path)

    if output_path is None:
        output_file = input_file.with_name(
            f"{input_file.stem}_renamed{input_file.suffix}"
        )
    else:
        output_file = Path(output_path)

    content = input_file.read_text(encoding="utf-8")
    updated = rename_gl_goals(content, suffix=suffix)
    output_file.write_text(updated, encoding="utf-8")

    print(f"Færdig. Gemt i: {output_file}")


if __name__ == "__main__":
    # Eksempel:
    # process_file("Rehoboam 1.80g.per")
    process_file("anti_overkill_ny.per")
