**English** | [简体中文](README.md)

<div align="center">

# 🔍 SoSkill

**The "Security-First Search Engine" for AI Agent Skills**

> Auto-aggregate · Risk audit · Ready to use
>
> Solving "Is this Skill safe to install?" from the source

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Stars](https://img.shields.io/github/stars/AIPMAndy/soskill?style=social)](https://github.com/AIPMAndy/soskill)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://python.org)
[![Skill Audit](https://img.shields.io/badge/Security%20Audit-Enabled-success)](docs/skills-audit.md)

</div>

---

## 💡 Why SoSkill

The AI Agent ecosystem has more Skills every day. But can you trust them all?

- Community Skills have **no unified security review**
- Some hide `curl | bash`, `rm -rf`, or credential theft patterns
- Jailbreak / prompt override attacks lurk in long text — hard to spot manually
- Skills are scattered across repos — **hard to even find them all**

**SoSkill = Aggregate + Audit + Output** — one command does it all.

---

## ⚡ 30-Second Quick Start

```bash
git clone https://github.com/AIPMAndy/soskill.git
cd soskill

# One command: fetch + stats + security audit
python3 scripts/run_workflow.py --mode secure-refresh --out-dir data
```

Then check:
- `data/skills.json` — Full aggregated data
- `docs/skills-audit.md` — Security audit report
- `docs/latest.md` — Latest fetch summary

---

## 🛡️ Security Audit (Core Feature)

This is what sets SoSkill apart from a regular "awesome list".

| Detection | Examples |
|-----------|---------|
| 🔴 Dangerous commands | `rm -rf /`, `git reset --hard`, `git clean -fdx` |
| 🔴 Remote execution pipes | `curl \| bash`, `wget \| sh` |
| 🟡 Jailbreak / prompt override | Hidden system prompt overrides |
| 🟡 Credential leakage | Token / secret / password collection patterns |

```bash
make audit          # Fast audit (offline, metadata only)
make audit-deep     # Deep audit (fetches SKILL.md content)
```

**Risk Levels:**

| Level | Action |
|-------|--------|
| `critical` | ⛔ Block immediately, manual review required |
| `high` | 🔒 Quarantine and review |
| `medium` | ⚠️ Review before deployment |
| `low` | 👀 Track and monitor |
| `clean` | ✅ No rules matched (still review for business fit) |

---

## 🆚 vs. Manual Skill Discovery

| Dimension | Manual | SoSkill |
|-----------|--------|---------|
| **Coverage** | Browse repos one by one | Multi-source auto-aggregation |
| **Safety** | Read code by eye | Rule-based scan + severity report |
| **Format** | Different per repo | Unified JSON / CSV / Markdown |
| **Updates** | Check when you remember | GitHub Actions every 6 hours |
| **Go/No-Go** | Gut feeling | Structured audit evidence |

---

## 📊 Current Data Sources

| Source | Type |
|--------|------|
| `openai/skills` | Official (`.curated` + `.system`) |
| `VoltAgent/awesome-openclaw-skills` | Community |
| `AIPMAndy/awesome-openclaw-skills-CN` | Community (Chinese) |

> Configured in `config/sources.json` — easily extensible.

---

## 📦 Output Files

| File | Description |
|------|-------------|
| `data/skills.json` | Full aggregated data |
| `data/skills.csv` | For filtering & analysis |
| `data/skills.audit.json` | Structured audit findings |
| `data/collections.json` | Structured collection data |
| `docs/latest.md` | Latest fetch summary |
| `docs/skills-audit.md` | Human-readable audit report |

---

## 🧩 Install as a Codex Skill

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo AIPMAndy/soskill \
  --path skills/public/soskill
```

Restart Codex after installation.

---

<details>
<summary>🛠 <b>Full Command Reference</b> (click to expand)</summary>

### Makefile Shortcuts

```bash
make refresh          # Full fetch
make audit            # Fast risk audit
make audit-deep       # Deep risk audit
make workflow         # Fetch + stats + audit
make workflow-full    # Fetch + stats + audit + organize
make test             # Run tests
make check-bundle-sync # Check script/bundle sync
```

### Workflow Modes

```bash
python3 scripts/run_workflow.py --mode refresh --out-dir data
python3 scripts/run_workflow.py --mode secure-refresh --out-dir data
python3 scripts/run_workflow.py --mode full --out-dir data
python3 scripts/run_workflow.py --mode offline --out-dir data --skills-input data/skills.json
```

### Advanced Options

```bash
python3 scripts/fetch_skills.py \
  --config config/sources.json \
  --output data/skills.json \
  --csv data/skills.csv \
  --markdown docs/latest.md \
  --min-total 1 \
  --max-retries 2 \
  --retry-delay 1.0 \
  --timeout 30
```

</details>

---

## 📁 Project Structure

```
soskill/
├── skills/public/soskill/    # Installable Codex Skill package
├── config/                   # Source & collection configs
├── scripts/                  # Core scripts (fetch/audit/workflow)
├── tests/                    # Automated tests
├── data/                     # Output data (JSON/CSV)
├── docs/                     # Output docs (audit report/summary)
└── .github/workflows/        # CI + scheduled refresh
```

---

## 🗺️ Roadmap

- [x] Multi-source aggregation + unified schema
- [x] Security audit engine (rule scan + severity levels)
- [x] GitHub Actions auto-refresh
- [x] Codex Skill package
- [ ] More data sources
- [ ] Web UI search interface
- [ ] AI-powered semantic search
- [ ] Skill similarity deduplication

---

## 🤝 Contributing

PRs welcome for new sources, audit rules, and bug fixes. Please open an Issue first.

## 👨‍💻 Author

**AI酋长Andy** — Ex-Tencent/Baidu AI Product Expert · AI Business Strategy Consultant

WeChat `AIPMAndy` · GitHub [@AIPMAndy](https://github.com/AIPMAndy)

## 📄 License

[Apache-2.0](LICENSE)

---

<div align="center">

**Found it useful? Give it a ⭐ Star to help others discover safe Skills**

</div>
