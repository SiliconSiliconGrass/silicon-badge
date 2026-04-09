#!/usr/bin/env python3
"""
验证纪念章签名
运行: python verify_badge.py badge.json
"""

import json
import base64
import hashlib
import sys
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature

def verify_badge(badge_file: str, public_key_path: str = "keys/public_key.pem"):
    """验证纪念章签名"""
    
    # 加载纪念章数据
    with open(badge_file, "r", encoding="utf-8") as f:
        badge_data = json.load(f)
    
    # 分离数据和签名
    badge_info = badge_data["badge"]
    signature_b64 = badge_data["signature"]
    
    # 加载公钥
    with open(public_key_path, "rb") as f:
        public_key = serialization.load_pem_public_key(
            f.read(),
            backend=default_backend()
        )
        
    
    # 规范化JSON字符串（必须与签名时完全一致）
    json_str = json.dumps(badge_info, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
    
    # 计算哈希
    digest = hashlib.sha256(json_str.encode('utf-8')).digest()
    
    # 解码签名
    signature_bytes = base64.b64decode(signature_b64)
    
    # 验证签名
    try:
        public_key.verify(
            signature_bytes,
            digest,
            ec.ECDSA(hashes.SHA256())
        )
        return True, badge_info
    except InvalidSignature:
        return False, badge_info
    except Exception as e:
        return False, badge_info

def display_badge_info(badge_info: dict):
    """美观地显示纪念章信息"""
    print("\n" + "="*50)
    print("🏅 纪念章验证结果")
    print("="*50)
    print(f"持有人: {badge_info['member_name']}")
    print(f"学号: {badge_info['member_student_id'] or '未设置'}")
    print(f"角色: {badge_info['member_role']}")
    print(f"社团: {badge_info['club_name']}")
    print(f"纪念章: {badge_info['badge_title']}")
    print(f"类型: {badge_info['badge_type']}")
    print(f"年份: {badge_info['badge_year']}")
    if badge_info['badge_description']:
        print(f"描述: {badge_info['badge_description']}")
    print(f"颁发时间: {badge_info['issue_time']}")
    print(f"唯一ID: {badge_info['id']}")
    print("="*50)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使用方法: python verify_badge.py <badge_file.json> [public_key.pem]")
        sys.exit(1)
    
    badge_file = sys.argv[1]
    public_key = sys.argv[2] if len(sys.argv) > 2 else "keys/public_key.pem"
    
    try:
        is_valid, badge_info = verify_badge(badge_file, public_key)
        
        if is_valid:
            print("✅ 验证通过！此纪念章真实有效。")
            display_badge_info(badge_info)
        else:
            print("❌ 验证失败！纪念章可能被篡改或签名无效。")
            display_badge_info(badge_info)
            
    except FileNotFoundError as e:
        print(f"❌ 文件未找到: {e}")
    except json.JSONDecodeError:
        print(f"❌ 文件格式错误: {badge_file} 不是有效的JSON文件")
    except Exception as e:
        print(f"❌ 验证过程中发生错误: {e}")