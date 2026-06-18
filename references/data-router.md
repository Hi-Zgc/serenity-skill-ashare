# A 股数据路由

抓取当前 A 股事实前，先使用本文件确定调用路径。

## 网关

所有实时 A 股来源调用都通过：

```bash
python scripts/ashare_fetch_bridge.py --source <source> --method <method> [--symbol 600519] [--kwargs '{"limit": 20}']
```

桥接脚本会转调同级项目：

```text
../a-share-intelligence/scripts/a_share_fetch.py
```

如果 `a-share-intelligence` 不在同级目录，显式传入路径：

```bash
python scripts/ashare_fetch_bridge.py --project F:\Projects\GitHubProjects\a-share-intelligence --source chain --method get_quote --symbol 600519
```

在 Windows PowerShell 中，简单参数优先用可重复的 `--kw key=value`，批量任务优先用 `--calls-file`：

```bash
python scripts/ashare_fetch_bridge.py --source chain --method get_kline --symbol 600519 --kw limit=60
python scripts/ashare_fetch_bridge.py --calls-file calls.json
```

## 默认来源选择

普通检索优先用 `chain`。关键字段需要核验时，显式调用独立来源交叉比较。

| 需求 | 首选调用 | 交叉核验或兜底 |
| --- | --- | --- |
| 实时行情 | `chain.get_quote` | `tencent.get_quote`, `eastmoney.get_quote` |
| K 线 | `chain.get_kline` | `eastmoney.get_kline`, `sina.get_kline` |
| 基础面 | `chain.get_fundamentals` | `eastmoney.get_fundamentals`, `tencent.get_fundamentals` |
| 利润表 | `chain.get_income_statement` | `eastmoney`, `sina`, 可选 `akshare` |
| 资产负债表 | `chain.get_balance_sheet` | `eastmoney`, `sina`, 可选 `akshare` |
| 现金流量表 | `chain.get_cashflow` | `eastmoney`, `sina`, 可选 `akshare` |
| 个股新闻 | `chain.get_news` | `eastmoney.get_news`, `sina.get_news` |
| 市场新闻 | `chain.get_global_news` | `eastmoney.get_global_news`, `cls.get_global_news` |
| 官方公告 | `chain.get_announcements` | `cninfo.get_announcements` |
| 研报元数据 | `chain.get_research_reports` | `eastmoney.get_research_reports` |
| 题材暴露 | `chain.fetch_theme_exposure` | `baidu`, `eastmoney` |
| 市场指数 | `chain.get_market_indices` | `eastmoney`, `tencent`, `sina` |
| 市场宽度 | `chain.get_market_statistics` | `eastmoney`, `sina` |
| 板块强弱 | `chain.get_sector_rankings` | `eastmoney.get_sector_rankings` |
| 北向资金或热股 | `ths.fetch_cross_border_flow`, `ths.fetch_market_heatmap` | 标注日期和缺口 |
| 个股资金流 | `chain.fetch_order_flow_profile` | `eastmoney.fetch_order_flow_profile` |
| 龙虎榜 | `chain.fetch_trading_seat_activity` | `eastmoney.fetch_trading_seat_activity` |
| 解禁 | `chain.fetch_supply_unlock_schedule` | `eastmoney.fetch_supply_unlock_schedule` |
| 同行快照 | `chain.fetch_peer_industry_snapshot` | `eastmoney.fetch_peer_industry_snapshot` |
| 资金流和板块文章 | `eastmoney.search_articles` | 不足 10 条时补市场新闻 |

## 常用数据包

### 单家公司

先准备以下调用列表：

```json
[
  {"source":"chain","method":"get_quote","symbol":"600519"},
  {"source":"tencent","method":"get_quote","symbol":"600519"},
  {"source":"eastmoney","method":"get_quote","symbol":"600519"},
  {"source":"chain","method":"get_kline","symbol":"600519","kwargs":{"limit":60}},
  {"source":"chain","method":"get_fundamentals","symbol":"600519"},
  {"source":"chain","method":"get_income_statement","symbol":"600519","kwargs":{"limit":5}},
  {"source":"chain","method":"get_balance_sheet","symbol":"600519","kwargs":{"limit":5}},
  {"source":"chain","method":"get_cashflow","symbol":"600519","kwargs":{"limit":5}},
  {"source":"chain","method":"get_news","symbol":"600519","kwargs":{"limit":20}},
  {"source":"chain","method":"get_announcements","symbol":"600519","kwargs":{"limit":20}},
  {"source":"chain","method":"get_research_reports","symbol":"600519","kwargs":{"limit":10}},
  {"source":"chain","method":"fetch_theme_exposure","symbol":"600519"},
  {"source":"chain","method":"fetch_order_flow_profile","symbol":"600519","kwargs":{"include_history":true}},
  {"source":"chain","method":"fetch_trading_seat_activity","symbol":"600519","kwargs":{"look_back_days":30}},
  {"source":"chain","method":"fetch_supply_unlock_schedule","symbol":"600519","kwargs":{"forward_days":90}},
  {"source":"chain","method":"fetch_peer_industry_snapshot","symbol":"600519","kwargs":{"top_n":20}}
]
```

保存为 `calls.json`，然后运行 `python scripts/ashare_fetch_bridge.py --calls-file calls.json`。

再补市场环境：

```json
[
  {"source":"chain","method":"get_market_indices"},
  {"source":"chain","method":"get_market_statistics"},
  {"source":"chain","method":"get_sector_rankings","kwargs":{"n":10}},
  {"source":"ths","method":"fetch_cross_border_flow","kwargs":{"include_history":true}},
  {"source":"eastmoney","method":"search_articles","kwargs":{"keyword":"A股 资金流向 板块分析","limit":20}}
]
```

### 主题或板块扫描

从板块和概念数据开始：

```bash
python scripts/ashare_fetch_bridge.py --source eastmoney --method list_concept_boards
python scripts/ashare_fetch_bridge.py --source eastmoney --method list_industry_boards
python scripts/ashare_fetch_bridge.py --source eastmoney --method get_board_stocks --kw board_code=<code>
python scripts/ashare_fetch_bridge.py --source ths --method fetch_market_heatmap
```

用板块成分股建立第一轮候选池，再对最相关公司抓取单股数据包。

## 失败处理

- 同一个失败调用最多重试一次。
- 第二次仍失败时，继续后续任务，并记录 `source.method`、股票代码、错误摘要和返回条数。
- 两个行情来源出现明显分歧时，并列展示，不要强行选一个。
- 资金流、热股原因、概念暴露和社区类数据只作为信号，不作为业务质量证明。
- 如果 `a-share-intelligence` 没有实现某个方法，明确说明缺失方法并改走其他来源；不要假装已经抓到数据。
