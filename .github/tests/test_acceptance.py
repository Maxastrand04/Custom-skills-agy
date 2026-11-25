import contextlib
import importlib.util
import io
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent.parent
spec = importlib.util.spec_from_file_location(
    "release_page", ROOT / ".github/scripts/release_page.py"
)
release_page = importlib.util.module_from_spec(spec)
spec.loader.exec_module(release_page)

UPSTREAM = "https://github.com/Maxastrand04/Custom-skills/releases/tag/"
PINNED_INSTALL = "agy plugin install https://github.com/Maxastrand04/Custom-skills-agy/tree/"
BAD_TAGS = ("v1.2", "1.2.3", "v1.2.3-rc1", "latest", "v1.2.3.4", "va.b.c", "")


def run_main(argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = release_page.main(argv)
    return code, out.getvalue(), err.getvalue()


class ReleaseNoteTests(unittest.TestCase):
    def test_note_links_to_the_matching_custom_skills_release(self):
        """The note links to the Custom-skills release page for the same tag."""
        self.assertIn(UPSTREAM + "v2.0.0", release_page.release_note("v2.0.0"))

    def test_note_gives_the_install_command_pinned_to_the_tag(self):
        """The note gives the agy install command pinned to this tag."""
        self.assertIn(PINNED_INSTALL + "v2.0.0", release_page.release_note("v2.0.0"))

    def test_multi_digit_versions_are_accepted(self):
        """A tag with multi-digit numbers, like v1.10.23, gets a note linking that exact tag."""
        self.assertIn(UPSTREAM + "v1.10.23", release_page.release_note("v1.10.23"))

    def test_note_names_no_other_tag(self):
        """The note for one tag carries no other release's tag."""
        self.assertNotIn("v2.0.0", release_page.release_note("v3.1.4"))

    def test_bad_tags_are_refused(self):
        """A tag not shaped vX.Y.Z raises ValueError."""
        for tag in BAD_TAGS:
            with self.subTest(tag=tag):
                with self.assertRaises(ValueError):
                    release_page.release_note(tag)

    def test_refusal_names_the_tag(self):
        """The ValueError for a bad tag names that tag."""
        with self.assertRaises(ValueError) as caught:
            release_page.release_note("v1.2.3-rc1")
        self.assertIn("v1.2.3-rc1", str(caught.exception))


class MainTests(unittest.TestCase):
    def test_good_tag_succeeds(self):
        """A vX.Y.Z tag returns 0."""
        code, _, _ = run_main(["v2.0.0"])
        self.assertEqual(code, 0)

    def test_good_tag_prints_the_note(self):
        """A vX.Y.Z tag prints release_note(tag) to stdout."""
        _, out, _ = run_main(["v2.0.0"])
        self.assertEqual(out.strip(), release_page.release_note("v2.0.0").strip())

    def test_bad_tag_fails(self):
        """A tag not shaped vX.Y.Z returns 1."""
        code, _, _ = run_main(["v1.2"])
        self.assertEqual(code, 1)

    def test_bad_tag_prints_nothing_to_stdout(self):
        """A bad tag leaves stdout empty, so no notes file gets written."""
        _, out, _ = run_main(["v1.2"])
        self.assertEqual(out, "")

    def test_bad_tag_is_named_on_stderr(self):
        """A bad tag prints a line naming the tag to stderr."""
        _, _, err = run_main(["v1.2"])
        self.assertIn("v1.2", err)

    def test_no_argument_fails(self):
        """No argument returns 1."""
        code, _, _ = run_main([])
        self.assertEqual(code, 1)

    def test_no_argument_prints_nothing_to_stdout(self):
        """No argument leaves stdout empty."""
        _, out, _ = run_main([])
        self.assertEqual(out, "")

    def test_no_argument_explains_on_stderr(self):
        """No argument prints a reason to stderr."""
        _, _, err = run_main([])
        self.assertNotEqual(err.strip(), "")

    def test_extra_arguments_fail(self):
        """More than one argument returns 1."""
        code, _, _ = run_main(["v2.0.0", "v2.0.1"])
        self.assertEqual(code, 1)

    def test_extra_arguments_print_nothing_to_stdout(self):
        """More than one argument leaves stdout empty."""
        _, out, _ = run_main(["v2.0.0", "v2.0.1"])
        self.assertEqual(out, "")

    def test_extra_arguments_explain_on_stderr(self):
        """More than one argument prints a reason to stderr."""
        _, _, err = run_main(["v2.0.0", "v2.0.1"])
        self.assertNotEqual(err.strip(), "")


if __name__ == "__main__":
    unittest.main()
