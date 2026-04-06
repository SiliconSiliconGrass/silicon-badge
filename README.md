# Silicon Badge

一个基于 ECDSA 签名的社团纪念章生成与验证仓库。项目包含密钥生成、纪念章生成、JSON 签名验证以及一个浏览器端验证 UI 演示页面。

## 主要功能

- `generator/generate_keys.py`：生成 ECDSA 密钥对（secp256k1），输出 `private_key.pem` 和 `public_key.pem`，并生成压缩公钥十六进制文件。
- `generator/generate_badge.py`：读取私钥，生成带签名的纪念章 JSON 文件。
- `generator/verify_badge.py`：使用公钥验证纪念章 JSON 文件中的 ECDSA 签名。
- `frontend/index.html`：社团纪念章验证器页面示例，支持上传 `.json` 纪念章文件并输入 PEM 格式公钥进行演示验证。

## 原理简介

本仓库采用 ECDSA 数字签名保护纪念章数据完整性：

1. 通过 `generate_keys.py` 生成一对 ECDSA 密钥。
2. `generate_badge.py` 将纪念章原始数据规范化为排序后的 JSON 字符串，并对其 SHA-256 哈希进行私钥签名。
3. 纪念章数据与签名一起保存为 JSON 文件。
4. `verify_badge.py` 读取 JSON、重新规范化 badge 数据、计算哈希，并使用公钥验证签名是否有效。

这种方式可以保证：

- 纪念章数据未被篡改；
- 只有持有私钥方才能生成有效纪念章；
- 公钥可公开分享用于验证。

## 目录结构

- `frontend/index.html`：前端验证器页面。
- `generator/generate_keys.py`：生成 ECDSA 密钥对。
- `generator/generate_badge.py`：生成带签名的纪念章 JSON。
- `generator/verify_badge.py`：验证纪念章签名。
- `generator/pyproject.toml`：Python 项目依赖声明。
- `generator/keys/`：生成后的密钥文件目录。
- `generator/badges/`：生成的纪念章 JSON 文件目录。

## 环境要求

- Python 3.12+
- `cryptography` 库

## 安装步骤

```bash
cd generator
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install cryptography
```

如果你不想使用虚拟环境，也可以直接安装：

```bash
python3 -m pip install cryptography
```

## 生成密钥对

```bash
cd generator
python generate_keys.py
```

执行后，会在 `generator/keys/` 目录中生成：

- `private_key.pem`
- `public_key.pem`
- `public_key_hex.txt`

> 请妥善保管私钥 `private_key.pem`，一旦丢失或泄露，将影响纪念章签名安全。

## 生成纪念章

```bash
cd generator
python generate_badge.py
```

脚本会提示输入：

- 成员姓名
- 学号
- 社团名称
- 社团代号
- 纪念章类型
- 纪念章标题
- 描述

生成的纪念章 JSON 文件默认保存到 `generator/badges/` 目录。

## 验证纪念章

使用 Python 脚本验证：

```bash
cd generator
python verify_badge.py badges/<your_badge_file>.json keys/public_key.pem
```

如果签名有效，脚本会输出验证通过和纪念章信息；否则会提示验证失败。

## 浏览器端演示验证

打开 `frontend/index.html`，然后：

1. 将 `generator/keys/public_key.pem` 的内容复制到页面中的公钥输入框。
2. 上传生成的纪念章 JSON 文件。
3. 点击“验证纪念章”查看结果。

> 当前前端页面为演示版本，主要展示验证流程 UI。实际生产环境建议使用 Web Crypto API 或后端签名验证实现完整的 ECDSA 验证。

## 注意事项

- `generate_badge.py` 和 `verify_badge.py` 使用相同的 JSON 规范化方式（`sort_keys=True` 以及最小分隔符），保证签名和验证计算一致。
- 生成的纪念章文件中包含 `badge`、`signature` 和 `algorithm` 字段。
- `test_keys/public_key_hex.txt` 为示例公钥文件，可用于测试和参考。

## 参考

本项目适合作为社团纪念章、荣誉凭证、数字凭证等场景的原型实现。
