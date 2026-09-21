"""Frente E (P-16) — identity and hygiene of the motors.

Inverts four reproductions of the 2026-09-08 adversarial review
(`docs/ADVERSARIAL_REVIEW_2026-09-08.md`, `docs/review-evidence/`):

  F01  a duplicated SU id was accepted in silence: `parsed_rows=2`,
       `drawer_entries=1`, `diagnostics=[]`, and the FIRST fact disappeared.
  F02  a stale lock reattached to whatever answered on that port — server A's
       URL served engagement B.
  F11  a `failed` extraction stayed in the cache after its cause was gone.
  F12  `[x](javascript:...)` in engagement content became an executable href.

Plus P-R13: the library guard compared paths case-sensitively, so
`LIBRARY/kernel/states.md` — the same file on Windows — passed.

    python .claude/tests/test_motor_identity.py
"""

import contextlib
import functools
import io
import json
import os
import runpy
import socketserver
import sys
import tempfile
import threading
import unittest
import urllib.request
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
DASHBOARD = ROOT / "library" / "kernel" / "tools" / "dashboard.py"
TEXT_EXTRACT = ROOT / "library" / "kernel" / "tools" / "text_extract.py"
WRITE_GUARD = ROOT / ".claude" / "hooks" / "pre-write-guard.py"
ROUND_SKILL = ROOT / ".claude" / "skills" / "aisa-round" / "SKILL.md"

D = runpy.run_path(str(DASHBOARD))

SU_DUP = """# Shared Understanding

## Confirmed

| id | lens | claim | evidência | verificado_em | validade | ronda |
|----|------|-------|-----------|---------------|----------|-------|
| C-001 | business | First distinct fact | source A | 2026-09-08 | organizacional | R-01 |
| C-001 | operations | Second distinct fact | source B | 2026-09-08 | organizacional | R-01 |
| C-002 | data | Only fact under this id | source C | 2026-09-08 | organizacional | R-01 |
"""


class DuplicateIds(unittest.TestCase):
    """F01 — the motor cannot pick the right row, so it must report both."""

    def setUp(self):
        _, self.rows, _, self.diagnostics = D["parse_su"](SU_DUP)
        self.payload = D["_ids_payload"](self.rows)

    def test_duplicate_is_an_error_diagnostic_naming_both_lines(self):
        errors = [d for d in self.diagnostics if d["level"] == "error"]
        self.assertEqual(len(errors), 1, self.diagnostics)
        msg = errors[0]["message"]
        self.assertIn("id duplicado: C-001", msg)
        self.assertIn("7, 8", msg)

    def test_first_row_is_kept_and_the_other_is_carried_marked(self):
        rec = self.payload["C-001"]
        self.assertEqual(rec["c"], "First distinct fact")
        self.assertTrue(rec["dp"])
        self.assertEqual([d["c"] for d in rec["dups"]], ["Second distinct fact"])

    def test_rows_carry_the_flag(self):
        flagged = {r["id"] for r in self.rows if r["duplicate_id"]}
        self.assertEqual(flagged, {"C-001"})

    def test_a_unique_id_is_untouched(self):
        self.assertNotIn("dp", self.payload["C-002"])
        self.assertNotIn("dups", self.payload["C-002"])

    def test_clean_su_reports_nothing(self):
        clean = SU_DUP.replace(
            "| C-001 | operations | Second distinct fact",
            "| C-003 | operations | Second distinct fact")
        _, rows, _, diags = D["parse_su"](clean)
        self.assertEqual([d for d in diags if d["level"] == "error"], [])
        self.assertFalse(any(r["duplicate_id"] for r in rows))

    def test_round_recomputes_ids_before_each_lens(self):
        text = ROUND_SKILL.read_text(encoding="utf-8")
        self.assertIn("before EACH lens", text)


class LinkSchemes(unittest.TestCase):
    """F12 — allow-list of schemes; a rejected URL stays visible as text."""

    def test_executable_schemes_never_become_hrefs(self):
        for url in ("javascript:alert(1)", "JaVaScRiPt:alert(1)", "java\tscript:x",
                    "data:text/html;base64,PHN2Zz4=", "vbscript:x", "file:///C:/x",
                    "//evil.example/x"):
            self.assertIsNone(D["safe_href"](url), url)

    def test_safe_targets_pass_through(self):
        for url in ("https://a.pt/x", "http://a.pt/x", "mailto:a@b.pt",
                    "_capture/evidence-index.md", "#seccao", "../inputs/f.xlsx"):
            self.assertEqual(D["safe_href"](url), url, url)

    def test_rendered_output(self):
        out = D["inline_md"]("[Abrir fonte](javascript:alert%281%29)")
        self.assertNotIn("href=", out)
        self.assertIn("javascript:alert%281%29", out)
        self.assertTrue(
            D["inline_md"]("[ok](https://x.pt)").startswith('<a href="https://x.pt">'))

    def test_link_text_is_still_escaped(self):
        out = D["inline_md"]("[<script>](https://x.pt)")
        self.assertNotIn("<script>", out)


class ServerIdentity(unittest.TestCase):
    """F02 — a port is not an identity."""

    def setUp(self):
        self.holder = dict(D["_Handler"].build_holder)

    def tearDown(self):
        D["_Handler"].build_holder.clear()
        D["_Handler"].build_holder.update(self.holder)

    def test_same_server_requires_every_field(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = Path(tmp) / "eng"
            eng.mkdir()
            lock = {"engagement": str(eng.resolve()), "slug": "eng",
                    "pid": 4242, "started": "2026-09-08T10:00:00"}
            ident = dict(lock)
            self.assertTrue(D["_same_server"](lock, ident, eng))
            for field, other in (("pid", 99), ("engagement", "X"),
                                 ("started", "2026-09-08T11:00:00")):
                broken = dict(ident)
                broken[field] = other
                self.assertFalse(D["_same_server"](lock, broken, eng), field)
            # The slug is the PAGE's identity (`_state.json.engagement`), not the
            # server's: a copied engagement keeps the declared slug under another
            # folder name, so the reattach test must not depend on it.
            renamed = dict(ident)
            renamed["slug"] = "outro"
            self.assertTrue(D["_same_server"](lock, renamed, eng))
            self.assertFalse(D["_same_server"](lock, {"build": "hash"}, eng))

    def test_stale_lock_does_not_reattach_to_another_engagement(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            a, b = base / "client-a", base / "client-b"
            for folder, name in ((a, "A"), (b, "B")):
                folder.mkdir()
                (folder / "_state.json").write_text(
                    json.dumps({"client": name}), encoding="utf-8")
            server = socketserver.ThreadingTCPServer(
                ("127.0.0.1", 0),
                functools.partial(D["_Handler"], directory=str(b)))
            threading.Thread(target=server.serve_forever, daemon=True).start()
            port = server.server_address[1]
            original = D["_lock_path"]
            D["_lock_path"] = lambda eng: base / (eng.name + ".lock.json")
            try:
                D["write_lock"](a, port)
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr):
                    running = D["running_server"](a)
                self.assertIsNone(running)
                self.assertFalse((base / "client-a.lock.json").exists())
                # B is still there — what changed is that A refuses it.
                with urllib.request.urlopen(
                        "http://127.0.0.1:{}/_state.json".format(port)) as r:
                    self.assertEqual(json.loads(r.read()), {"client": "B"})
            finally:
                D["_lock_path"] = original
                server.shutdown()
                server.server_close()

    def test_a_server_reattaches_to_its_own_engagement(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = Path(tmp) / "eng"
            eng.mkdir()
            (eng / "_state.json").write_text("{}", encoding="utf-8")
            httpd, port = D["serve"](eng, 8791)
            try:
                ident = D["probe"](port)
                self.assertEqual(ident["engagement"], str(eng.resolve()))
                self.assertEqual(ident["pid"], os.getpid())
                live = D["running_server"](eng)
                self.assertIsNotNone(live)
                self.assertEqual(live[0], port)
            finally:
                httpd.shutdown()
                httpd.server_close()
                D["clear_lock"](eng)


class FailedCacheIsNotAnExtraction(unittest.TestCase):
    """F11 — `failed` / `skipped` record why nothing came out, not an extraction."""

    def _run(self, status):
        te = runpy.run_path(str(TEXT_EXTRACT))
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            src, md, js = base / "i.vtt", base / "i.vtt.text.md", base / "i.vtt.json"
            src.write_text("WEBVTT\n\n00:00:01.000 --> 00:00:02.000\nEVIDENCE\n",
                           encoding="utf-8")
            original = te["EXTRACTORS"][".vtt"]

            def failing(path):
                raise te["ExtractionError"]("simulated", status)

            te["EXTRACTORS"][".vtt"] = failing
            with contextlib.redirect_stdout(io.StringIO()):
                te["extract"](str(src), str(md), str(js), False, None)
            self.assertEqual(json.loads(js.read_text(encoding="utf-8"))["status"], status)
            te["EXTRACTORS"][".vtt"] = original
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                te["extract"](str(src), str(md), str(js), False, None)
            return (json.loads(js.read_text(encoding="utf-8"))["status"],
                    md.read_text(encoding="utf-8"), out.getvalue())

    def test_failed_is_retried_and_says_why(self):
        status, body, log = self._run("failed")
        self.assertEqual(status, "ok")
        self.assertIn("EVIDENCE", body)
        self.assertIn("retry:", log)

    def test_skipped_is_retried_too(self):
        status, body, _ = self._run("skipped")
        self.assertEqual(status, "ok")
        self.assertIn("EVIDENCE", body)

    def test_ok_is_still_cached(self):
        te = runpy.run_path(str(TEXT_EXTRACT))
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            src, md, js = base / "i.vtt", base / "i.vtt.text.md", base / "i.vtt.json"
            src.write_text("WEBVTT\n\n00:00:01.000 --> 00:00:02.000\nEVIDENCE\n",
                           encoding="utf-8")
            with contextlib.redirect_stdout(io.StringIO()):
                te["extract"](str(src), str(md), str(js), False, None)
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                te["extract"](str(src), str(md), str(js), False, None)
            self.assertIn("cache-hit", out.getvalue())


class LibraryGuardIsCanonical(unittest.TestCase):
    """P-R13 — the guard matches the file, not the spelling."""

    def _guard(self, path):
        payload = {"tool_name": "Write", "tool_input": {"file_path": path}}
        with patch.object(sys, "stdin", io.StringIO(json.dumps(payload))), \
                contextlib.redirect_stderr(io.StringIO()):
            try:
                return runpy.run_path(str(WRITE_GUARD))["main"]()
            except SystemExit as error:
                return error.code

    def test_every_spelling_of_library_blocks(self):
        for path in ("library/kernel/states.md", "./library/kernel/states.md",
                     "projects/../library/kernel/states.md",
                     str(ROOT / "library" / "kernel" / "states.md")):
            self.assertEqual(self._guard(path), 2, path)

    @unittest.skipUnless(os.name == "nt", "case-insensitive filesystem required")
    def test_case_variants_block_on_windows(self):
        for path in ("LIBRARY/kernel/states.md", "Library/Kernel/States.md",
                     str(ROOT / "LIBRARY" / "kernel" / "states.md")):
            self.assertEqual(self._guard(path), 2, path)

    def test_everything_else_passes(self):
        for path in ("projects/p/shared-understanding.md", "docs/x.md",
                     ".claude/hooks/pre-write-guard.py", "librarian/notes.md"):
            self.assertEqual(self._guard(path), 0, path)


if __name__ == "__main__":
    unittest.main(verbosity=2)
