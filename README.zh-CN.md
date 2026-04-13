# Headline Skill 中文说明

[English README](./README.md)

`headline_skill` 是一套可复用的标题工作流。它不是帮你临时起几个标题的 prompt，而是把起标题这件事拆成固定流程、可替换配置和可插拔评分器，方便你自己用，也方便别人按自己的场景接入。

## 这个项目想解决什么

很多 AI 写出来的标题不差，但也不想点。问题通常不在语法，而在表达方式太老实。它太快把中心思想说完了，于是标题变成了摘要、总结，或者教程目录。

这个项目的出发点很简单：好标题往往不是先把重点讲清，而是先把情绪钩子、冲突、代价、反差或者场景放出来。真正的中心思想，可以藏一点，留给读者在点开后自己补全。

## 它是怎么组织的

整个仓库分三层。

第一层是固定流程。负责读 brief、拆内容、挑路线、出候选、做过滤、做评审、给出首选和备选。这一层尽量不跟着个人偏好乱改。

第二层是 profile。这里放平台规则、受众画像、语气约束、禁词、好坏样本和评分权重。换句话说，真正和你业务绑定的东西，都放在这一层。

第三层是 scorer。仓库里已经带了硬过滤和节奏评分。你如果有自己的脚本，也可以按统一返回格式接进来，不用重写整条流程。

## 为什么它不是一个大 prompt

很多标题系统喜欢把一长串要求直接塞进 prompt。这样短期看方便，长期几乎一定会出三个问题。

- 约束一多，模型就开始求稳，越写越像总结
- 换个平台、换业务、换受众，就得重新改 prompt
- 团队里的经验很难沉淀，最后只能靠人记住

这个项目反过来处理：

- 方法写进流程
- 审美写进 profile
- 规则写进脚本

这样别人在接入时，主要改的是自己的风格和场景，不是把底层逻辑重做一遍。

## 仓库里已经有什么

- `SKILL.md`
  - Codex Skill 主入口，定义什么时候触发、按什么流程工作
- `profiles/`
  - 现在带了两个示例
  - `default_xiaohongshu.yaml`
  - `example_bilibili.yaml`
- `references/`
  - 放通用方法、profile schema 和 review rubric
- `scripts/`
  - `hard_filter.py`
  - `rhythm_scorer.py`
  - `evaluate_candidates.py`
  - `validate_skill.py`
- `tests/`
  - 33 条 golden set
  - 一组单元测试
- `.github/workflows/headline-skill-ci.yml`
  - GitHub Actions 自动校验

## 适合什么人

如果你符合下面任一类，这个仓库基本就有用：

- 你在做小红书、B 站、公众号、视频号、课程页之类的内容标题
- 你想把团队里的标题经验沉淀下来，而不是散落在聊天记录和 prompt 里
- 你想开源一套标题方法，但不想把自己的审美写死
- 你想让别人只换 profile 就能用上同一套流程

## 怎么开始用

先装依赖：

```bash
python -m pip install -r requirements.txt
```

然后先检查仓库结构有没有问题：

```bash
python scripts/validate_skill.py .
```

再跑测试，确认本地环境没问题：

```bash
python -m unittest discover -s tests -p "test_*.py"
```

如果你已经有一批候选标题，可以直接走评估链路：

```bash
python scripts/hard_filter.py --profile profiles/default_xiaohongshu.yaml --input candidates.json
python scripts/rhythm_scorer.py --profile profiles/default_xiaohongshu.yaml --input candidates.json
python scripts/evaluate_candidates.py --profile profiles/default_xiaohongshu.yaml --input candidates.json
```

## 如果你要接自己的版本

最省事的接入方式是：

1. 复制一个 profile
2. 改成自己的平台规则和受众画像
3. 填自己的好标题样本和坏标题样本
4. 如果你有额外脚本，就按 scorer contract 接进来
5. 保留现有 workflow、测试和 CI

这样你改的是业务层，不是底层流程。

## 输出结果长什么样

这个项目默认输出的不是一句标题，而是一组结构化结果，方便后续继续做 A/B 测试和人工终审。

- `winner`
- `alternatives`
- `rejected`
- `hook_family`
- `concealment_pattern`
- `hard_filter_result`
- `soft_scores`
- `selection_reason`
- `risk_notes`

## 一句话说完

`headline_skill` 不是一个起标题 prompt，而是一套能迁移、能复用、能让别人接入自己风格的标题工作流。
