"""Selbsttest fuer scripts/lint-skills.py.

Die Fixture-Skills entstehen zur Laufzeit in einem Temp-Ordner (keine eingecheckten
dtb:-Dateien im Baum, CRLF exakt geschrieben). Aufruf vom Repo-Root:

    python -m unittest discover -s scripts/tests

Jeder Test prueft die EXAKTE Menge der Befundzeilen (Stufe, Skill, Regel) — eine
zusaetzliche Falschmeldung faellt so auf, nicht nur eine fehlende.
"""

import sys

sys.dont_write_bytecode = True

import collections
import importlib.util
import os
import re
import subprocess
import tempfile
import unittest

SCRIPT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "lint-skills.py")
FINDING_RE = re.compile(r"^(FEHLER|WARNUNG) (\S+): (\S+) — ", re.M)

DEFAULT = {
    "name": "name: dtb:{short}",
    "description": 'description: >-\n  Use when: "probe". Checks a fixture skill.',
    "dmi": "disable-model-invocation: true",
    "tools": "allowed-tools: Read, Glob, Grep",
    "pipeline": "pipeline:\n  stage: planning\n  after: {after}\n  next: {next}\n  consumes: []\n  produces: []",
}
ORDER = ("name", "description", "dmi", "tools", "pipeline")


def skill_text(short, after="null", next_="null", body="# Fixture\n", **parts):
    """Baut eine SKILL.md; parts ueberschreibt Frontmatter-Teile, None laesst sie weg."""
    lines = []
    for key in ORDER:
        value = parts.get(key, DEFAULT[key])
        if value is not None:
            lines.append(value.format(short=short, after=after, next=next_))
    return "---\n" + "\n".join(lines) + "\n---\n" + body


def findings(text):
    return collections.Counter(FINDING_RE.findall(text))


def expect(*items):
    return collections.Counter(items)


def load_module():
    spec = importlib.util.spec_from_file_location("lint_skills", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class LintCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = self._tmp.name
        os.mkdir(os.path.join(self.root, "skills"))

    def tearDown(self):
        self._tmp.cleanup()

    def write(self, short, text, crlf=False):
        folder = os.path.join(self.root, "skills", "dtb-" + short)
        os.makedirs(folder, exist_ok=True)
        data = text.replace("\n", "\r\n") if crlf else text
        with open(os.path.join(folder, "SKILL.md"), "wb") as handle:
            handle.write(data.encode("utf-8"))

    def pair(self, alpha=None, beta=None, crlf=False):
        """Zwei Skills mit sauberer Gegenkante alpha.next <-> beta.after."""
        self.write("alpha", alpha or skill_text("alpha", next_="[dtb:beta]"), crlf)
        self.write("beta", beta or skill_text("beta", after="[dtb:alpha]"), crlf)

    def run_lint(self, root=None):
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8")
        result = subprocess.run(
            [sys.executable, SCRIPT, "--ohne-ausnahmen", root or self.root],
            capture_output=True, text=True, encoding="utf-8", env=env,
        )
        return result.returncode, result.stdout, result.stderr

    def assert_findings(self, expected, exit_code=None):
        """Exakte Befundmenge; Exit-Code 1 bei mindestens einem FEHLER, sonst 0."""
        code, out, err = self.run_lint()
        self.assertEqual(findings(out), expected, out + err)
        if exit_code is None:
            exit_code = 1 if any(level == "FEHLER" for level, _, _ in expected) else 0
        self.assertEqual(code, exit_code, out + err)
        return out


class GreenTests(LintCase):
    def test_clean_pair_is_green(self):
        self.pair()
        out = self.assert_findings(expect())
        self.assertIn("2 Skills geprueft, 0 FEHLER, 0 WARNUNG(EN)", out)

    def test_crlf_clean_pair_is_green(self):
        self.pair(crlf=True)
        self.assert_findings(expect())

    def test_crlf_does_not_hide_errors(self):
        self.pair(alpha=skill_text("alpha", next_="[dtb:beta]", name="name: dtb:wrong"), crlf=True)
        self.assert_findings(expect(("FEHLER", "dtb-alpha", "name-verzeichnis")))

    def test_missing_skills_dir_is_exit_2(self):
        with tempfile.TemporaryDirectory() as empty:
            code, _, err = self.run_lint(empty)
        self.assertEqual(code, 2)
        self.assertIn("kein Ordner skills/", err)

    def test_unexpected_error_is_exit_2(self):
        module = load_module()

        def broken(*_args, **_kwargs):
            raise RuntimeError("kaputt")

        module.lint = broken
        stderr = sys.stderr
        sys.stderr = open(os.devnull, "w", encoding="utf-8")
        try:
            self.assertEqual(module.main(["lint-skills.py", self.root]), 2)
        finally:
            sys.stderr.close()
            sys.stderr = stderr


class ErrorTests(LintCase):
    def test_directory_without_skill_md(self):
        self.pair()
        os.mkdir(os.path.join(self.root, "skills", "dtb-empty"))
        self.assert_findings(expect(("FEHLER", "dtb-empty", "skill-md-fehlt")))

    def test_no_frontmatter(self):
        self.pair()
        self.write("gamma", "# kein Frontmatter\n")
        self.assert_findings(expect(("FEHLER", "dtb-gamma", "frontmatter")))

    def test_invalid_yaml(self):
        self.pair()
        self.write("gamma", "---\nname: dtb:gamma\ndescription: [offen\n---\n")
        self.assert_findings(expect(("FEHLER", "dtb-gamma", "frontmatter")))

    def test_name_missing(self):
        self.pair(beta=skill_text("beta", after="[dtb:alpha]", name=None))
        self.assert_findings(expect(("FEHLER", "dtb-beta", "name-fehlt")))

    def test_description_missing(self):
        self.pair(beta=skill_text("beta", after="[dtb:alpha]", description=None))
        self.assert_findings(expect(("FEHLER", "dtb-beta", "description-fehlt")))

    def test_description_not_text(self):
        self.pair(beta=skill_text("beta", after="[dtb:alpha]", description="description: 42"))
        self.assert_findings(expect(("FEHLER", "dtb-beta", "use-when")))

    def test_name_does_not_match_directory(self):
        self.pair(beta=skill_text("beta", after="[dtb:alpha]", name="name: dtb:gamma"))
        self.assert_findings(expect(("FEHLER", "dtb-beta", "name-verzeichnis")))

    def test_use_when_prefix(self):
        self.pair(beta=skill_text("beta", after="[dtb:alpha]", description="description: Checks things."))
        self.assert_findings(expect(("FEHLER", "dtb-beta", "use-when")))

    def test_edge_not_a_list(self):
        # nur `listenform` beim Verursacher — keine Folge-Meldung `gegenkante` beim Ziel
        self.pair(alpha=skill_text("alpha", next_="dtb:beta"))
        self.assert_findings(expect(("FEHLER", "dtb-alpha", "listenform")))

    def test_edge_target_missing(self):
        self.pair(alpha=skill_text("alpha", next_="[dtb:beta, dtb:gamma]"))
        self.assert_findings(expect(("FEHLER", "dtb-alpha", "kanten-ziel")))

    def test_one_way_next_edge(self):
        self.pair(beta=skill_text("beta"))
        self.assert_findings(expect(("FEHLER", "dtb-alpha", "gegenkante")))

    def test_one_way_after_edge(self):
        self.pair(alpha=skill_text("alpha"))
        self.assert_findings(expect(("FEHLER", "dtb-beta", "gegenkante")))

    def test_stage_outside_enum(self):
        pipeline = DEFAULT["pipeline"].replace("planning", "deploy")
        self.pair(beta=skill_text("beta", after="[dtb:alpha]", pipeline=pipeline))
        self.assert_findings(expect(("FEHLER", "dtb-beta", "stage")))

    def test_pipeline_not_a_block(self):
        self.pair()
        self.write("gamma", skill_text("gamma", pipeline="pipeline: planning"))
        self.assert_findings(expect(("FEHLER", "dtb-gamma", "pipeline")))


class LengthTests(LintCase):
    @staticmethod
    def described(short, length, dmi="false", **kw):
        prefix = 'Use when: "probe". '
        filler = ("x" * 40 + " ") * 20
        text = (prefix + filler)[:length]
        # gefaltet ueber mehrere Zeilen: Umbruch + Einrueckung zaehlen als ein Leerzeichen
        words = text.split(" ")
        block = "description: >-\n  " + " ".join(words[:5]) + "\n  " + " ".join(words[5:])
        dmi_line = None if dmi is None else f"disable-model-invocation: {dmi}"
        return skill_text(short, description=block, dmi=dmi_line, **kw)

    def test_exactly_limit_is_green(self):
        self.pair(beta=self.described("beta", 350, after="[dtb:alpha]"))
        self.assert_findings(expect())

    def test_one_over_limit_is_error(self):
        self.pair(beta=self.described("beta", 351, after="[dtb:alpha]"))
        out = self.assert_findings(expect(("FEHLER", "dtb-beta", "beschreibung-laenge")))
        self.assertIn("351 Zeichen", out)

    def test_missing_dmi_counts_as_model_invocation(self):
        self.pair(beta=self.described("beta", 351, dmi=None, after="[dtb:alpha]"))
        self.assert_findings(expect(
            ("FEHLER", "dtb-beta", "beschreibung-laenge"),
            ("WARNUNG", "dtb-beta", "feld-fehlt"),
        ))

    def test_dmi_string_is_error_and_length_counts(self):
        self.pair(beta=self.described("beta", 351, dmi='"false"', after="[dtb:alpha]"))
        self.assert_findings(expect(
            ("FEHLER", "dtb-beta", "dmi-typ"),
            ("FEHLER", "dtb-beta", "beschreibung-laenge"),
        ))

    def test_limit_ignored_without_model_invocation(self):
        self.pair(beta=self.described("beta", 400, dmi="true", after="[dtb:alpha]"))
        self.assert_findings(expect())


class ToolTests(LintCase):
    def tool_case(self, body, tools=None):
        parts = {"tools": tools} if tools else {}
        self.pair(beta=skill_text("beta", after="[dtb:alpha]", body=body, **parts))

    def test_bash_fence_without_bash(self):
        self.tool_case("# Fixture\n\n```bash\ngit status\n```\n")
        self.assert_findings(expect(("FEHLER", "dtb-beta", "werkzeug-bash")))

    def test_sh_and_tilde_fences_without_bash(self):
        for fence in ("```sh", "```shell", "~~~bash"):
            with self.subTest(fence=fence):
                self.tool_case(f"# Fixture\n\n{fence}\ngit status\n{fence[:3]}\n")
                self.assert_findings(expect(("FEHLER", "dtb-beta", "werkzeug-bash")))

    def test_worktree_guard_without_bash(self):
        for heading in ("## Worktree-Guard", "### Worktree-Guard"):
            with self.subTest(heading=heading):
                self.tool_case(f"# Fixture\n\n{heading}\n\nSiehe Vorlage.\n")
                self.assert_findings(expect(("FEHLER", "dtb-beta", "werkzeug-bash")))

    def test_indented_part_guard_without_bash(self):
        # der #195-Fall: Teil-Guard eingerueckt in einer Liste, Body ohne das Wort "Bash"
        self.tool_case("# Fixture\n\n6. **Schritt**\n\n   **Teil-Guard (Worktree):** Siehe Vorlage.\n")
        self.assert_findings(expect(("FEHLER", "dtb-beta", "werkzeug-bash")))

    def test_guard_with_bash_variants_is_green(self):
        body = "# Fixture\n\n**Teil-Guard (Worktree):** Siehe Vorlage.\n"
        for tools in ("allowed-tools: Read, Bash", "allowed-tools: [Read, Bash]",
                      "allowed-tools: Read, Bash(git:*)"):
            with self.subTest(tools=tools):
                self.tool_case(body, tools=tools)
                self.assert_findings(expect())


class WarningTests(LintCase):
    def test_missing_optional_fields_warn_only(self):
        self.pair()
        self.write("gamma", skill_text("gamma", dmi=None, tools=None, pipeline=None))
        out = self.assert_findings(expect(*[("WARNUNG", "dtb-gamma", "feld-fehlt")] * 3))
        for field in ("disable-model-invocation", "allowed-tools", "pipeline"):
            self.assertIn(f"WARNUNG dtb-gamma: feld-fehlt — {field} fehlt", out)


class ExceptionTests(LintCase):
    def setUp(self):
        super().setUp()
        self.module = load_module()

    def lint_with(self, exceptions):
        _, report = self.module.lint(self.root, exceptions)
        return findings("\n".join(report.lines)), report

    def test_exception_silences_one_way_next_edge(self):
        self.pair(beta=skill_text("beta"))
        got, report = self.lint_with((("dtb:alpha", "next", "dtb:beta", "Lese-Sicht"),))
        self.assertEqual(got, expect(), report.lines)

    def test_exception_silences_one_way_after_edge(self):
        self.pair(alpha=skill_text("alpha"))
        got, report = self.lint_with((("dtb:beta", "after", "dtb:alpha", "Lese-Sicht"),))
        self.assertEqual(got, expect(), report.lines)

    def test_exception_with_existing_counter_edge_warns(self):
        self.pair()
        got, report = self.lint_with((("dtb:alpha", "next", "dtb:beta", "Lese-Sicht"),))
        self.assertEqual(got, expect(("WARNUNG", "lint-skills", "ausnahme-ueberfluessig")), report.lines)
        self.assertIn("Gegenkante existiert inzwischen", "\n".join(report.lines))

    def test_exception_without_edge_warns(self):
        self.pair()
        got, report = self.lint_with((("dtb:beta", "next", "dtb:alpha", "Lese-Sicht"),))
        self.assertEqual(got, expect(("WARNUNG", "lint-skills", "ausnahme-ueberfluessig")), report.lines)
        self.assertIn("deckt keine bestehende Kante", "\n".join(report.lines))

    def test_exception_with_vanished_skill_warns(self):
        self.pair()
        got, report = self.lint_with((("dtb:gone", "next", "dtb:other", "Lese-Sicht"),))
        self.assertEqual(got, expect(("WARNUNG", "lint-skills", "ausnahme-ueberfluessig")), report.lines)
        self.assertIn("Quelle oder Ziel fehlt", "\n".join(report.lines))

    def test_exception_without_reason_is_error(self):
        self.pair(beta=skill_text("beta"))
        got, report = self.lint_with((("dtb:alpha", "next", "dtb:beta", " "),))
        self.assertEqual(got, expect(("FEHLER", "lint-skills", "ausnahme-grund")), report.lines)

    def test_exception_with_unknown_field_is_error(self):
        self.pair(beta=skill_text("beta"))
        got, report = self.lint_with((("dtb:alpha", "nxt", "dtb:beta", "Lese-Sicht"),))
        self.assertEqual(got, expect(
            ("FEHLER", "lint-skills", "ausnahme-feld"),
            ("FEHLER", "dtb-alpha", "gegenkante"),
        ), report.lines)


if __name__ == "__main__":
    unittest.main()
