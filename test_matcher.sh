#!/bin/bash
# 测试自动 Skill 匹配功能

cd ~/.openclaw/workspace/soskill

echo "=== 测试 1: 飞书日历管理 ==="
python3 scripts/auto_skill_matcher.py "我想自动化飞书日历管理" --top-k 3

echo ""
echo "=== 测试 2: 生成 PPT ==="
python3 scripts/auto_skill_matcher.py "怎么生成 PPT" --top-k 3

echo ""
echo "=== 测试 3: 数据分析 ==="
python3 scripts/auto_skill_matcher.py "有什么数据分析工具" --top-k 5

echo ""
echo "=== 测试 4: 代码开发 ==="
python3 scripts/auto_skill_matcher.py "需要一个代码开发助手" --top-k 3
