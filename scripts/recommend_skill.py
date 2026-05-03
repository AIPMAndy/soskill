#!/usr/bin/env python3
"""
SoSkill 推荐引擎 - 极简版
根据用户需求推荐 Skill，支持自动安装
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import List, Dict

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from scripts.auto_skill_matcher import SkillMatcher


def recommend(query: str, top_k: int = 3) -> List[Dict]:
    """
    推荐 Skill
    
    Args:
        query: 用户需求描述
        top_k: 返回前 N 个推荐
    
    Returns:
        推荐结果列表
    """
    # 获取 skills.json 路径
    script_dir = Path(__file__).parent
    skills_path = script_dir.parent / "data" / "skills.json"
    
    if not skills_path.exists():
        print(f"❌ 错误：找不到 {skills_path}")
        return []
    
    matcher = SkillMatcher(skills_path=skills_path)
    matches = matcher.match(query, top_k=top_k)
    
    results = []
    for match in matches:
        results.append({
            "name": match.name,
            "description": match.description,
            "source": match.source,
            "score": match.relevance_score,
            "safety": match.safety_level,
            "install_cmd": match.install_command,
            "reason": match.reason
        })
    
    return results


def format_output(results: List[Dict]) -> str:
    """格式化输出"""
    if not results:
        return "❌ 没有找到匹配的 Skill"
    
    output = "🔍 推荐的 Skill:\n\n"
    for i, skill in enumerate(results, 1):
        safety_icon = {"clean": "✅", "low": "🟢", "medium": "🟡", "high": "🟠", "critical": "🔴"}.get(skill["safety"], "❓")
        output += f"{i}. {skill['name']} {safety_icon}\n"
        output += f"   📝 {skill['description'][:80]}...\n"
        output += f"   🎯 匹配度: {skill['score']:.2f}\n"
        output += f"   💡 {skill['reason']}\n"
        output += f"   📦 {skill['install_cmd']}\n\n"
    
    return output


def install_skill(install_cmd: str) -> bool:
    """
    安装 Skill
    
    Args:
        install_cmd: 安装命令（如 openclaw skills install xxx）
    
    Returns:
        是否安装成功
    """
    try:
        result = subprocess.run(install_cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ 安装失败: {e}", file=sys.stderr)
        return False


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="SoSkill 推荐引擎")
    parser.add_argument("query", help="用户需求描述")
    parser.add_argument("--top-k", type=int, default=3, help="返回前 N 个推荐")
    parser.add_argument("--install", action="store_true", help="自动安装第一个推荐")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    
    args = parser.parse_args()
    
    # 推荐 Skill
    results = recommend(args.query, args.top_k)
    
    # 输出结果
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print(format_output(results))
    
    # 自动安装
    if args.install and results:
        best_match = results[0]
        print(f"\n🔧 正在安装: {best_match['name']}...")
        if install_skill(best_match["install_cmd"]):
            print(f"✅ 安装成功: {best_match['name']}")
        else:
            print(f"❌ 安装失败: {best_match['name']}")


if __name__ == "__main__":
    main()
