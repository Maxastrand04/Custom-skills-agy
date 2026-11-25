#!/usr/bin/env python3
"""Write the release page note for a Custom-skills-agy tag. No extra packages.

Lives under .github/ because a Custom-skills Release replaces every other
tracked file in this repo except README.md.
"""

import re
import sys

_TAG_SHAPE = re.compile(r"v[0-9]+\.[0-9]+\.[0-9]+")
_UPSTREAM_RELEASE_URL = "https://github.com/Maxastrand04/Custom-skills/releases/tag/"
_AGY_TREE_URL = "https://github.com/Maxastrand04/Custom-skills-agy/tree/"


def release_note(tag):
    """Return the Markdown note for the release page of `tag`.

    tag: a git tag name, required, shaped exactly "vX.Y.Z" where X, Y and Z
        are decimal numbers, such as "v2.0.0" or "v1.10.3".

    The note is short and holds exactly two things:
    - a link to the matching Custom-skills release page,
      https://github.com/Maxastrand04/Custom-skills/releases/tag/<tag>
    - the install command pinned to this tag,
      agy plugin install https://github.com/Maxastrand04/Custom-skills-agy/tree/<tag>

    It copies no text from the Custom-skills release note.

    Raises ValueError, naming the tag, when `tag` is not shaped "vX.Y.Z",
    such as "v1.2", "1.2.3", "v1.2.3-rc1" or "latest". The workflow's trigger
    already skips such tags, so this only fires if that filter is wrong.

    Pure: reads nothing, writes nothing, calls nothing outside this process.
    """
    if not _TAG_SHAPE.fullmatch(tag):
        raise ValueError(f"tag {tag!r} is not shaped vX.Y.Z")
    return (
        f"[Custom-skills {tag} release notes]({_UPSTREAM_RELEASE_URL}{tag})\n"
        "\n"
        "```sh\n"
        f"agy plugin install {_AGY_TREE_URL}{tag}\n"
        "```\n"
    )


def main(argv):
    """Run from the command line: release_page.py <tag>.

    argv: the arguments after the script name, required, a list holding
        exactly one tag name.

    Prints release_note(tag) to stdout and returns 0. The workflow redirects
    it to a file and hands that to `gh release create --notes-file`.

    Returns 1, printing nothing to stdout and one line naming the problem to
    stderr, when the tag is not shaped "vX.Y.Z" or argv does not hold exactly
    one argument.
    """
    if len(argv) != 1:
        print(f"expected exactly one tag, got {len(argv)} arguments", file=sys.stderr)
        return 1
    try:
        note = release_note(argv[0])
    except ValueError as error:
        print(error, file=sys.stderr)
        return 1
    print(note, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
