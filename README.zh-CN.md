# Headline Skill 中文说明

[English README](./README.md)

一套给 Codex 用的标题工作流：负责生成、评审、筛选标题，也负责把平台差异、受众差异和风格偏好拆出来，做成可替换的 profile 和 scorer。

## 这个仓库是干什么的

很多 AI 写出来的标题不差，但也不想点。问题通常不在语法，而在表达太老实，太快把中心思想讲完，结果标题就变成了摘要、总结或者教程目录。

这个仓库的目标不是多给几个标题，而是把起标题这件事做成一套能复用的流程。真正稳定的部分放在流程里，真正会因人而异的部分放在 profile 里，能脚本化的判断放进 scorer。

### 核心特性

- 可替换的 Profile
  - 平台规则、用户画像、语气限制、禁词、review tests、样本和评分权重都放在 profile。
- 成套的 Profile 资产
  - 一个 profile 不只是一份 YAML，还可以带 editorial playbook 和 benchmark title 集。
- 结构化评审
  - 候选标题不是随便丢一串出来，而是经过过滤、评分、基准对照和排序。
- 可插拔的 Scorer
  - 仓库内置节奏评分，也支持接自己的脚本。
- 流程可迁移
  - 同一套 workflow 可以服务小红书、B 站，也可以继续扩。
- 可回归测试
  - golden set 和单元测试让你改规则时不靠感觉。

## 安装方式

### 当作 Skill 使用

如果你想直接把它接进 Codex：

```bash
git clone https://github.com/starfishwrx/headline-skill.git ~/.codex/skills/headline-skill
```

### 当作独立仓库使用

如果你只是想跑脚本和改配置：

```bash
git clone https://github.com/starfishwrx/headline-skill.git
cd headline-skill
python -m pip install -r requirements.txt
```

## 怎么用

### 评估一批候选标题

先准备一个带 brief 的 `candidates.json`：

```json
{
  "brief": {
    "platform": "xiaohongshu",
    "audience": "内容创业者",
    "content_summary": "为什么好的标题不能一上来讲中心思想",
    "core_points": [
      "好标题先放情绪钩子",
      "总结腔会削弱点击"
    ],
    "desired_emotion": "被说破",
    "hidden_thesis": "标题应该隐藏中心思想",
    "forbidden_angles": [
      "教学目录感"
    ],
    "length_range": [
      14,
      22
    ],
    "risk_level": "medium",
    "extra_context": "偏方法论",
    "anchor_artifacts": [
      {
        "type": "opening_hook",
        "content": "上来先讲结论的视频，往往最容易被划走",
        "notes": "标题不要重复这句话本身，要往更大的判断上提"
      }
    ]
  },
  "candidates": [
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
        "curiosity_gap": 82
      },
      "selection_reason": "",
      "risk_notes": []
    }
  ]
}
```

然后跑完整评估链路：

```bash
python scripts/hard_filter.py --profile profiles/default_xiaohongshu.yaml --input candidates.json
python scripts/rhythm_scorer.py --profile profiles/default_xiaohongshu.yaml --input candidates.json
python scripts/evaluate_candidates.py --profile profiles/default_xiaohongshu.yaml --input candidates.json
```

### 自定义一个 Profile

复制 `profiles/` 下面任意一个文件，然后改这些部分：

- `platform_rules`
- `audience_model`
- `tone_rules`
- `hook_families`
- `bad_patterns`
- `banned_words`
- `score_weights`
- `review_tests`
- `golden_examples`
- `negative_examples`
- `editorial_playbook`
- `benchmark_titles`

具体字段约定在 `references/profile_schema.md`。

### 接自己的 Scorer

你自己的 scorer 只要返回下面这些字段，就能接进现有流程：

- `title`
- `score_name`
- `numeric_score`
- `pass_fail`
- `reason`

分数保持在 `0-100` 区间，方便和内置评分器合并。

## 内置的两个 Profile

### 小红书

- `profiles/default_xiaohongshu.yaml`
- 更强调情绪钩子、平台语感和反摘要倾向

### B 站

- `profiles/example_bilibili.yaml`
- 更强调讨论感、判断力和信息密度

## 架构怎么设计的

这个仓库走的是 progressive disclosure。主入口 `SKILL.md` 尽量短，只负责流程和调用规则。其他文件按需读取，不把所有说明一次性塞进上下文。

| 文件 | 作用 | 什么时候读 |
| --- | --- | --- |
| `SKILL.md` | 主流程和调用规则 | 每次调用都读 |
| `profiles/*.editorial_playbook.md` | profile 的长文本认知层 | 生成前 |
| `profiles/*.benchmark_titles.txt` | 外部标题基准 | 评审时 |
| `references/framework.md` | 通用标题方法 | 做策略和生成时 |
| `references/profile_schema.md` | profile 约定 | 改配置时 |
| `references/review_rubric.md` | 软评审标准 | 做筛选时 |
| `scripts/hard_filter.py` | 硬过滤 | 评估阶段 |
| `scripts/rhythm_scorer.py` | 节奏评分 | 评估阶段 |
| `scripts/evaluate_candidates.py` | 合并结果并排序 | 评估阶段 |
| `tests/golden_set.jsonl` | 回归样本集 | 测试阶段 |

## 这个项目背后的几个判断

1. 好标题通常不是先解释，而是先制造拉力。
2. 审美应该可配置，流程应该可复用。
3. 能写进脚本的规则，就不要全塞进 prompt。
4. 一个不能回归测试的标题系统，最后大概率会慢慢滑回平庸。

## 校验和测试

先跑结构校验：

```bash
python scripts/validate_skill.py .
```

再跑测试：

```bash
python -m unittest discover -s tests -p "test_*.py"
```

仓库里也自带了 `.github/workflows/headline-skill-ci.yml`，同样这两类检查会在 GitHub Actions 里自动执行。
