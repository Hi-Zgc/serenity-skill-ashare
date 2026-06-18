<div align="center">

# Serenity A 股技能

### 把 Serenity 式供应链卡点研究，改造成可核验的 A 股 Agent Skill

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](LICENSE)
[![Agent Skill](https://img.shields.io/badge/Agent%20Skill-SKILL.md-black)](SKILL.md)
[![A-share Data](https://img.shields.io/badge/Data-a--share--intelligence-red)](references/data-router.md)
[![中文优先](https://img.shields.io/badge/README-%E4%B8%AD%E6%96%87%E4%BC%98%E5%85%88-red)](README.md)

</div>

看到 AI 半导体、CPO、机器人、电力设备、先进封装这些热点，真正难的不是知道“热”，而是判断哪一层真的会卡住、哪些公司只是蹭题材、哪些证据能撑住排序。

`serenity-skill-ashare` 做的就是这件事：把 Serenity / `@aleabitoreddit` 公开讨论中最有价值的“供应链瓶颈”研究方式，改造成 A 股可执行的 Agent Skill。它不靠模型记忆直接给结论，而是通过同级 `a-share-intelligence` 项目拉取行情、K 线、公告、新闻、研报、财务、板块和资金流，再回到公开证据里排序。

> 研究支持，不是荐股系统。这个项目帮 Agent 做产业链拆解、证据核验和优先级排序；最终买卖判断始终由用户自己负责。

## 一句话

```text
先排产业链层级，再排公司。
先找真实扩产约束，再看谁离约束最近。
先核验证据，再谈优先研究名单。
```

## 为什么叫 Serenity A 股技能

Serenity，也就是 X 上的 [`@aleabitoreddit`](https://x.com/aleabitoreddit)，是近年在海外投资社区里走红的匿名 AI/半导体供应链研究者。他受到关注，主要来自一批围绕 AI 光通信、CPO、InP 基板、光子学、小盘科技股的高弹性案例，以及一套非常鲜明的供应链瓶颈研究路径。

公开资料里，他的自我定位接近 AI/半导体供应链分析者。和常见的“先买热门龙头”不同，他更像是在问：

```text
AI 数据中心扩张之后，系统到底哪里先卡住？
这个卡点需要什么材料、设备、工艺或认证？
供应商有几个？扩产要多久？客户能不能绕开？
市场是不是还在用旧业务给它定价？
```

这套路径受到关注，不只是因为个别股票涨幅大，更因为它把投资研究从“主题热度”往“物理瓶颈”推了一层。围绕 AXTI、Sivers Photonics、Raspberry Pi / OpenClaw 等案例，海外和中文媒体都把 Serenity 与“瓶颈理论”“AI 供应链侦探”“小盘科技股重估”联系在一起。

但本项目不神化这个叙事。公开身份和收益记录缺少第三方审计，社交媒体影响力可能放大短期波动，小盘股流动性也可能带来跟风风险。所以这里迁移的是方法，不是持仓；学习的是推理结构，不是喊单。

## 为什么需要 A 股版

海外供应链研究不能直接套进 A 股。A 股有自己的披露、监管和交易噪音：

| 研究问题 | A 股里必须回到哪里 |
| --- | --- |
| 公司是否真在卡点环节 | 年报、半年报、季报、临时公告、互动平台回复 |
| 客户和订单是否真实 | 招投标、中标公告、客户认证、上下游交叉验证 |
| 扩产是否落地 | 环评、能评、项目备案、在建工程、资本开支 |
| 题材是否过热 | 板块强弱、市场宽度、资金流、新闻密度 |
| 财务是否验证叙事 | 应收、存货、合同负债、经营现金流、毛利率 |
| 结论是否过度自信 | 数据缺口、失败来源、反证条件 |

因此这个项目拆成两层：

| 层 | 负责什么 |
| --- | --- |
| 方法层 | Serenity 式产业链拆解：先找系统压力，再找稀缺层级，再排公司 |
| 数据层 | 通过 `a-share-intelligence` 抓取 A 股当前事实，避免凭记忆拼答案 |

## 它能帮你做什么

| 你现在遇到的问题 | 可以这样问 Agent | 本技能会优先检查 |
| --- | --- | --- |
| 热点很多，不知道从哪下手 | `用 Serenity 的方式看 A 股 AI 半导体` | 先排设备、材料、封测、光通信、算力芯片等层级 |
| 担心某只票只是蹭概念 | `挑战一下 600XXX 是不是真 CPO 核心供应商` | 主营、公告、客户、财务和题材暴露是否匹配 |
| 想比较几家公司 | `比较 A/B/C 谁更接近机器人真实瓶颈` | 产业链位置、证据强弱、扩产难度、风险扣分 |
| 想找更上游的卡点 | `光模块之外，A 股 CPO 还该看哪些上游环节` | 基板、激光器、连接、测试、设备和材料 |
| 想建立固定流程 | `带我做一次 A 股产业链卡点研究` | 从需求变化、系统压力、稀缺层级一路问到反证条件 |

## 怎么提问更有效

不要把这个技能当成固定模板。更好的用法是先说清楚你真正想研究的对象、时间窗口和证据要求，让 Agent 按你的问题展开。

可以从下面几块里自由组合：

| 你要指定的东西 | 可以怎么说 |
| --- | --- |
| 主题 | `A 股 AI 半导体`、`机器人执行器`、`CPO 上游材料`、`电力设备出海` |
| 目标 | `找产业链卡点`、`比较候选公司`、`挑战这只股票的逻辑`、`找需要降级的热门方向` |
| 数据要求 | `先查公告和财报`、`补充板块强弱和资金流`、`研报只看元数据`、`列出数据源缺口` |
| 排序方式 | `先排层级再排公司`、`按证据强度排序`、`按证伪风险排序`、`把题材股和真卡点分开` |
| 反方检查 | `什么情况说明这个判断错了`、`哪些证据还不够硬`、`市场可能过度乐观在哪里` |

几个更开放的问法：

```text
我想研究 A 股 [主题]，但不想只看热门票。
请先拆产业链层级，再告诉我哪些环节更可能是真实卡点。
候选公司不用急着给结论，先说明你需要哪些公告、财报、项目或资金数据来验证。
```

```text
我手里有 [公司 A]、[公司 B]、[公司 C]。
请按 Serenity 式方法比较它们：谁更接近真实供应链约束，谁更像题材暴露？
重点写证据缺口和证伪条件。
```

```text
请挑战我对 [股票代码/公司名] 的看法。
不要默认它是核心标的，先判断它在产业链哪一层，再查公开证据是否支持。
如果证据不够，请直接降级。
```

你也可以只给一个很粗的问题，让 Agent 先反问范围：

```text
我想用 Serenity 的方式看 A 股 CPO，但还没想清楚从哪层开始。
你先问我 3 个会影响研究方向的问题。
```

## 方法流

```text
市场叙事
  -> 需求/政策/技术变化
  -> 受压系统
  -> 稀缺层级
  -> A 股候选池
  -> 公告/财报/新闻/研报/行情数据
  -> 优先研究名单
  -> 数据缺口与证伪条件
```

默认输出应该长这样：

```text
先排产业链层级，再排公司。

我会优先看三类：
1. [层级 A]：原因是它更接近真实扩产约束。
2. [层级 B]：原因是供应商少、认证慢。
3. [层级 C]：原因是财务和订单可能先验证。

候选对象：
| 公司 | 位置 | 为什么排这里 | 证据 | 主要缺口 | 证伪点 |

被降级的热门方向：
- [方向 X]：题材热，但目前缺少公告或财务验证。

下一步先查：
1. 最新公告和问询回复。
2. 相关业务收入、毛利率、应收和存货。
3. 客户认证、项目备案或招投标证据。
```

## 数据接入

本项目自身只依赖 Python 标准库。实时数据能力来自同级目录下的 `a-share-intelligence`：

```text
GitHubProjects/
├── a-share-intelligence/
└── serenity-skill-ashare/
```

单次行情：

```bash
python scripts/ashare_fetch_bridge.py --source chain --method get_quote --symbol 600519
```

K 线：

```bash
python scripts/ashare_fetch_bridge.py --source chain --method get_kline --symbol 600519 --kw limit=60
```

公告：

```bash
python scripts/ashare_fetch_bridge.py --source chain --method get_announcements --symbol 600519 --kw limit=20
```

如果数据项目不在同级目录：

```bash
python scripts/ashare_fetch_bridge.py --project F:\Projects\GitHubProjects\a-share-intelligence --source chain --method get_quote --symbol 600519
```

## 本地卡点评分

生成模板：

```bash
python scripts/ashare_bottleneck_score.py --template > candidate.json
```

输出 Markdown 评分：

```bash
python scripts/ashare_bottleneck_score.py candidate.json --format md
```

评分只帮助统一比较口径，不替代证据核验。

## 快速验证

```bash
python -m py_compile scripts/ashare_fetch_bridge.py scripts/ashare_bottleneck_score.py
python scripts/ashare_bottleneck_score.py --template
python scripts/ashare_fetch_bridge.py --help
```

如果同级目录存在 `a-share-intelligence`，再跑：

```bash
python scripts/ashare_fetch_bridge.py --source chain --method get_quote --symbol 600519
```

## 仓库结构

```text
serenity-skill-ashare/
├── SKILL.md
├── README.md
├── NOTICE
├── references/
│   ├── data-router.md
│   ├── output-contract.md
│   └── research-workflow.md
├── scripts/
│   ├── ashare_bottleneck_score.py
│   └── ashare_fetch_bridge.py
├── agents/
│   └── openai.yaml
└── .github/
    ├── ISSUE_TEMPLATE/
    └── workflows/
```

## 边界

`serenity-skill-ashare` 是独立非官方项目，不代表 Serenity / `@aleabitoreddit`，不复刻持仓，不提供跟单，不把公开账号观点当成事实。

本项目只做公开资料研究支持：

- 不给直接买入或卖出指令。
- 不承诺收益。
- 不使用或请求非公开重大信息。
- 不把资金流、热股原因、社区帖子当成主营业务证明。
- 不编造价格、客户、订单、公告、研报结论或市值。

固定结尾：

```text
以上不构成买卖建议，仅作研究参考。
```

## 公开资料线索

以下资料用于理解 Serenity / `@aleabitoreddit` 的公众叙事和研究风格，不代表本项目认可其中收益、身份或个股判断：

- [X 账号公开简介](https://x.com/aleabitoreddit)：`@aleabitoreddit` 自称 AI/半导体供应链分析者，并提示不构成投资建议。
- [Singularity Research 的方法分析](https://singularityresearchfund.substack.com/p/inside-the-mind-of-serenity-aleabitoreddit)：重点讨论 AXTI、光子学和供应链瓶颈。
- [Futu 对 Serenity 公众叙事的整理](https://news.futunn.com/en/post/73707645/225x-returns-in-2-years-unpacking-serenity-the-mysterious-researcher)：讨论其 Reddit/X 背景、AI 数据中心硬件、硅光和先进封装线索。
- [Foresight News 中文报道](https://foresightnews.pro/article/detail/97459)：梳理中文社区对 Serenity 和高弹性科技股案例的关注。
- [Odaily 英文报道](https://www.odaily.news/en/post/5210924)：同时提到公开研究、媒体引用和身份/业绩未审计风险。
- [PANews 对瓶颈理论的概括](https://www.panewslab.com/en/articles/019e7d30-5a0b-7721-8dfb-ff74096ba255)：把其方法描述为避开大市值显性龙头、寻找供应受限的关键环节。
- [Raspberry Pi / OpenClaw 相关报道](https://www.investments.halifax.co.uk/research-centre/news-centre/article/?id=21722536&type=bsm)：展示公开账号观点如何进入交易叙事，也提醒社交媒体影响力本身可能成为风险变量。

使用这些材料时要区分三件事：方法论可以学习，公开说法需要核验，个股交易结果不能外推。

## License

Apache-2.0。项目灵感和边界说明见 [NOTICE](NOTICE)。
