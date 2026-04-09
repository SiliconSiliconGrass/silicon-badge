import nacl from 'tweetnacl';
import { Buffer } from 'buffer';

function pemToPublicKeyBytes(pem: string): Uint8Array {
  const base64 = pem
    .replace(/-----BEGIN PUBLIC KEY-----/g, '')
    .replace(/-----END PUBLIC KEY-----/g, '')
    .replace(/\s+/g, '');

  const der = Buffer.from(base64, 'base64');

  // 解析 DER 格式的 Ed25519 公钥
  // 结构: SEQUENCE -> SEQUENCE (算法标识) -> BIT STRING (公钥数据)
  if (der[0] !== 0x30) {
    throw new Error('Invalid PEM format: missing SEQUENCE');
  }

  let offset = 1;
  // 读取 SEQUENCE 长度
  const seqLen = readAsn1Length(der, offset);
  offset += seqLen.bytes;

  if (der[offset] !== 0x30) {
    throw new Error('Invalid PEM format: missing inner SEQUENCE');
  }
  offset += 1;

  // 读取算法标识长度
  const algLen = readAsn1Length(der, offset);
  offset += algLen.bytes + algLen.length;

  if (der[offset] !== 0x03) {
    throw new Error('Invalid PEM format: missing BIT STRING');
  }
  offset += 1;

  // 读取 BIT STRING 长度
  const bitStringLen = readAsn1Length(der, offset);
  offset += bitStringLen.bytes;

  if (der[offset] !== 0x00) {
    throw new Error('Invalid PEM format: expected unused bits byte');
  }
  offset += 1;

  // 提取公钥字节 (Ed25519 公钥长度为 32 字节)
  const publicKeyBytes = der.slice(offset, offset + 32);
  return new Uint8Array(publicKeyBytes);
}

function readAsn1Length(buffer: Buffer, offset: number): { length: number; bytes: number } {
  const first = buffer[offset];
  if (first < 0x80) {
    return { length: first, bytes: 1 };
  }
  const size = first & 0x7f;
  let length = 0;
  for (let i = 0; i < size; i++) {
    length = (length << 8) + buffer[offset + 1 + i];
  }
  return { length, bytes: 1 + size };
}

export async function verifyBadge(badgeData: any, signature: string, algorithm: string, publicKeyPem: string): Promise<boolean> {
  if (algorithm !== 'Ed25519') {
    return false;
  }

  try {
    // 递归排序对象键
    function sortObject(obj: any): any {
      if (obj === null || typeof obj !== 'object') return obj;
      if (Array.isArray(obj)) return obj.map(sortObject);
      const sorted: any = {};
      Object.keys(obj).sort().forEach(key => {
        sorted[key] = sortObject(obj[key]);
      });
      return sorted;
    }

    const normalizedData = sortObject(badgeData);
    // 与 Python 的 json.dumps(data, sort_keys=True, separators=(',', ':'), ensure_ascii=False) 完全一致
    // 使用自定义序列化函数确保格式一致
    function serialize(obj: any): string {
      if (obj === null) return 'null';
      if (typeof obj === 'boolean') return obj.toString();
      if (typeof obj === 'number') return obj.toString();
      if (typeof obj === 'string') return '"' + obj.replace(/"/g, '\\"').replace(/\\/g, '\\\\').replace(/\n/g, '\\n').replace(/\r/g, '\\r').replace(/\t/g, '\\t') + '"';
      if (Array.isArray(obj)) return '[' + obj.map(serialize).join(',') + ']';
      if (typeof obj === 'object') {
        const keys = Object.keys(obj).sort();
        return '{' + keys.map(key => '"' + key + '":' + serialize(obj[key])).join(',') + '}';
      }
      return '';
    }
    const jsonStr = serialize(normalizedData);
    
    // 实际使用正确的序列化方式
    const jsonBytes = new TextEncoder().encode(jsonStr);
    
    // 解码公钥
    const publicKey = pemToPublicKeyBytes(publicKeyPem);
    
    // 解码Base64签名
    const signatureBytes = Buffer.from(signature, 'base64');
    
    // 验证签名
    return nacl.sign.detached.verify(jsonBytes, signatureBytes, publicKey);
  } catch (error) {
    console.error('Signature verification failed:', error);
    return false;
  }
}