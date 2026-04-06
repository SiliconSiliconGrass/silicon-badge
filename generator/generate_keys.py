"""
生成 ECDSA 密钥对
运行: python generate_keys.py
"""
import os
from pathlib import Path
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend

curr_dir = Path(__file__).parent

def generate_key_pair():
    """生成 ECDSA 密钥对 (secp256k1)"""
    
    # 确保输出目录存在
    os.makedirs("keys", exist_ok=True)
    
    # 生成私钥
    private_key = ec.generate_private_key(
        ec.SECP256K1(),  # 使用 secp256k1 曲线
        default_backend()
    )
    
    # 序列化私钥
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    # 生成公钥
    public_key = private_key.public_key()
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    key_dir = curr_dir / "keys"

    if key_dir.exists():
        answer = input(f"{key_dir.absolute()} 目录已存在！\n继续生成将可能覆盖已生成的密钥对，是否继续？(y/N)")
        if answer.lower() != "y":
            print("❌密钥对生成已取消")
            return


    key_dir.mkdir(exist_ok=True)

    # 保存到文件
    with open(key_dir / "private_key.pem", "wb") as f:
        f.write(private_pem)
    
    with open(key_dir / "public_key.pem", "wb") as f:
        f.write(public_pem)
    
    # 生成公钥的压缩版（用于嵌入HTML）
    compressed_pubkey = public_key.public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.CompressedPoint
    )
    
    with open(key_dir / "public_key_hex.txt", "w") as f:
        f.write(compressed_pubkey.hex())
    
    print("✅ 密钥对生成成功！")
    print(f"   私钥: {(key_dir / "private_key.pem").absolute()} (请妥善保存，切勿泄露！)")
    print(f"   公钥: {(key_dir / "public_key.pem").absolute()}")
    print(f"   公钥(压缩): {(key_dir / "public_key_hex.txt").absolute()}")
    print("\n⚠️  请务必备份 private_key.pem，一旦丢失，所有签发的纪念章将无法验证！")

if __name__ == "__main__":
    generate_key_pair()