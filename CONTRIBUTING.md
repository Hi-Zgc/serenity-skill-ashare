# 贡献指南

欢迎改进 `serenity-skill-ashare`。这个项目更重视研究流程的可验证性，而不是增加更多漂亮但无法核验的结论。

## 适合的贡献

- 改进对 Serenity / `@aleabitoreddit` 公开方法论的边界描述。
- 改进 A 股数据调用路径或失败处理。
- 补充产业链卡点研究流程中的证据标准。
- 优化中文输出结构，让答案更清楚、更少券商报告腔。
- 修复 Windows PowerShell、编码、JSON 文件读取等本地使用问题。
- 增加不联网也能跑的脚本测试或校验。
- 改进候选公司评分因子的解释。

## 不适合的贡献

- 把项目改成荐股或交易信号系统。
- 把 Serenity 的公开发言、持仓或媒体报道写成无需核验的事实。
- 添加无法核验的收益承诺、目标价或确定性判断。
- 引入需要私密账号、cookie、付费数据密钥才能默认运行的路径。
- 把社区传闻或题材归因写成公司事实。
- 大量复制其他项目的 README、工作流或模板文本。

## 本地检查

提交前建议运行：

```bash
python -m py_compile scripts/ashare_fetch_bridge.py scripts/ashare_bottleneck_score.py
python scripts/ashare_bottleneck_score.py --template
python scripts/ashare_fetch_bridge.py --help
python scripts/ashare_bottleneck_score.py --help
```

如果同级目录存在 `a-share-intelligence`，再运行一次轻量数据桥接：

```bash
python scripts/ashare_fetch_bridge.py --source chain --method get_quote --symbol 600519
```

数据接口可能受网络、代理、交易日和上游服务影响。不要把单次失败直接当成代码错误；需要记录来源、方法、错误摘要和是否有兜底来源。

## 修改原则

- `SKILL.md` 保持精简，只放另一个 Agent 必须先知道的规则。
- 细节放入 `references/`，脚本放入 `scripts/`。
- 面向用户和维护者的说明默认使用中文。
- 命令参数、JSON 字段和 `a-share-intelligence` 的方法名保持英文接口，不要为了中文化破坏兼容性。
- 新增数据调用路径时，同步更新 `references/data-router.md`。
- 新增输出规则时，同步更新 `references/output-contract.md`。
- 新增 Serenity 相关背景时，必须标注它是公开资料或二级报道，并保留“非本人项目、非背书、非跟单”的边界。

## Pull Request 建议

PR 说明尽量包含：

- 改了什么。
- 为什么需要改。
- 是否影响数据调用路径。
- 是否影响输出边界或合规提示。
- 跑过哪些本地检查。
