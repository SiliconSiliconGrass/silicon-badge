#!/usr/bin/env python3
"""
测试 Ed25519 加密算法的实现
"""
import json
import os
import sys

def test_ed25519():
    """测试 Ed25519 加密算法的实现"""
    print("🔐 测试 Ed25519 加密算法实现")
    print("=" * 60)
    
    # 1. 生成纪念章
    print("\n1. 生成纪念章...")
    member_info = {
        "name": "测试用户",
        "student_id": "20260001",
        "role": "测试角色",
        "club_name": "测试社团",
        "club_id": "TEST",
        "badge_type": "测试纪念章",
        "badge_title": "测试贡献纪念",
        "description": "这是一个测试纪念章"
    }
    
    try:
        from generate_badge import BadgeGenerator
        generator = BadgeGenerator()
        badge = generator.generate_badge(member_info)
        print("✅ 纪念章生成成功")
        print(f"   算法: {badge['algorithm']}")
        print(f"   签名长度: {len(badge['signature'])} 字符")
        
        # 保存纪念章
        filename = generator.save_badge(badge)
        print(f"   保存到: {filename}")
        
    except Exception as e:
        print(f"❌ 生成纪念章失败: {e}")
        return False
    
    # 2. 验证纪念章
    print("\n2. 验证纪念章...")
    try:
        from verify_badge import verify_badge
        is_valid, badge_info = verify_badge(filename)
        if is_valid:
            print("✅ 验证通过！纪念章真实有效")
        else:
            print("❌ 验证失败！纪念章可能被篡改或签名无效")
            return False
    except Exception as e:
        print(f"❌ 验证纪念章失败: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 所有测试通过！Ed25519 加密算法实现正常")
    return True

if __name__ == "__main__":
    # 添加当前目录到 Python 路径
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    test_ed25519()
