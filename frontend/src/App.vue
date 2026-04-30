<script setup lang="ts">
import FileInput from './components/FileInput.vue'
import { verifyBadge } from './utils/verifyBadge'
import { ref, computed } from 'vue'
import badgeRegistry from './badgeRegistry.json'

// const publicKey = "033cf979c65b903c05c386ee2b0fc732a2b53fda9759caf94e737d17ed28b63461";
const publicKeyPem = `-----BEGIN PUBLIC KEY-----
MCowBQYDK2VwAyEAqihA2xS+pIA/DGAqu0lPEPcf8Nv7Zzmhj8freVkLyu0=
-----END PUBLIC KEY-----`;

const verificationResult = ref<boolean | null>(null);
const badgeInfo = ref<any>(null);
const errorMessage = ref<string>('');
const showUploadSection = ref<boolean>(true);
const showSuccessMessage = ref<boolean>(true);

const badgeMedia = computed(() => {
  if (!badgeInfo.value || !verificationResult.value) {
    return null;
  }
  const badgeTitle = badgeInfo.value.badge_title;
  const registryEntry = badgeRegistry[badgeTitle as keyof typeof badgeRegistry];
  if (!registryEntry) {
    return null;
  }
  return {
    image: registryEntry.image ? `/silicon-badge/badge_data/images/${registryEntry.image}` : null,
    video: registryEntry.video ? `/silicon-badge/badge_data/videos/${registryEntry.video}` : null
  };
});

function toggleUploadSection() {
  showUploadSection.value = !showUploadSection.value;
}

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
    showSuccessMessage.value = true;
    
    if (isValid) {
      showUploadSection.value = false;
      setTimeout(() => {
        showSuccessMessage.value = false;
      }, 2000);
    }
  } catch (error) {
    console.error('Error processing file:', error);
    errorMessage.value = '文件处理错误，请确保选择的是有效的纪念章文件';
    verificationResult.value = null;
    badgeInfo.value = null;
  }
}
</script>

<template>
  <div class="app-container">
    <!-- 展开按钮 - 验证通过后显示 -->
    <button v-if="verificationResult === true && !showUploadSection" 
            @click="toggleUploadSection" 
            class="expand-button">
      <span class="expand-icon">📁</span>
      <span class="expand-text">上传新文件</span>
    </button>

    <!-- 标题和上传区域 - 验证通过时折叠 -->
    <transition name="collapse">
      <div v-show="showUploadSection" class="upload-section">
        <header>
          <h1>验收你的网协纪念章！</h1>
          <p>请选择一个 .json 文件来验证你的纪念章</p>
        </header>

        <FileInput @file-selected="processJsonFile" />

        <!-- 错误信息显示 -->
        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>
      </div>
    </transition>

    <!-- 验证结果显示 -->
    <transition name="fade">
      <div v-if="verificationResult !== null" class="verification-result">
        <!-- 成功时的视频背景 -->
        <div v-if="verificationResult && badgeMedia && badgeMedia.video" class="video-background">
          <video 
            :src="badgeMedia.video" 
            class="background-video"
            autoplay 
            loop 
            muted 
            playsinline
          />
          <!-- <div class="video-overlay"></div> -->
        </div>

        <!-- 内容容器 - 确保在视频之上 -->
        <div class="content-wrapper">
          <!-- 验证成功消息 - 始终渲染，保持占位 -->
          <div v-if="verificationResult" :class="['success-message', { 'fade-out': !showSuccessMessage }]">
            <h2>✅ 验证通过！</h2>
            <p>此纪念章真实有效</p>
          </div>
          
          <!-- 验证失败消息 -->
          <transition name="slide-fade">
            <div v-if="!verificationResult" class="error-message">
              <h2>❌ 验证失败！</h2>
              <p>纪念章可能是假的或者已被篡改</p>
              <p>请联系纪念章发放者进行核实</p>
            </div>
          </transition>
          

          <!-- 纪念章信息展示 -->
          <div v-if="badgeInfo" :class="['badge-info', { 'invalid': !verificationResult }]">
            <div class="badge-layout">
              <!-- 左列：纪念章图片和标题 -->
              <div class="badge-left-column">
                <div class="badge-image">
                  <template v-if="verificationResult && badgeMedia && badgeMedia.image">
                    <img :src="badgeMedia.image" alt="徽章图片" class="badge-img" />
                  </template>
                  <span v-else class="badge-emoji">🏅</span>
                </div>
                <h2 class="badge-title">{{ badgeInfo.badge_title }}</h2>
                <p class="badge-type">{{ badgeInfo.badge_type }}</p>
              </div>
              
              <!-- 右列：详细信息 -->
              <div class="badge-right-column">
                <div class="detail-section">
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
      </div>
    </transition>
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
  position: relative;
  overflow: visible;
}

/* 展开按钮样式 */
.expand-button {
  position: fixed;
  top: 20px;
  right: 20px;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
  transition: all 0.3s ease;
  z-index: 1000;
}

.expand-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(99, 102, 241, 0.5);
}

.expand-button:active {
  transform: translateY(0);
}

.expand-icon {
  font-size: 1.2rem;
}

.expand-text {
  font-size: 0.95rem;
}

/* 上传区域折叠动画 */
.upload-section {
  transition: all 0.5s ease;
}

.collapse-enter-active,
.collapse-leave-active {
  transition: all 0.5s ease;
  overflow: hidden;
}

.collapse-enter-from,
.collapse-leave-to {
  opacity: 0;
  max-height: 0;
  padding-top: 0;
  padding-bottom: 0;
  margin-bottom: 0;
}

.collapse-enter-to,
.collapse-leave-from {
  opacity: 1;
  max-height: 500px;
}

/* 淡入淡出动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 滑动淡出动画 - 用于成功消息 */
.slide-fade-enter-active {
  transition: opacity 0.5s ease-out;
}

.slide-fade-leave-active {
  transition: opacity 0.5s ease-in;
  position: relative;
  pointer-events: none;
}

.slide-fade-enter-from {
  opacity: 0;
}

.slide-fade-leave-to {
  opacity: 0;
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
  position: relative;
  overflow: hidden;
}

/* 内容容器 - 确保在视频之上 */
.content-wrapper {
  position: relative;
  z-index: 10;
}

.success-message {
  text-align: center;
  color: #10b981;
  margin-bottom: 2rem;
  padding: 1.5rem;
  border-radius: 8px;
  background: #d1fae5;
  transition: opacity 0.5s ease;
}

.success-message.fade-out {
  opacity: 0;
  pointer-events: none;
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

/* 纪念章信息样式 */
.badge-info {
  margin-top: 2rem;
}

.badge-layout {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 3rem;
  align-items: start;
}

/* 左列：纪念章图片和标题 */
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

.badge-img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
}

/* 视频背景区域 */
.video-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
  overflow: hidden;
  border-radius: 8px;
}

.background-video {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transform: scale(1.1);
  opacity: 0.8;
}

.video-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.7) 0%,
    rgba(255, 255, 255, 0.65) 50%,
    rgba(255, 255, 255, 0.7) 100%
  );
  z-index: 2;
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

/* 无效纪念章的样式 */
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
