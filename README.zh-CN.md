# Headline Skill 中文说明

[English README](./README.md)

`headline_skill` 是一个可复用、可配置、可开源的标题生成与评审工作流。

它解决的不是一次性起标题，而是把起标题这件事做成一套可迁移的生产协议。你可以把自己的平台规则、受众画像、禁词、样本和评分器接进来，而不用重写整条流程。

## 这个项目在做什么

大多数 AI 标题之所以平，是因为它们太早开始总结。真正有拉力的标题，往往会先藏住中心思想，先放出情绪钩子、冲突、代价、反差或者场景。

这个仓库把这个过程拆成三层：

1. 通用流程层
   - 读取 brief
   - 提取卖点、冲突、身份、情绪目标、隐藏中心思想
   - 选择 4 到 6 条不同的 hook route
   - 生成候选标题
   - 做硬规则过滤
   - 做软评分和选优
2. 配置层
   - 平台规则
   - 用户画像
   - 风格约束
   - 禁词和坏模式
   - 好标题样本和坏标题样本
   - 评分权重
3. 评分器层
   - 内置硬过滤器
   - 内置节奏评分器
   - 支持按统一 contract 接入自定义 scorer

## 为什么它不是一个 prompt

如果把一整份 guideline 全塞进 prompt，模型通常会出现三个问题：

- 输出越来越像总结句
- 约束越多，结果越像折中产物
- 一旦换平台、换受众、换业务，就得重写整套提示词

这个项目的设计是反着来的：

- 方法放在 workflow
- 审美放在 profile
- 规则放在脚本

这样别人接入时，主要改的是 profile 和样本，不是底层流程。

## 仓库里已经包含什么

- `SKILL.md`
  - Codex Skill 主入口，定义触发场景和标准流程
- `profiles/`
  - 两个示例 profile
  - `default_xiaohongshu.yaml`
  - `example_bilibili.yaml`
- `references/`
  - 通用方法、profile schema、review rubric
- `scripts/`
  - `hard_filter.py`
  - `rhythm_scorer.py`
  - `evaluate_candidates.py`
  - `validate_skill.py`
- `tests/`
  - 33 条 golden set
  - 单元测试
- `.github/workflows/headline-skill-ci.yml`
  - GitHub Actions 自动校验

## 最适合谁用

这个仓库适合：

- 做小红书、B 站、公众号、视频号、课程内容标题的人
- 想把团队里的标题经验沉淀成配置的人
- 想开源一套标题方法，但又不想把个人审美写死的人
- 想让别人只改 profile 就能接入自己业务的人

## 快速开始

### 1. 安装依赖

```bash
python -m pip install -r requirements.txt
```

### 2. 校验项目结构

```bash
python scripts/validate_skill.py .
```

### 3. 跑测试

```bash
python -m unittest discover -s tests -p "test_*.py"
```

### 4. 运行标题评估链路

```bash
python scripts/hard_filter.py --profile profiles/default_xiaohongshu.yaml --input candidates.json
python scripts/rhythm_scorer.py --profile profiles/default_xiaohongshu.yaml --input candidates.json
python scripts/evaluate_candidates.py --profile profiles/default_xiaohongshu.yaml --input candidates.json
```

## 如何接入你自己的版本

最推荐的方式是：

1. 复制一个 profile
2. 改成自己的平台规则和用户画像
3. 填自己的好标题样本和坏标题样本
4. 如果你有额外脚本，按 scorer contract 接入
5. 保留 workflow、测试和 CI

这样你改的是风格和业务，而不是底层能力。

## 输出长什么样

这个项目的输出不是一个标题，而是一组结构化结果：

- `winner`
- `alternatives`
- `rejected`
- `hook_family`
- `concealment_pattern`
- `hard_filter_result`
- `soft_scores`
- `selection_reason`
- `risk_notes`

这样后面才方便做：

- A/B 测试
- 人工终审
- scorer 升级
- 多平台扩展
- 复盘与回归测试

## 一句话总结

`headline_skill` 不是一个起标题 prompt，而是一套可迁移的标题生产协议。
