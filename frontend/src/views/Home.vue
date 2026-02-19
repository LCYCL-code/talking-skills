<template>
  <div class="home-page">

    <!-- Hero 区 -->
    <section class="hero">
      <div class="hero-content">
        <div class="hero-badge">💬 社会化表达训练平台</div>
        <h1 class="hero-title">
          别吵架。<br />
          <span class="hero-highlight">先把话说清楚。</span>
        </h1>
        <p class="hero-sub">
          很多人脑子里有想法，一开口就乱。<br />
          这里，帮你训练「把话说对」这件事。
        </p>
        <div class="hero-actions">
          <router-link to="/hotspots" class="btn btn-primary btn-hero">⚡ 今日开吵，去练嘴</router-link>
          <router-link to="/articles" class="btn btn-ghost btn-hero">📰 读一篇，然后说</router-link>
        </div>
        <p class="hero-note">免费使用 · 登录解锁全部功能</p>
      </div>
      <div class="hero-visual">
        <div class="visual-card vc-1">
          <span class="vc-emoji">🔥</span>
          <span>今日热点 · 去表态</span>
        </div>
        <div class="visual-card vc-2">
          <span class="vc-emoji">💡</span>
          <span>读完一篇，用自己的话说</span>
        </div>
        <div class="visual-card vc-3">
          <span class="vc-emoji">🎤</span>
          <span>上传 PPT，先吵赢自己</span>
        </div>
      </div>
    </section>

    <!-- 三大功能区 -->
    <section class="features">
      <h2 class="section-heading">怎么练？三步走。</h2>
      <div class="features-grid">
        <router-link to="/articles" class="feature-card">
          <div class="feature-icon">📰</div>
          <h3>读懂再说</h3>
          <p>每天精选文章，读完用自己的话总结一遍。不能复述的，叫做「没看懂」。</p>
          <div class="feature-cta">去总结 →</div>
        </router-link>

        <router-link to="/upload" class="feature-card feature-card--highlight">
          <div class="feature-badge">最受欢迎</div>
          <div class="feature-icon">🎤</div>
          <h3>上台前练一遍</h3>
          <p>上传你的 PPT、文档、讲义，用自己的话讲一遍，AI 帮你找逻辑漏洞。</p>
          <div class="feature-cta">开始练习 →</div>
        </router-link>

        <router-link to="/hotspots" class="feature-card">
          <div class="feature-icon">🔥</div>
          <h3>今日开吵</h3>
          <p>对热点事件主动出击，表达观点，和别人吵一吵。沉默的那方，永远输。</p>
          <div class="feature-cta">参战 →</div>
        </router-link>
      </div>
    </section>

    <!-- 价值主张 -->
    <section class="values">
      <div class="values-grid">
        <div class="value-item">
          <div class="value-icon">💥</div>
          <h4>说出来，比想明白更难</h4>
          <p>很多人脑子里清楚，但开口就乱。这里练的，就是「开口」这个高难度动作。</p>
        </div>
        <div class="value-item">
          <div class="value-icon">🧠</div>
          <h4>吵架是最高效的思维训练</h4>
          <p>不是教你撒泼，是训练你有理有据。逻辑清晰的人，争论中永远占优势。</p>
        </div>
        <div class="value-item">
          <div class="value-icon">🚀</div>
          <h4>你的观点，值得被听见</h4>
          <p>不表达，等于不存在。每一次开口，都是你存在感的投票。</p>
        </div>
      </div>
    </section>

    <!-- 适合谁 -->
    <section class="scenarios">
      <h2 class="section-heading">适合你，如果你...</h2>
      <div class="scenarios-grid">
        <div class="scenario-card">
          <span class="scenario-emoji">😶</span>
          <p>开会不敢发言，有想法不知道怎么开口</p>
        </div>
        <div class="scenario-card">
          <span class="scenario-emoji">😵</span>
          <p>汇报总结一堆废话，说完没人记住你说了什么</p>
        </div>
        <div class="scenario-card">
          <span class="scenario-emoji">😤</span>
          <p>看热点事件有想法，但说出来总感觉没底气</p>
        </div>
        <div class="scenario-card">
          <span class="scenario-emoji">🤦</span>
          <p>答辩前临时抱佛脚，逻辑乱成一锅粥</p>
        </div>
      </div>
    </section>

    <!-- 底部 CTA -->
    <section class="cta-section">
      <h2>第一步，就从现在开始。</h2>
      <p>读一篇文章，用自己的话说一遍。<br />别小看这件事，90% 的人做不到。</p>
      <div class="cta-actions">
        <router-link v-if="!user" to="/register" class="btn btn-primary btn-hero">免费注册</router-link>
        <router-link v-else to="/articles" class="btn btn-primary btn-hero">开始今天的练习</router-link>
        <router-link to="/hotspots" class="btn btn-ghost btn-hero">先去吵一架</router-link>
      </div>
    </section>

  </div>
</template>

<script setup>
import { useAuth } from '../composables/useAuth.js'
const { user } = useAuth()
</script>

<style scoped>
.home-page {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 16px 60px;
}

/* ===== Hero ===== */
.hero {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 48px;
  align-items: center;
  padding: 64px 0 48px;
}
.hero-badge {
  display: inline-block;
  font-size: 13px;
  color: var(--primary-light);
  background: rgba(16,185,129,0.1);
  border: 1px solid rgba(16,185,129,0.25);
  padding: 5px 14px;
  border-radius: var(--radius-full);
  margin-bottom: 20px;
}
.hero-title {
  font-size: 46px;
  font-weight: 800;
  line-height: 1.2;
  margin-bottom: 16px;
}
.hero-highlight {
  background: linear-gradient(135deg, var(--primary-light), #06b6d4);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}
.hero-sub {
  font-size: 16px;
  color: var(--text-secondary);
  line-height: 1.8;
  margin-bottom: 28px;
}
.hero-actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 16px;
}
.btn-hero { padding: 12px 24px; font-size: 15px; font-weight: 600; }
.hero-note {
  font-size: 12px;
  color: var(--text-muted);
}

/* Hero 右侧悬浮卡片 */
.hero-visual {
  position: relative;
  height: 300px;
}
.visual-card {
  position: absolute;
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 14px 20px;
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
  font-weight: 500;
  box-shadow: var(--shadow-md);
  white-space: nowrap;
  animation: float 4s ease-in-out infinite;
}
.vc-emoji { font-size: 20px; }
.vc-1 { top: 20px; left: 0; animation-delay: 0s; border-left: 3px solid var(--primary); }
.vc-2 { top: 110px; left: 40px; animation-delay: 1.3s; border-left: 3px solid #06b6d4; }
.vc-3 { top: 200px; left: 10px; animation-delay: 2.6s; border-left: 3px solid #f59e0b; }
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}

/* ===== Features ===== */
.features { padding: 48px 0; }
.section-heading {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 28px;
  text-align: center;
}
.features-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
}
.feature-card {
  display: block;
  text-decoration: none;
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 28px 24px;
  position: relative;
  transition: all var(--transition);
}
.feature-card:hover {
  border-color: var(--border-active);
  transform: translateY(-4px);
  box-shadow: var(--shadow-glow);
}
.feature-card--highlight {
  border-color: rgba(16,185,129,0.3);
  background: rgba(16,185,129,0.04);
}
.feature-badge {
  position: absolute; top: -10px; left: 20px;
  background: var(--primary); color: #fff;
  font-size: 11px; font-weight: 700;
  padding: 3px 10px; border-radius: var(--radius-full);
}
.feature-icon { font-size: 36px; margin-bottom: 14px; }
.feature-card h3 { font-size: 18px; font-weight: 700; margin-bottom: 10px; color: var(--text-primary); }
.feature-card p { font-size: 14px; color: var(--text-secondary); line-height: 1.7; margin-bottom: 16px; }
.feature-cta { font-size: 14px; color: var(--primary-light); font-weight: 600; }

/* ===== Values ===== */
.values { padding: 48px 0; }
.values-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}
.value-item {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 28px 22px;
}
.value-icon { font-size: 32px; margin-bottom: 12px; }
.value-item h4 { font-size: 16px; font-weight: 700; margin-bottom: 8px; }
.value-item p { font-size: 13px; color: var(--text-secondary); line-height: 1.7; }

/* ===== Scenarios ===== */
.scenarios { padding: 48px 0; }
.scenarios-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}
.scenario-card {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 20px 22px;
  display: flex;
  align-items: center;
  gap: 14px;
}
.scenario-emoji { font-size: 28px; flex-shrink: 0; }
.scenario-card p { font-size: 14px; color: var(--text-secondary); line-height: 1.6; margin: 0; }

/* ===== CTA ===== */
.cta-section {
  text-align: center;
  padding: 64px 0 24px;
  border-top: 1px solid var(--border);
}
.cta-section h2 { font-size: 28px; font-weight: 700; margin-bottom: 12px; }
.cta-section p { color: var(--text-secondary); line-height: 1.8; margin-bottom: 28px; }
.cta-actions { display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; }

/* ===== 响应式 ===== */
@media (max-width: 768px) {
  .hero { grid-template-columns: 1fr; }
  .hero-visual { display: none; }
  .hero-title { font-size: 32px; }
  .features-grid, .values-grid { grid-template-columns: 1fr; }
  .scenarios-grid { grid-template-columns: 1fr; }
}
</style>
