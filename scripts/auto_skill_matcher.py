#!/usr/bin/env python3
"""
自动 Skill 匹配引擎
根据用户需求自动推荐最合适的 Skill，并进行安全审核
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import sys


@dataclass
class SkillMatch:
    """Skill 匹配结果"""
    name: str
    description: str
    source: str
    relevance_score: float
    safety_level: str  # clean, low, medium, high, critical
    install_command: str
    reason: str  # 为什么推荐这个 Skill


class NeedAnalyzer:
    """需求分析器 - 识别用户需求中的关键意图"""
    
    # 关键词映射到 Skill 类别（支持中英文）
    INTENT_KEYWORDS = {
        "数据分析": ["数据", "分析", "统计", "可视化", "图表", "报表", "data", "analysis", "chart", "visualization"],
        "文档处理": ["文档", "PDF", "Word", "Excel", "PPT", "Markdown", "doc", "document", "presentation", "slide"],
        "代码开发": ["代码", "编程", "开发", "调试", "测试", "部署", "code", "coding", "development", "debug", "test"],
        "自动化": ["自动化", "定时", "批量", "脚本", "工作流", "automation", "workflow", "batch", "script"],
        "AI/ML": ["AI", "机器学习", "深度学习", "模型", "训练", "推理", "machine learning", "deep learning", "model"],
        "Web开发": ["网站", "前端", "后端", "API", "服务器", "数据库", "web", "frontend", "backend", "server", "database"],
        "内容创作": ["写作", "文案", "创意", "故事", "博客", "社交媒体", "writing", "content", "blog", "social"],
        "项目管理": ["项目", "任务", "日程", "协作", "团队", "看板", "project", "task", "calendar", "team", "collaboration"],
        "安全审计": ["安全", "审计", "漏洞", "风险", "合规", "security", "audit", "vulnerability", "risk"],
        "飞书集成": ["飞书", "Lark", "Feishu", "日历", "文档", "多维表格", "bitable", "calendar", "feishu"],
    }
    
    # Skill 名称关键词映射（用于直接匹配 Skill 名称）
    SKILL_NAME_KEYWORDS = {
        "feishu": ["飞书", "日历", "文档", "多维表格", "任务"],
        "ppt": ["PPT", "幻灯片", "演示", "presentation"],
        "data": ["数据", "分析", "统计"],
        "coding": ["代码", "编程", "开发"],
        "github": ["GitHub", "代码仓库", "版本控制"],
    }
    
    def analyze(self, user_input: str) -> List[str]:
        """分析用户输入，返回匹配的意图类别"""
        user_input_lower = user_input.lower()
        matched_intents = []
        
        for intent, keywords in self.INTENT_KEYWORDS.items():
            for keyword in keywords:
                if keyword.lower() in user_input_lower:
                    matched_intents.append(intent)
                    break
        
        return list(set(matched_intents))  # 去重


class SkillMatcher:
    """Skill 匹配引擎"""
    
    def __init__(self, skills_path: Path, audit_path: Optional[Path] = None):
        self.skills_path = Path(skills_path)
        self.audit_path = Path(audit_path) if audit_path else None
        self.skills = self._load_skills()
        self.audit_data = self._load_audit() if audit_path else {}
    
    def _load_skills(self) -> List[Dict[str, Any]]:
        """加载 skills.json"""
        if not self.skills_path.exists():
            return []
        
        with open(self.skills_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # 处理新的数据格式：{"skills": [...]}
            if isinstance(data, dict) and 'skills' in data:
                return data['skills']
            # 兼容旧格式：直接是数组
            elif isinstance(data, list):
                return data
            else:
                return []
    
    def _load_audit(self) -> Dict[str, Any]:
        """加载安全审核数据"""
        if not self.audit_path or not self.audit_path.exists():
            return {}
        
        with open(self.audit_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # 转换为 name -> audit_result 的映射
            return {skill['name']: skill for skill in data.get('skills', [])}
    
    def _calculate_relevance(self, skill: Dict[str, Any], intents: List[str], user_input: str) -> float:
        """计算 Skill 与需求的相关度 (0-1) - 极简版，只看 name"""
        score = 0.0
        
        name = skill.get('name', '').lower()
        user_input_lower = user_input.lower()
        
        # 中文关键词映射（按优先级排序）
        keyword_map = {
            '飞书': ['feishu', 'lark'],  # 最高优先级
            '文档': ['doc'],
            '表格': ['sheet', 'bitable'],
            '日历': ['calendar'],
            '任务': ['task'],
            '维基': ['wiki'],
            '云空间': ['drive'],
        }
        
        # 1. 名称完全匹配 → 1.0
        if user_input_lower in name or name in user_input_lower:
            return 1.0
        
        # 2. 中文关键词匹配（累加得分，多个关键词匹配得分更高）
        matched_keywords = 0
        for cn_word, en_words in keyword_map.items():
            if cn_word in user_input_lower:
                # 检查英文关键词是否在 name 中
                for en_word in en_words:
                    if en_word in name:
                        matched_keywords += 1
                        # 飞书相关的权重更高
                        if cn_word == '飞书':
                            score += 0.6
                        else:
                            score += 0.3
                        break
        
        # 3. 英文关键词直接匹配（用户直接输入英文）
        # 提取用户输入中的英文单词（长度 > 2）
        import re
        user_words = re.findall(r'\b[a-z]{3,}\b', user_input_lower)
        for word in user_words:
            if word in name:
                score += 0.5
                matched_keywords += 1
        
        # 如果匹配了多个关键词，额外加分
        if matched_keywords >= 2:
            score += 0.2
        
        # 限制最高分为 0.95（低于完全匹配）
        score = min(score, 0.95)
        
        return score
    
    def _get_safety_level(self, skill_name: str) -> str:
        """获取 Skill 的安全等级"""
        if skill_name not in self.audit_data:
            return "unknown"
        
        audit = self.audit_data[skill_name]
        return audit.get('risk_level', 'unknown')
    
    def _generate_install_command(self, skill: Dict[str, Any]) -> str:
        """生成安装命令"""
        name = skill.get('name', '')
        repo = skill.get('repo', '')
        path = skill.get('path', '')
        html_url = skill.get('html_url', '')
        
        # 如果有完整的 repo 和 path 信息
        if repo and path:
            # 提取 skill 路径（去掉 SKILL.md）
            skill_path = path.replace('/SKILL.md', '')
            return f"openclaw skills install {repo} --path {skill_path}"
        
        # 如果有 html_url
        if html_url and 'github.com' in html_url:
            return f"# 从 GitHub 安装:\n# {html_url}"
        
        # 默认
        return f"# 手动安装 Skill: {name}"
    
    def match(self, user_input: str, top_k: int = 5, min_score: float = 0.3) -> List[SkillMatch]:
        """匹配最合适的 Skill"""
        analyzer = NeedAnalyzer()
        intents = analyzer.analyze(user_input)
        
        # 注释掉这个过滤，允许英文关键词直接匹配
        # if not intents:
        #     return []
        
        # 计算每个 Skill 的相关度
        matches = []
        for skill in self.skills:
            relevance = self._calculate_relevance(skill, intents, user_input)
            
            if relevance < min_score:
                continue
            
            safety_level = self._get_safety_level(skill['name'])
            
            # 过滤掉高风险 Skill
            if safety_level in ['critical', 'high']:
                continue
            
            matches.append(SkillMatch(
                name=skill['name'],
                description=skill.get('description', ''),
                source=skill.get('source', ''),
                relevance_score=relevance,
                safety_level=safety_level,
                install_command=self._generate_install_command(skill),
                reason=f"匹配意图: {', '.join(intents)}"
            ))
        
        # 按相关度排序
        matches.sort(key=lambda x: x.relevance_score, reverse=True)
        
        return matches[:top_k]


def format_output(matches: List[SkillMatch], format: str = "markdown") -> str:
    """格式化输出"""
    if not matches:
        return "未找到匹配的 Skill"
    
    if format == "simple":
        # 极简输出：每个 Skill 只显示 1 行
        output = ["🔍 推荐的 Skill:\n"]
        
        for i, match in enumerate(matches[:3], 1):  # 只显示前 3 个
            safety = {"clean": "✅", "low": "🟢", "medium": "🟡"}.get(match.safety_level, "❓")
            desc_short = match.description[:50] + "..." if len(match.description) > 50 else match.description
            output.append(f"{i}. {match.name} {safety} - {desc_short}")
        
        output.append("\n💡 查看完整列表: 添加 --format markdown")
        return "\n".join(output)
    
    elif format == "markdown":
        output = ["# 推荐的 Skill\n"]
        
        for i, match in enumerate(matches, 1):
            safety_emoji = {
                "clean": "✅",
                "low": "🟢",
                "medium": "🟡",
                "high": "🔴",
                "critical": "⛔",
                "unknown": "❓"
            }.get(match.safety_level, "❓")
            
            output.append(f"## {i}. {match.name} {safety_emoji}")
            output.append(f"**相关度**: {match.relevance_score:.2f}")
            output.append(f"**安全等级**: {match.safety_level}")
            output.append(f"**描述**: {match.description}")
            output.append(f"**推荐理由**: {match.reason}")
            output.append(f"**安装命令**:")
            output.append(f"```bash")
            output.append(match.install_command)
            output.append(f"```")
            output.append("")
        
        return "\n".join(output)
    
    elif format == "json":
        return json.dumps([
            {
                "name": m.name,
                "description": m.description,
                "relevance_score": m.relevance_score,
                "safety_level": m.safety_level,
                "install_command": m.install_command,
                "reason": m.reason
            }
            for m in matches
        ], indent=2, ensure_ascii=False)
    
    else:
        return str(matches)


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="自动 Skill 匹配引擎")
    parser.add_argument("query", help="用户需求描述")
    parser.add_argument("--skills", default="data/skills.json", help="skills.json 路径")
    parser.add_argument("--audit", default="data/skills.audit.json", help="审核数据路径")
    parser.add_argument("--format", choices=["simple", "markdown", "json"], default="simple", help="输出格式")
    parser.add_argument("--top-k", type=int, default=5, help="返回前 K 个结果")
    parser.add_argument("--min-score", type=float, default=0.3, help="最低相关度阈值")
    
    args = parser.parse_args()
    
    # 解析路径
    skills_path = Path(args.skills)
    audit_path = Path(args.audit) if args.audit else None
    
    if not skills_path.exists():
        print(f"错误: skills.json 不存在: {skills_path}", file=sys.stderr)
        sys.exit(1)
    
    # 匹配
    matcher = SkillMatcher(skills_path, audit_path)
    matches = matcher.match(args.query, top_k=args.top_k, min_score=args.min_score)
    
    # 输出
    print(format_output(matches, format=args.format))


if __name__ == "__main__":
    main()
