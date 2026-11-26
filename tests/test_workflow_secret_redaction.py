#!/usr/bin/env python3
"""Static regression tests for sensitive-value logging in scheduled workflows."""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "daily_analysis.yml"

SENSITIVE_NAMES = (
    "GEMINI_API_KEY",
    "TUSHARE_TOKEN",
    "BOCHA_API_KEYS",
    "TAVILY_API_KEYS",
    "SERPAPI_API_KEYS",
    "OPENAI_API_KEY",
    "WECHAT_WEBHOOK_URL",
    "FEISHU_WEBHOOK_URL",
    "TELEGRAM_BOT_TOKEN",
    "TELEGRAM_CHAT_ID",
    "EMAIL_PASSWORD",
    "CUSTOM_WEBHOOK_URLS",
    "CUSTOM_WEBHOOK_BEARER_TOKEN",
    "FEISHU_APP_SECRET",
    "FEISHU_FOLDER_TOKEN",
    "STOCK_LIST",
)


class ScheduledWorkflowSecretRedactionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.workflow = WORKFLOW.read_text(encoding="utf-8")

    def test_echo_commands_do_not_reference_secrets_or_watchlist(self) -> None:
        echo_lines = [
            line for line in self.workflow.splitlines()
            if re.match(r"^\\s*echo\\b", line)
        ]
        self.assertTrue(echo_lines, "Expected workflow output statements to review")
        for line in echo_lines:
            for name in SENSITIVE_NAMES:
                with self.subTest(line=line.strip(), variable=name):
                    self.assertNotIn(name, line)

    def test_workflow_does_not_enable_shell_xtrace(self) -> None:
        self.assertNotRegex(
            self.workflow,
            r"(?m)^\\s*set\\s+-[^\\n]*x(?:trace)?(?:\\s|$)",
        )
        self.assertNotRegex(
            self.workflow,
            r"(?m)^\\s*set\\s+-o\\s+xtrace\\s*$",
        )

    def test_key_length_and_secret_metadata_are_not_echoed(self) -> None:
        self.assertNotRegex(
            self.workflow,
            r"(?i)(?:key|token|secret|webhook)[^\\n]*(?:length|size)|"
            r"(?:length|size)[^\\n]*(?:key|token|secret|webhook)",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
