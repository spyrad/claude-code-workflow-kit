"""Selbsttest fuer scripts/lint-skills.py.

Die Fixture-Skills entstehen zur Laufzeit in einem Temp-Ordner (keine eingecheckten
dtb:-Dateien im Baum, CRLF exakt geschrieben). Aufruf vom Repo-Root:

    python -m unittest discover -s scripts/tests
"""

import sys

sys.dont_write_bytecode = True

import importlib.util
import os
import subprocess
import tempfile
import unittest

SCRIPT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "lint-skills.py")

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
            [sys.executable, SCRIPT, root or self.root],
            capture_output=True, text=True, encoding="utf-8", env=env,
        )
        return result.returncode, result.stdout, result.stderr

    def assert_finding(self, level, skill, rule, exit_code=1):
        code, out, err = self.run_lint()
        self.assertEqual(code, exit_code, out + err)
        self.assertIn(f"{level} dtb-{skill}: {rule} — ", out)
        return out


class GreenTests(LintCase):
    def test_clean_pair_is_green(self):
        self.pair()
        code, out, _ = self.run_lint()
        self.assertEqual(code, 0, out)
        self.assertIn("2 Skills geprueft, 0 FEHLER, 0 WARNUNG(EN)", out)

    def test_crlf_clean_pair_is_green(self):
        self.pair(crlf=True)
        code, out, _ = self.run_lint()
        self.assertEqual(code, 0, out)

    def test_crlf_does_not_hide_errors(self):
        self.pair(alpha=skill_text("alpha", next_="[dtb:beta]", name="name: dtb:wrong"), crlf=True)
        self.assert_finding("FEHLER", "alpha", "name-verzeichnis")

    def test_missing_skills_dir_is_exit_2(self):
        with tempfile.TemporaryDirectory() as empty:
            code, _, err = self.run_lint(empty)
        self.assertEqual(code, 2)
        self.assertIn("kein Ordner skills/", err)


class ErrorTests(LintCase):
    def test_directory_without_skill_md(self):
        self.pair()
        os.mkdir(os.path.join(self.root, "skills", "dtb-empty"))
        self.assert_finding("FEHLER", "empty", "skill-md-fehlt")

    def test_no_frontmatter(self):
        self.pair()
        self.write("gamma", "# kein Frontmatter\n")
        self.assert_finding("FEHLER", "gamma", "frontmatter")

    def test_invalid_yaml(self):
        self.pair()
        self.write("gamma", "---\nname: dtb:gamma\ndescription: [offen\n---\n")
        self.assert_finding("FEHLER", "gamma", "frontmatter")

    def test_name_missing(self):
        self.pair(beta=skill_text("beta", after="[dtb:alpha]", name=None))
        self.assert_finding("FEHLER", "beta", "name-fehlt")

    def test_description_missing(self):
        self.pair(beta=skill_text("beta", after="[dtb:alpha]", description=None))
        self.assert_finding("FEHLER", "beta", "description-fehlt")

    def test_name_does_not_match_directory(self):
        self.pair(beta=skill_text("beta", after="[dtb:alpha]", name="name: dtb:gamma"))
        self.assert_finding("FEHLER", "beta", "name-verzeichnis")

    def test_use_when_prefix(self):
        self.pair(beta=skill_text("beta", after="[dtb:alpha]", description="description: Checks things."))
        self.assert_finding("FEHLER", "beta", "use-when")

    def test_edge_not_a_list(self):
        self.pair(alpha=skill_text("alpha", next_="dtb:beta"))
        self.assert_finding("FEHLER", "alpha", "listenform")

    def test_edge_target_missing(self):
        self.pair(alpha=skill_text("alpha", next_="[dtb:beta, dtb:gamma]"))
        self.assert_finding("FEHLER", "alpha", "kanten-ziel")

    def test_one_way_edge(self):
        self.pair(beta=skill_text("beta"))
        self.assert_finding("FEHLER", "alpha", "gegenkante")

    def test_stage_outside_enum(self):
        pipeline = DEFAULT["pipeline"].replace("planning", "deploy")
        self.pair(beta=skill_text("beta", after="[dtb:alpha]", pipeline=pipeline))
        self.assert_finding("FEHLER", "beta", "stage")

    def test_pipeline_not_a_block(self):
        self.pair()
        self.write("gamma", skill_text("gamma", pipeline="pipeline: planning"))
        self.assert_finding("FEHLER", "gamma", "pipeline")


class LengthTests(LintCase):
    @staticmethod
    def described(short, length, dmi="false", **kw):
        prefix = 'Use when: "probe". '
        filler = ("x" * 40 + " ") * 20
        text = (prefix + filler)[:length]
        # gefaltet ueber mehrere Zeilen: Umbruch + Einrueckung zaehlen als ein Leerzeichen
        words = text.split(" ")
        block = "description: >-\n  " + " ".join(words[:5]) + "\n  " + " ".join(words[5:])
        return skill_text(short, description=block, dmi=f"disable-model-invocation: {dmi}", **kw)

    def test_exactly_limit_is_green(self):
        self.pair(beta=self.described("beta", 350, after="[dtb:alpha]"))
        code, out, _ = self.run_lint()
        self.assertEqual(code, 0, out)

    def test_one_over_limit_is_error(self):
        self.pair(beta=self.described("beta", 351, after="[dtb:alpha]"))
        out = self.assert_finding("FEHLER", "beta", "beschreibung-laenge")
        self.assertIn("351 Zeichen", out)

    def test_limit_ignored_without_model_invocation(self):
        self.pair(beta=self.described("beta", 400, dmi="true", after="[dtb:alpha]"))
        code, out, _ = self.run_lint()
        self.assertEqual(code, 0, out)


class ToolTests(LintCase):
    def test_bash_fence_without_bash(self):
        body = "# Fixture\n\n```bash\ngit status\n```\n"
        self.pair(beta=skill_text("beta", after="[dtb:alpha]", body=body))
        self.assert_finding("FEHLER", "beta", "werkzeug-bash")

    def test_worktree_guard_without_bash(self):
        body = "# Fixture\n\n## Worktree-Guard\n\nSiehe Vorlage.\n"
        self.pair(beta=skill_text("beta", after="[dtb:alpha]", body=body))
        self.assert_finding("FEHLER", "beta", "werkzeug-bash")

    def test_indented_part_guard_without_bash(self):
        # der #195-Fall: Teil-Guard eingerueckt in einer Liste, Body ohne das Wort "Bash"
        body = "# Fixture\n\n6. **Schritt**\n\n   **Teil-Guard (Worktree):** Siehe Vorlage.\n"
        self.pair(beta=skill_text("beta", after="[dtb:alpha]", body=body))
        self.assert_finding("FEHLER", "beta", "werkzeug-bash")

    def test_guard_with_bash_is_green(self):
        body = "# Fixture\n\n**Teil-Guard (Worktree):** Siehe Vorlage.\n"
        tools = "allowed-tools: Read, Bash"
        self.pair(beta=skill_text("beta", after="[dtb:alpha]", body=body, tools=tools))
        code, out, _ = self.run_lint()
        self.assertEqual(code, 0, out)


class WarningTests(LintCase):
    def test_missing_optional_fields_warn_only(self):
        self.pair()
        self.write("gamma", skill_text("gamma", dmi=None, tools=None, pipeline=None))
        code, out, _ = self.run_lint()
        self.assertEqual(code, 0, out)
        for field in ("disable-model-invocation", "allowed-tools", "pipeline"):
            self.assertIn(f"WARNUNG dtb-gamma: feld-fehlt — {field} fehlt", out)


class ExceptionTests(LintCase):
    def setUp(self):
        super().setUp()
        self.module = load_module()

    def lint_with(self, exceptions):
        self.module.EDGE_EXCEPTIONS = exceptions
        _, report = self.module.lint(self.root)
        return report

    def test_exception_silences_one_way_edge(self):
        self.pair(beta=skill_text("beta"))
        report = self.lint_with((("dtb:alpha", "next", "dtb:beta", "Lese-Sicht"),))
        self.assertEqual(report.errors, 0, report.lines)
        self.assertEqual(report.warnings, 0, report.lines)

    def test_stale_exception_warns(self):
        self.pair()
        report = self.lint_with((("dtb:alpha", "next", "dtb:beta", "Lese-Sicht"),))
        self.assertEqual(report.errors, 0, report.lines)
        self.assertTrue(any("ausnahme-ueberfluessig" in line for line in report.lines), report.lines)

    def test_exception_with_vanished_source_warns(self):
        self.pair()
        report = self.lint_with((("dtb:gone", "next", "dtb:beta", "Lese-Sicht"),))
        self.assertTrue(any("ausnahme-ueberfluessig" in line for line in report.lines), report.lines)

    def test_exception_foreign_tree_is_silent(self):
        self.pair()
        report = self.lint_with((("dtb:gone", "next", "dtb:other", "Lese-Sicht"),))
        self.assertEqual(report.warnings, 0, report.lines)

    def test_exception_without_reason_is_error(self):
        self.pair(beta=skill_text("beta"))
        report = self.lint_with((("dtb:alpha", "next", "dtb:beta", " "),))
        self.assertTrue(any("ausnahme-grund" in line for line in report.lines), report.lines)
        self.assertGreater(report.errors, 0)


if __name__ == "__main__":
    unittest.main()
