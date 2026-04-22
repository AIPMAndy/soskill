# OpenClaw 自动触发集成指南

## 概述

让 soskill 自动识别用户需求并推荐最合适的 Skill，无需手动调用。

## 触发机制

### 1. 对话触发（推荐）

当用户消息包含以下关键词时，自动触发 Skill 推荐：

**触发关键词**：
- "推荐 skill"
- "有什么 skill"
- "需要什么工具"
- "怎么实现"（+ 具体需求）
- "自动化"（+ 具体任务）

**实现方式**：在 `AGENTS.md` 或 `SOUL.md` 中添加规则：

```markdown
## Skill 推荐规则

当用户询问"如何实现 X"或"需要什么工具"时：

1. 先分析需求关键词
2. 调用 soskill 自动匹配引擎
3. 只推荐安全等级为 clean/low 的 Skill
4. 提供安装命令和使用建议

命令：
```bash
cd ~/.openclaw/workspace/soskill
python3 scripts/auto_skill_matcher.py "用户需求" \
  --skills data/skills.json \
  --audit data/skills.audit.json \
  --top-k 3 \
  --format markdown
```
```

### 2. 心跳触发（定期检查）

在 `HEARTBEAT.md` 中添加定期检查：

```markdown
## Skill 生态检查（每周 1 次）

- 检查是否有新的高质量 Skill 发布
- 更新本地 skills.json 数据
- 审核新 Skill 的安全性

命令：
```bash
cd ~/.openclaw/workspace/soskill
python3 scripts/run_workflow.py --mode secure-refresh --out-dir data
```
```

### 3. Cron 定时触发（自动更新）

创建 cron job 自动更新 Skill 数据库：

```bash
# 每天凌晨 2 点更新
openclaw cron add \
  --schedule "0 2 * * *" \
  --command "cd ~/.openclaw/workspace/soskill && python3 scripts/run_workflow.py --mode secure-refresh --out-dir data" \
  --name "soskill-daily-update"
```

## 使用示例

### 场景 1: 用户问"我想自动化飞书日历管理"

**触发流程**：
1. 识别关键词：自动化、飞书、日历
2. 调用匹配引擎：
   ```bash
   python3 scripts/auto_skill_matcher.py "自动化飞书日历管理" --top-k 3
   ```
3. 返回推荐：
   - feishu-calendar ✅
   - feishu-task ✅
   - ai-life-os 🟢

### 场景 2: 用户问"怎么生成 PPT"

**触发流程**：
1. 识别关键词：生成、PPT
2. 调用匹配引擎：
   ```bash
   python3 scripts/auto_skill_matcher.py "生成 PPT" --top-k 3
   ```
3. 返回推荐：
   - ppt-nano-master ✅
   - PPTskill ✅
   - frontend-slides 🟢

### 场景 3: 用户问"有什么数据分析工具"

**触发流程**：
1. 识别关键词：数据分析、工具
2. 调用匹配引擎：
   ```bash
   python3 scripts/auto_skill_matcher.py "数据分析工具" --top-k 5
   ```
3. 返回推荐：
   - data-analysis ✅
   - data-storytelling ✅
   - chart-image ✅

## 安全策略

### 自动过滤规则

1. **阻断高风险 Skill**：
   - `critical` 级别 → 永不推荐
   - `high` 级别 → 永不推荐

2. **警告中风险 Skill**：
   - `medium` 级别 → 推荐但标注 🟡
   - 提示用户手动审核

3. **优先推荐低风险 Skill**：
   - `clean` 级别 → ✅ 优先推荐
   - `low` 级别 → 🟢 可以推荐

### 审核更新策略

- **每天自动审核**：通过 cron 定时运行 `audit_skills.py`
- **新 Skill 强制审核**：首次推荐前必须通过安全审核
- **用户反馈机制**：如果用户报告问题，立即重新审核

## 集成到 AGENTS.md

在 `~/.openclaw/workspace/AGENTS.md` 中添加：

```markdown
## Skill 推荐系统（自动触发）

### 触发条件
当用户询问以下问题时，自动调用 soskill：
- "有什么 skill 可以..."
- "怎么实现..."
- "需要什么工具..."
- "推荐一个..."

### 执行流程
1. 提取用户需求关键词
2. 调用自动匹配引擎：
   ```bash
   cd ~/.openclaw/workspace/soskill
   python3 scripts/auto_skill_matcher.py "用户需求" --top-k 3
   ```
3. 只推荐安全等级为 clean/low 的 Skill
4. 提供安装命令和使用说明

### 安全原则
- 永不推荐 critical/high 风险 Skill
- medium 风险 Skill 需标注警告
- 优先推荐官方和经过审核的 Skill
```

## 高级配置

### 自定义匹配规则

编辑 `scripts/auto_skill_matcher.py` 中的 `INTENT_KEYWORDS`：

```python
INTENT_KEYWORDS = {
    "你的自定义类别": ["关键词1", "关键词2", "关键词3"],
    # ...
}
```

### 调整相关度算法

修改 `_calculate_relevance` 方法中的权重：

```python
# 名称匹配权重 (默认 0.3)
# 描述匹配权重 (默认 0.4)
# 意图匹配权重 (默认 0.3)
```

### 自定义安全策略

修改 `match` 方法中的过滤逻辑：

```python
# 过滤掉高风险 Skill
if safety_level in ['critical', 'high']:
    continue
```

## 监控与日志

### 推荐日志

记录每次推荐的结果：

```bash
# 在 memory/ 目录下创建推荐日志
echo "$(date): 推荐 Skill: $skill_name (相关度: $score)" >> memory/skill-recommendations.log
```

### 性能监控

```bash
# 统计推荐准确率
python3 scripts/analyze_recommendations.py --log memory/skill-recommendations.log
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

## 最佳实践

1. **每天自动更新**：通过 cron 定时更新 skills.json
2. **优先推荐官方 Skill**：OpenAI/Anthropic 官方 Skill 优先级最高
3. **记录用户反馈**：收集用户对推荐的反馈，持续优化
4. **定期审核**：每周重新审核所有 Skill 的安全性
5. **版本控制**：将 skills.json 纳入 git 版本控制

## 扩展方向

- [ ] AI 驱动的语义搜索（使用 embedding）
- [ ] 用户偏好学习（基于历史推荐）
- [ ] Skill 相似度去重
- [ ] 多语言支持（中英文混合搜索）
- [ ] Web UI 搜索界面
