<script setup lang="ts">
import FileInput from './components/FileInput.vue'
import { verifyBadge } from './utils/verifyBadge'
import { ref } from 'vue'

// const publicKey = "033cf979c65b903c05c386ee2b0fc732a2b53fda9759caf94e737d17ed28b63461";
const publicKeyPem = `-----BEGIN PUBLIC KEY-----
MCowBQYDK2VwAyEAqihA2xS+pIA/DGAqu0lPEPcf8Nv7Zzmhj8freVkLyu0=
-----END PUBLIC KEY-----`;

const verificationResult = ref<boolean | null>(null);
const badgeInfo = ref<any>(null);
const errorMessage = ref<string>('');

async function processJsonFile(file: File) {
  try {
    const text = await file.text();
    const data = JSON.parse(text);
    console.log('data', data)

    const isValid = await verifyBadge(data.badge, data.signature, data.algorithm, publicKeyPem);
    console.log(isValid)

    verificationResult.value = isValid;
    badgeInfo.value = data.badge;
    errorMessage.value = '';
  } catch (error) {
    console.error('Error processing file:', error);
    errorMessage.value = '文件处理错误，请确保选择的是有效的徽章文件';
    verificationResult.value = null;
    badgeInfo.value = null;
  }
}
</script>

<template>
  <div class="app-container">
    <header>
      <h1>验收你的网协徽章！</h1>
      <p>请选择一个 .json 文件来验证你的徽章</p>
    </header>

    <main>
      <FileInput @file-selected="processJsonFile" />

      <!-- 错误信息显示 -->
      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>

      <!-- 验证结果显示 -->
      <div v-if="verificationResult !== null" class="verification-result">
        <div v-if="verificationResult" class="success-message">
          <h2>✅ 验证通过！</h2>
          <p>此徽章真实有效</p>
        </div>
        <div v-else class="error-message">
          <h2>❌ 验证失败！</h2>
          <p>徽章可能是假的或者已被篡改</p>
          <p>请联系徽章发放者进行核实</p>
        </div>

        <!-- 徽章信息展示 -->
        <div v-if="badgeInfo" :class="['badge-info', { 'invalid': !verificationResult }]">
          <div class="badge-layout">
            <!-- 左列：徽章图片和标题 -->
            <div class="badge-left-column">
              <div class="badge-image">
                <span class="badge-emoji">🏅</span>
              </div>
              <h2 class="badge-title">{{ badgeInfo.badge_title }}</h2>
              <p class="badge-type">{{ badgeInfo.badge_type }}</p>
            </div>
            
            <!-- 右列：详细信息 -->
            <div class="badge-right-column">
              <div class="detail-section">
                <!-- <h3>基本信息</h3> -->
                <div class="info-grid">
                  <span class="label">持有人</span>
                  <span class="value">{{ badgeInfo.member_name }}</span>
                  <span class="label">学号</span>
                  <span class="value">{{ badgeInfo.member_student_id || '未设置' }}</span>
                  <span class="label">角色</span>
                  <span class="value">{{ badgeInfo.member_role }}</span>
                  <span class="label">社团</span>
                  <span class="value">{{ badgeInfo.club_name }}</span>
                  <span class="label">社团ID</span>
                  <span class="value">{{ badgeInfo.club_id }}</span>
                </div>
              
                <div class="info-grid">
                  <span class="label">颁发年份</span>
                  <span class="value">{{ badgeInfo.badge_year }}</span>
                  <span class="label">颁发时间</span>
                  <span class="value">{{ badgeInfo.issue_time }}</span>
                  <span class="label">描述</span>
                  <span class="value">{{ badgeInfo.badge_description || '无' }}</span>
                  <span class="label">唯一ID</span>
                  <span class="value">{{ badgeInfo.id }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.app-container {
  max-width: 900px;
  margin: 2rem auto;
  padding: 2rem;
  border-radius: 12px;
  background: #f8fafc;
  box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

header {
  text-align: center;
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #e2e8f0;
}

h1 {
  margin: 0;
  font-size: 2.5rem;
  color: #111827;
  font-weight: 700;
}

p {
  margin: 0.5rem 0 0;
  color: #475569;
  font-size: 1.1rem;
}

.verification-result {
  margin-top: 2rem;
  padding: 2rem;
  border-radius: 8px;
  background: #ffffff;
  box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05);
}

.success-message {
  text-align: center;
  color: #10b981;
  margin-bottom: 2rem;
  padding: 1.5rem;
  border-radius: 8px;
  background: #d1fae5;
}

.success-message h2 {
  margin: 0 0 0.5rem;
  font-size: 1.5rem;
}

.error-message {
  text-align: center;
  color: #ef4444;
  margin: 1rem 0 2rem;
  padding: 1.5rem;
  border-radius: 8px;
  background: #fee2e2;
}

.error-message h2 {
  margin: 0 0 0.5rem;
  font-size: 1.5rem;
}

/* 徽章信息样式 */
.badge-info {
  margin-top: 2rem;
}

.badge-layout {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 3rem;
  align-items: start;
}

/* 左列：徽章图片和标题 */
.badge-left-column {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.badge-image {
  width: 200px;
  height: 200px;
  border-radius: 50%;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.5rem;
  box-shadow: 0 8px 24px rgba(99, 102, 241, 0.4);
}

.badge-emoji {
  font-size: 6rem;
}

.badge-title {
  font-size: 2rem;
  color: #111827;
  font-weight: 700;
}

.badge-type {
  margin: 0;
  font-size: 1.4rem;
  color: #64748b;
  font-weight: 500;
}

/* 右列：详细信息 */
.badge-right-column {
  width: 100%;
}

.detail-section {
  background: #f8fafc;
  padding: 1.5rem;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  margin-bottom: 1.5rem;
}

.detail-section h3 {
  margin: 0 0 1.5rem;
  font-size: 1.25rem;
  color: #111827;
  font-weight: 600;
}

.info-grid {
  display: grid;
  grid-template-columns: 1fr 4fr;
  gap: 0.5rem 1rem;
  align-items: center;
}

.label {
  font-size: 1.0rem;
  font-weight: 500;
  color: #64748b;
  text-align: right;
}

.value {
  font-size: 1.0rem;
  color: #111827;
  font-weight: 500;
  text-align: left;
}

.full-width {
  grid-column: 1 / -1;
  margin-bottom: 0.5rem;
}

.full-width.label {
  margin-bottom: 0.25rem;
}

.full-width.value {
  text-align: left;
  width: 100%;
}

/* 无效徽章的样式 */
.badge-info.invalid .value {
  text-decoration: line-through;
  color: #94a3b8;
}

.badge-info.invalid .badge-title,
.badge-info.invalid .badge-type,
.badge-info.invalid h3 {
  color: #94a3b8;
}

.badge-info.invalid .badge-image {
  background: linear-gradient(135deg, #94a3b8, #cbd5e1);
  box-shadow: none;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .app-container {
    max-width: 95%;
    padding: 1.5rem;
  }

  h1 {
    font-size: 2rem;
  }

  .badge-layout {
    grid-template-columns: 1fr;
    gap: 2rem;
  }

  .badge-left-column {
    align-items: center;
  }

  .badge-image {
    width: 150px;
    height: 150px;
  }

  .badge-emoji {
    font-size: 4rem;
  }

  .badge-title {
    font-size: 2rem;
  }

  .info-grid {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }

  .label {
    text-align: left;
  }

  .value {
    text-align: left;
    margin-top: 0.25rem;
  }
}
</style>
