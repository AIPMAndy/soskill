#!/usr/bin/env python3
import sys
sys.path.insert(0, '/Users/andy/.openclaw/workspace/soskill/scripts')

from auto_skill_matcher import SkillMatcher, format_output
from pathlib import Path

# 测试
skills_path = Path('/Users/andy/.openclaw/workspace/soskill/data/skills.json')
audit_path = Path('/Users/andy/.openclaw/workspace/soskill/data/skills.audit.json')

matcher = SkillMatcher(skills_path, audit_path if audit_path.exists() else None)

# 测试 1
print("=== 测试 1: 飞书日历管理 ===")
matches = matcher.match("我想自动化飞书日历管理", top_k=3)
print(format_output(matches, format="markdown"))

print("\n=== 测试 2: 生成 PPT ===")
matches = matcher.match("怎么生成 PPT", top_k=3)
print(format_output(matches, format="markdown"))

print("\n=== 测试 3: 数据分析 ===")
matches = matcher.match("有什么数据分析工具", top_k=3)
print(format_output(matches, format="markdown"))
