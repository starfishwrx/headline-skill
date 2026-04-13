# 通用标题 Skill 介绍

`headline_skill` 是一个可复用、可开源、可配置的标题生成与评审工作流。

它解决的不是 单次起标题，而是把起标题这件事产品化：

- 有固定流程
- 有可替换 profile
- 有可插拔 scorer
- 有可回归测试
- 有 GitHub Actions 持续校验

## 它适合谁

它适合这些场景：

- 做小红书、B站、公众号、视频号等内容标题
- 想把团队里的标题经验沉淀成配置，而不是散落在 prompt 里
- 想开源自己的标题方法，但又不想把个人审美写死
- 想让别人只改 profile 就能接入自己的平台、用户和风格

## 它的核心思路

这个 Skill 把标题系统拆成三层：

### 1. 通用流程层

这一层固定不变，负责：

- 读取 brief
- 抽取卖点、冲突、身份、情绪目标、隐藏中心思想
- 选择不同 hook route
- 生成候选标题
- 做硬规则过滤
- 做软评分和选优

### 2. 配置层

这一层由 profile 驱动，不同团队只需要替换自己的：

- 平台规则
- 用户画像
- 风格约束
- 禁词
- 好标题样本
- 坏标题样本
- 评分权重

### 3. 评分器层

这一层负责确定性检查。当前内置：

- 硬过滤器：长度、禁词、重复度、摘要感、标点
- 节奏评分器：把标题的节奏感转成数值

如果你已经有自己的脚本，也可以按统一 contract 接进来。

## 为什么它不是一个固定 prompt

很多标题系统一开始就做错了方向：把一长串风格要求直接塞进 prompt。

这样的问题是：

- 模型容易回到四平八稳的总结句
- 约束越多，输出越像折中产物
- 一旦换平台、换受众、换业务，就得重写整套 prompt

这个 Skill 的设计就是为了解决这个问题：

- 方法写在 workflow
- 审美写在 profile
- 规则写在脚本

这样别人在接入时，主要改 profile 和样本，不用重写系统。

## 当前默认内置的能力

当前已经包含：

- 一个通用 `SKILL.md`
- 两个示例 profile
  - `default_xiaohongshu.yaml`
  - `example_bilibili.yaml`
- 三份方法与规范文档
- 三个可执行脚本
- 一组 golden set
- 单元测试
- GitHub Actions 工作流

## 它的输出不是一个标题

这个 Skill 默认输出的是结构化结果，而不是只吐一句话：

- `winner`
- `alternatives`
- `rejected`
- `hook_family`
- `concealment_pattern`
- `hard_filter_result`
- `soft_scores`
- `selection_reason`
- `risk_notes`

这样后面你才能继续做：

- A/B 测试
- 复盘
- 人工终审
- scorer 升级
- 多平台扩展

## 最适合的开源方式

如果你准备让别人接入自己的版本，推荐这样用：

1. fork 这个 Skill
2. 复制一个 profile
3. 换成自己的平台约束和审美样本
4. 如有需要，接入自己的 scorer
5. 保留 workflow 和 GitHub Actions

这样他们改的是风格和业务，不是底层流程。

## 一句话总结

`headline_skill` 不是一个标题 prompt，而是一套可迁移的标题生产协议。
