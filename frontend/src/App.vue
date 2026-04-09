<script setup lang="ts">
import FileInput from './components/FileInput.vue'
import { verifyBadge } from './utils/verifyBadge'

// const publicKey = "033cf979c65b903c05c386ee2b0fc732a2b53fda9759caf94e737d17ed28b63461";
const publicKeyPem = `-----BEGIN PUBLIC KEY-----
MCowBQYDK2VwAyEAqihA2xS+pIA/DGAqu0lPEPcf8Nv7Zzmhj8freVkLyu0=
-----END PUBLIC KEY-----`;

async function processJsonFile(file: File) {
  try {
    const text = await file.text();
    const data = JSON.parse(text);
    console.log('data', data)

    const isValid = await verifyBadge(data.badge, data.signature, data.algorithm, publicKeyPem);
    console.log(isValid)

    // TODO: 在UI中显示验证结果
  } catch (error) {
    console.error('Error processing file:', error);
  }
}
</script>

<template>
  <div class="app-container">
    <header>
      <h1>验收你的网协徽章！</h1>
      <p>请选择一个 .json 文件，然后系统会调用一个处理函数。</p>
    </header>

    <main>
      <FileInput @file-selected="processJsonFile" />
    </main>
  </div>
</template>

<style scoped>
.app-container {
  max-width: 500px;
  margin: 2rem auto;
  padding: 1.5rem;
  border-radius: 12px;
  background: #f8fafc;
  box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

header {
  text-align: center;
  margin-bottom: 1.5rem;
}

h1 {
  margin: 0;
  font-size: 1.75rem;
  color: #111827;
}

p {
  margin: 0.5rem 0 0;
  color: #475569;
}
</style>
