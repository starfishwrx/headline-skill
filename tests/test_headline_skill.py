from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from evaluate_candidates import evaluate  # noqa: E402
from hard_filter import apply_hard_filters, load_structured_file  # noqa: E402
from rhythm_scorer import score_title  # noqa: E402


class HeadlineSkillTests(unittest.TestCase):
    def setUp(self) -> None:
        self.xhs_profile = load_structured_file(ROOT / "profiles" / "default_xiaohongshu.yaml")
        self.bili_profile = load_structured_file(ROOT / "profiles" / "example_bilibili.yaml")

    def test_profiles_load_and_diverge(self) -> None:
        self.assertEqual(self.xhs_profile["profile_name"], "default_xiaohongshu")
        self.assertEqual(self.bili_profile["profile_name"], "example_bilibili")
        self.assertNotEqual(
            self.xhs_profile["platform_rules"]["preferred_length"],
            self.bili_profile["platform_rules"]["preferred_length"],
        )
        self.assertNotEqual(
            [item["name"] for item in self.xhs_profile["hook_families"]],
            [item["name"] for item in self.bili_profile["hook_families"]],
        )

    def test_golden_set_has_portable_briefs(self) -> None:
        golden_path = ROOT / "tests" / "golden_set.jsonl"
        lines = [line for line in golden_path.read_text(encoding="utf-8").splitlines() if line]
        self.assertGreaterEqual(len(lines), 30)
        sample = json.loads(lines[0])
        required = {
            "platform",
            "audience",
            "content_summary",
            "core_points",
            "desired_emotion",
            "hidden_thesis",
            "forbidden_angles",
            "length_range",
            "risk_level",
            "extra_context",
        }
        self.assertTrue(required.issubset(sample["brief"].keys()))

    def test_hard_filter_catches_banned_words_and_duplicates(self) -> None:
        candidates = [
            {"title": "爆款标题干货分享"},
            {"title": "这条内容为什么总有人转发", "hook_family": "curiosity-gap"},
            {"title": "这条内容为什么总有人转发？", "hook_family": "curiosity-gap"},
        ]
        filtered = apply_hard_filters(candidates, self.xhs_profile)
        self.assertFalse(filtered[0]["hard_filter_result"]["passed"])
        self.assertIn("banned-word:干货", filtered[0]["hard_filter_result"]["failures"])
        self.assertFalse(filtered[2]["hard_filter_result"]["passed"])
        self.assertTrue(
            any(
                failure.startswith("duplicate-of:")
                for failure in filtered[2]["hard_filter_result"]["failures"]
            )
        )

    def test_rhythm_scorer_contract(self) -> None:
        result = score_title("很多标题一开始就把答案说完了", self.xhs_profile)
        self.assertEqual(result["score_name"], "rhythm")
        self.assertIsInstance(result["numeric_score"], float)
        self.assertIn("reason", result)
        self.assertIn("pass_fail", result)

    def test_evaluate_returns_structured_output(self) -> None:
        candidates = [
            {
                "title": "真正能打的标题，第一眼往往不讲重点",
                "hook_family": "tension-and-cost",
                "concealment_pattern": "hide-conclusion-show-tension",
                "soft_scores": {
                    "emotional_tension": 88,
                    "concealment": 90,
                    "specificity": 72,
                    "platform_fit": 92,
                    "credibility": 78,
                    "curiosity_gap": 82,
                },
                "selection_reason": "代价感和判断力都在线",
                "risk_notes": [],
            },
            {
                "title": "会写标题的人，通常都没那么急着说明白",
                "hook_family": "identity-mirror",
                "concealment_pattern": "hide-claim-show-observation",
                "soft_scores": {
                    "emotional_tension": 76,
                    "concealment": 86,
                    "specificity": 68,
                    "platform_fit": 88,
                    "credibility": 82,
                    "curiosity_gap": 75,
                },
                "selection_reason": "克制但有拉力",
                "risk_notes": [],
            },
            {
                "title": "爆款标题干货分享",
                "hook_family": "practical-trigger",
                "concealment_pattern": "none",
                "soft_scores": {
                    "emotional_tension": 20,
                    "concealment": 10,
                    "specificity": 20,
                    "platform_fit": 10,
                    "credibility": 20,
                    "curiosity_gap": 10,
                },
                "selection_reason": "故意放一个坏样本",
                "risk_notes": [],
            },
        ]
        output = evaluate(candidates, self.xhs_profile)
        self.assertIsNotNone(output["winner"])
        self.assertGreaterEqual(len(output["alternatives"]), 1)
        self.assertGreaterEqual(len(output["rejected"]), 1)
        self.assertEqual(output["winner"]["title"], "真正能打的标题，第一眼往往不讲重点")
        self.assertIn("hard_filter_result", output["winner"])
        self.assertIn("scorer_results", output["winner"])

    def test_profiles_round_trip_as_yaml(self) -> None:
        for profile_path in ROOT.glob("profiles/*.yaml"):
            with self.subTest(profile=profile_path.name):
                data = yaml.safe_load(profile_path.read_text(encoding="utf-8"))
                with tempfile.NamedTemporaryFile(
                    "w", suffix=".yaml", encoding="utf-8", delete=False
                ) as handle:
                    yaml.safe_dump(data, handle, allow_unicode=True, sort_keys=False)
                    temp_path = handle.name
                reloaded = load_structured_file(temp_path)
                Path(temp_path).unlink(missing_ok=True)
                self.assertEqual(data["profile_name"], reloaded["profile_name"])


if __name__ == "__main__":
    unittest.main()
