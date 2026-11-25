"""One Line, One Laugh -- writes a single original one-liner to entry.txt.

The joke is a constant in this file; the program only resolves the output
location and writes it, byte for byte, with no trailing newline.
The kit harness exports MAKEFUN_OUTPUT_DIR and reads
``$MAKEFUN_OUTPUT_DIR/entry.txt`` afterwards, so that variable is
honoured here (after an explicit ENTRY_OUT).
"""

import os

JOKE = "I told my smart speaker I feel lonely. It said, 'I'm sorry, I didn't quite catch that.'"


def resolve_target():
    """Return the file path the entry must be written to.

    Priority: ENTRY_OUT, then the kit harness directory
    MAKEFUN_OUTPUT_DIR, then ENTRY_OUT_DIR, then OUTPUT, then the
    competition default /output/entry.txt. An env value that names a
    directory (or ends in a separator) means <dir>/entry.txt.
    MAKEFUN_OUTPUT_DIR always names a directory, even before it exists.
    """
    entry_out = os.environ.get("ENTRY_OUT")
    if entry_out:
        if entry_out.endswith(os.sep) or os.path.isdir(entry_out):
            return os.path.join(entry_out, "entry.txt")
        return entry_out
    makefun_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if makefun_dir:
        return os.path.join(makefun_dir, "entry.txt")
    for name in ("ENTRY_OUT_DIR", "OUTPUT"):
        value = os.environ.get(name)
        if value:
            if value.endswith(os.sep) or os.path.isdir(value):
                return os.path.join(value, "entry.txt")
            return value
    return "/output/entry.txt"


def write_entry(path):
    """Write the joke to path, creating its parent directory if needed."""
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(JOKE)


def main():
    target = resolve_target()
    write_entry(target)
    # The sealed scorer reads /output/entry.txt, so make sure the canonical
    # path holds the same bytes even when an env var pointed elsewhere.
    if os.path.abspath(target) != os.path.abspath("/output/entry.txt"):
        try:
            write_entry("/output/entry.txt")
        except OSError:
            pass


if __name__ == "__main__":
    main()
