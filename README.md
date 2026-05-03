# 🔍 SoSkill

AI Skill 搜索引擎 - 3 秒找到你需要的 OpenClaw Skill

[![Stars](https://img.shields.io/github/stars/AIPMAndy/soskill?style=social)](https://github.com/AIPMAndy/soskill)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)

---

## 快速开始

```bash
# 1. 克隆项目
git clone https://github.com/AIPMAndy/soskill.git && cd soskill

# 2. 搜索 Skill
python3 scripts/recommend_skill.py "飞书日历"

# 3. 安装 Skill
openclaw skills install openclaw/skills --path skills/autogame-17/feishu-calendar
```

---

## 在线演示

👉 **Web UI**（即将上线）：`streamlit run web_ui.py`

---

## 为什么用 SoSkill？

| 特性 | 说明 |
|------|------|
| ⚡ **快** | 3 秒找到需要的 Skill |
| 🎯 **准** | 智能匹配，推荐最相关的 |
| 🔒 **安全** | 自动过滤高风险 Skill |
| 🌐 **全面** | 聚合 2700+ 开源 Skill |

---

## 使用示例

### 中文查询
```bash
python3 scripts/recommend_skill.py "飞书文档" --top-k 3
```

**输出**：
```
🔍 推荐的 Skill:

1. feishu-doc ❓
   📝 ...
   🎯 匹配度: 0.95
   📦 openclaw skills install openclaw/skills --path skills/autogame-17/feishu-doc

2. feishu-doc-reader ❓
   📝 ...
   🎯 匹配度: 0.95
   📦 openclaw skills install openclaw/skills --path skills/snowshadow/feishu-doc-reader
```

### 英文查询
```bash
python3 scripts/recommend_skill.py "github" --top-k 3
```

**输出**：
```
🔍 推荐的 Skill:

1. github ❓
   📝 ...
   🎯 匹配度: 1.00
   📦 openclaw skills install openclaw/skills --path skills/steipete/github
```

---

## 高级用法

### 调整匹配阈值
```bash
python3 scripts/recommend_skill.py "数据分析" --min-score 0.5
```

### JSON 输出（用于脚本集成）
```bash
python3 scripts/recommend_skill.py "PPT" --format json
```

### Web UI（本地运行）
```bash
streamlit run web_ui.py
```

---

## 项目结构

```
soskill/
├── scripts/
│   ├── auto_skill_matcher.py  # 核心匹配引擎
│   ├── recommend_skill.py      # 命令行工具
│   └── fetch_skills.py         # 数据抓取
├── data/
│   └── skills.json             # Skill 数据库（2700+ Skills）
├── web_ui.py                   # Web 界面（Streamlit）
└── README.md
```

---

## 工作原理

1. **数据聚合**：从 GitHub/ClawHub 抓取 Skill 元数据
2. **智能匹配**：基于关键词匹配 + 多维度评分
3. **安全过滤**：自动过滤高风险 Skill
4. **推荐排序**：按相关度排序，返回 Top-K

---

## 贡献指南

欢迎提交 PR！

1. Fork 项目
2. 创建分支：`git checkout -b feature/your-feature`
3. 提交代码：`git commit -m "Add your feature"`
4. 推送分支：`git push origin feature/your-feature`
5. 提交 PR

---

## Star 历史

[![Star History Chart](https://api.star-history.com/svg?repos=AIPMAndy/soskill&type=Date)](https://star-history.com/#AIPMAndy/soskill&Date)

---

## 许可证

Apache 2.0 License - 详见 [LICENSE](LICENSE)

---

## 联系方式

- **作者**：Andy（AI 产品专家）
- **GitHub**：[@AIPMAndy](https://github.com/AIPMAndy)
- **问题反馈**：[Issues](https://github.com/AIPMAndy/soskill/issues)

---

**⭐ 如果觉得有用，请给个 Star！**
