#!/usr/bin/env python3
"""
生成带有签名的纪念章JSON文件
运行: python generate_badge.py
"""

import json
import hashlib
import base64
import uuid
from datetime import datetime
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature

class BadgeGenerator:
    def __init__(self, private_key_path="keys/private_key.pem"):
        """初始化签名器"""
        with open(private_key_path, "rb") as f:
            self.private_key = serialization.load_pem_private_key(
                f.read(),
                password=None,
                backend=default_backend()
            )
    
    def sign_data(self, data: dict) -> str:
        """为数据生成ECDSA签名"""
        
        # 将数据转为规范化JSON字符串（确保空格、排序一致）
        json_str = json.dumps(data, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
        
        # 计算SHA-256哈希
        digest = hashlib.sha256(json_str.encode('utf-8')).digest()
        
        # 使用私钥签名
        signature = self.private_key.sign(
            digest,
            ec.ECDSA(hashes.SHA256())
        )
        
        # 将签名转为Base64字符串
        return base64.b64encode(signature).decode('utf-8')
    
    def generate_badge(self, member_info: dict) -> dict:
        """生成完整的纪念章数据"""
        
        # 基本徽章信息
        badge_data = {
            "version": "1.0",
            "id": str(uuid.uuid4()),  # 唯一ID
            "issue_time": datetime.utcnow().isoformat() + "Z",
            "club_name": member_info.get("club_name", "未命名社团"),
            "club_id": member_info.get("club_id", "CLUB_001"),
            "member_name": member_info["name"],
            "member_student_id": member_info.get("student_id", ""),
            "member_role": member_info.get("role", "成员"),
            "badge_type": member_info.get("badge_type", "普通纪念章"),
            "badge_title": member_info.get("badge_title", "社团纪念章"),
            "badge_description": member_info.get("description", ""),
            "badge_year": datetime.now().year
        }
        
        # 生成签名
        signature = self.sign_data(badge_data)
        
        # 返回完整数据
        return {
            "badge": badge_data,
            "signature": signature,
            "algorithm": "ECDSA-SHA256-secp256k1"
        }
    
    def save_badge(self, badge_data: dict, filename: str = None):
        """保存纪念章到文件"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            member_name = badge_data["badge"]["member_name"]
            filename = f"badges/{member_name}_{timestamp}.json"
        
        os.makedirs("badges", exist_ok=True)
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(badge_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 纪念章已生成: {filename}")
        return filename

def get_member_info():
    """从用户输入获取成员信息"""
    print("\n🎖️  纪念章生成向导")
    print("-" * 30)
    
    info = {}
    info["name"] = input("成员姓名: ").strip()
    info["student_id"] = input("学号(可选): ").strip()
    info["role"] = input("在社团中的角色: ").strip() or "成员"
    info["club_name"] = input("社团名称: ").strip() or "元空间社团"
    info["club_id"] = input("社团代号(如: METASPACE): ").strip() or "METASPACE"
    info["badge_type"] = input("纪念章类型(如: 元老/杰出/活跃): ").strip() or "纪念章"
    info["badge_title"] = input("纪念章标题: ").strip() or "社团贡献纪念"
    info["description"] = input("描述(可选): ").strip()
    
    return info

if __name__ == "__main__":
    import os
    
    # 检查私钥是否存在
    if not os.path.exists("keys/private_key.pem"):
        print("❌ 未找到私钥文件，请先运行 generate_keys.py")
        exit(1)
    
    # 创建生成器
    try:
        generator = BadgeGenerator()
    except Exception as e:
        print(f"❌ 加载私钥失败: {e}")
        exit(1)
    
    # 获取成员信息
    member_info = get_member_info()
    
    # 生成纪念章
    badge = generator.generate_badge(member_info)
    
    # 保存文件
    print(badge)
    filename = generator.save_badge(badge)
    
    print(f"\n🎉 纪念章生成完成！")
    print(f"📁 文件位置: {filename}")
    print(f"🔐 签名算法: {badge['algorithm']}")
    print(f"🆔 唯一标识: {badge['badge']['id']}")
    print(f"\n💡 提示: 你可以将此文件发送给成员，并附上 verify_badge.html 进行验证")