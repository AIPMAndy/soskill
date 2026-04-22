# 🤖 自动 Skill 匹配引擎

> 智能推荐最合适的 OpenClaw Skill，无需手动搜索

## 功能特点

- ✅ **智能意图识别**：自动分析用户需求，识别关键意图
- ✅ **多维度匹配**：结合 Skill 名称、描述、标签进行匹配
- ✅ **安全优先**：自动过滤高风险 Skill，只推荐安全的
- ✅ **中英文支持**：支持中英文混合搜索
- ✅ **相关度排序**：按相关度从高到低排序
- ✅ **一键安装**：提供可直接执行的安装命令

## 快速开始

### 基础用法

```bash
cd ~/.openclaw/workspace/soskill

# 搜索飞书相关 Skill
python3 scripts/auto_skill_matcher.py "我想自动化飞书日历管理"

# 搜索 PPT 生成 Skill
python3 scripts/auto_skill_matcher.py "怎么生成 PPT"

# 搜索数据分析 Skill
python3 scripts/auto_skill_matcher.py "有什么数据分析工具"
```

### 高级用法

```bash
# 返回前 10 个结果
python3 scripts/auto_skill_matcher.py "数据分析" --top-k 10

# 降低相关度阈值（返回更多结果）
python3 scripts/auto_skill_matcher.py "数据分析" --min-score 0.2

# 输出 JSON 格式
python3 scripts/auto_skill_matcher.py "数据分析" --format json

# 指定数据文件路径
python3 scripts/auto_skill_matcher.py "数据分析" \
  --skills data/skills.json \
  --audit data/skills.audit.json
```

## 支持的意图类别

匹配引擎支持以下意图类别（中英文）：

| 类别 | 关键词示例 |
|------|-----------|
| 数据分析 | 数据、分析、统计、可视化、图表、data、analysis |
| 文档处理 | 文档、PDF、Word、Excel、PPT、Markdown |
| 代码开发 | 代码、编程、开发、调试、测试、code、coding |
| 自动化 | 自动化、定时、批量、脚本、automation、workflow |
| AI/ML | AI、机器学习、深度学习、模型、训练 |
| Web开发 | 网站、前端、后端、API、服务器、web、frontend |
| 内容创作 | 写作、文案、创意、故事、博客、writing、content |
| 项目管理 | 项目、任务、日程、协作、团队、project、task |
| 安全审计 | 安全、审计、漏洞、风险、security、audit |
| 飞书集成 | 飞书、Lark、Feishu、日历、文档、bitable |

## 匹配算法

匹配引擎使用多维度评分算法：

1. **Skill 名称直接匹配**（权重 0.5）
   - 检查 Skill 名称是否包含关键词
   - 例如：`feishu-calendar` 匹配 "飞书日历"

2. **名称包含意图关键词**（权重 0.3）
   - 检查 Skill 名称是否包含意图相关词
   - 例如：`data-analysis` 匹配 "数据分析"

3. **描述匹配**（权重 0.4）
   - 计算用户输入与 Skill 描述的关键词重叠度
   - 重叠词越多，得分越高

4. **意图匹配**（权重 0.3）
   - 检查 Skill 描述是否包含意图关键词
   - 支持多意图组合

**最终得分** = min(各项得分之和, 1.0)

## 安全策略

匹配引擎会自动过滤高风险 Skill：

| 风险等级 | 处理方式 |
|---------|---------|
| `critical` | ⛔ 永不推荐 |
| `high` | 🔴 永不推荐 |
| `medium` | 🟡 推荐但标注警告 |
| `low` | 🟢 可以推荐 |
| `clean` | ✅ 优先推荐 |
| `unknown` | ❓ 推荐但标注未审核 |

## 集成到 OpenClaw

### 方式 1：对话触发

在 `AGENTS.md` 中添加规则，当用户询问 Skill 时自动触发：

```markdown
## Skill 推荐系统（自动触发）

当用户询问以下问题时，自动调用 soskill：
- "有什么 skill 可以..."
- "怎么实现..."
- "需要什么工具..."
- "推荐一个..."

执行命令：
```bash
cd ~/.openclaw/workspace/soskill
python3 scripts/auto_skill_matcher.py "用户需求" --top-k 3
```
```

### 方式 2：心跳触发

在 `HEARTBEAT.md` 中添加定期检查：

```markdown
## Skill 生态维护（每周 1 次）

- 检查是否有新的高质量 Skill 发布
- 更新本地 skills.json 数据
- 审核新 Skill 的安全性

命令：
```bash
cd ~/.openclaw/workspace/soskill
python3 scripts/run_workflow.py --mode secure-refresh --out-dir data
```
```

### 方式 3：Cron 定时触发

创建 cron job 自动更新 Skill 数据库：

```bash
openclaw cron add \
  --schedule "0 2 * * *" \
  --command "cd ~/.openclaw/workspace/soskill && python3 scripts/run_workflow.py --mode secure-refresh --out-dir data" \
  --name "soskill-daily-update"
```

## 示例输出

```markdown
# 推荐的 Skill

## 1. feishu-calendar ✅
**相关度**: 0.80
**安全等级**: clean
**描述**: 飞书日历管理工具，支持创建、查询、更新日程
**推荐理由**: 匹配意图: 自动化, 飞书集成
**安装命令**:
```bash
openclaw skills install openclaw/skills --path skills/feishu-calendar
```

## 2. feishu-task 🟢
**相关度**: 0.75
**安全等级**: low
**描述**: 飞书任务管理工具
**推荐理由**: 匹配意图: 自动化, 飞书集成
**安装命令**:
```bash
openclaw skills install openclaw/skills --path skills/feishu-task
```
```

## 自定义配置

### 添加自定义意图

编辑 `scripts/auto_skill_matcher.py`，在 `INTENT_KEYWORDS` 中添加：

```python
INTENT_KEYWORDS = {
    "你的自定义类别": ["关键词1", "关键词2", "关键词3"],
    # ...
}
```

### 调整匹配权重

修改 `_calculate_relevance` 方法中的权重：

```python
# Skill 名称直接匹配（默认 0.5）
score += 0.5

# 名称包含意图关键词（默认 0.3）
score += 0.3

# 描述匹配（默认 0.4）
score += 0.4

# 意图匹配（默认 0.3）
score += 0.3
```

### 自定义安全策略

修改 `match` 方法中的过滤逻辑：

```python
# 过滤掉高风险 Skill
if safety_level in ['critical', 'high']:
    continue
```

## 故障排查

### 问题 1: 没有找到匹配的 Skill

**原因**：
- skills.json 数据过期
- 关键词匹配不准确
- 相关度阈值过高

**解决**：
```bash
# 更新数据
python3 scripts/run_workflow.py --mode refresh --out-dir data

# 降低阈值
python3 scripts/auto_skill_matcher.py "需求" --min-score 0.2
```

### 问题 2: 推荐的 Skill 不相关

**原因**：
- 意图识别不准确
- 需求描述不清晰

**解决**：
- 优化 `INTENT_KEYWORDS` 映射
- 让用户提供更详细的需求描述

### 问题 3: 安全审核数据缺失

**原因**：
- 未运行 audit_skills.py
- audit 数据文件不存在

**解决**：
```bash
# 运行安全审核
python3 scripts/audit_skills.py \
  --input data/skills.json \
  --output data/skills.audit.json
```

## 性能优化

### 缓存机制

匹配引擎会缓存已加载的数据，避免重复读取：

```python
matcher = SkillMatcher(skills_path, audit_path)

# 多次匹配，只加载一次数据
matches1 = matcher.match("需求1")
matches2 = matcher.match("需求2")
matches3 = matcher.match("需求3")
```

### 批量匹配

如果需要批量匹配多个需求，建议复用 matcher 实例：

```python
matcher = SkillMatcher(skills_path, audit_path)

queries = [
    "飞书日历管理",
    "生成 PPT",
    "数据分析",
]

for query in queries:
    matches = matcher.match(query, top_k=3)
    print(format_output(matches))
```

## 贡献指南

欢迎贡献新的意图类别、优化匹配算法、修复 Bug。

### 添加新意图

1. 在 `INTENT_KEYWORDS` 中添加新类别
2. 添加中英文关键词
3. 测试匹配效果
4. 提交 PR

### 优化匹配算法

1. 修改 `_calculate_relevance` 方法
2. 运行测试脚本验证
3. 提交 PR

## License

Apache-2.0

## 作者

**AI酋长Andy** — 前腾讯/百度 AI 产品专家 · AI 商业战略顾问

微信 `AIPMAndy` · GitHub [@AIPMAndy](https://github.com/AIPMAndy)
