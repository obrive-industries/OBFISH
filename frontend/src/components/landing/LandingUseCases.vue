<template>
  <section class="section-usecases" id="use-cases">
    <div class="container">
      <div class="section-header">
        <div class="category-pill">
          <span class="pill-dot"></span>
          INDUSTRY SIMULATION
        </div>

        <h2 class="section-title">
          OBMIND is built to Explore
        </h2>

        <p class="section-sub">
          From a question to a structured exploration of possibilities.
        </p>
      </div>

      <!-- 6 Bento Cards -->
      <div class="bento-grid">
        <div 
          v-for="(card, index) in useCases" 
          :key="card.sector"
          class="bento-card"
          :class="`bento-${index + 1}`"
        >
          <div class="card-glow"></div>
          
          <div class="card-top">
            <span class="sector-badge">{{ card.sector }}</span>
            <span class="bento-icon">{{ card.icon }}</span>
          </div>

          <h3 class="bento-heading">{{ card.subCategory }}</h3>

          <p class="bento-desc">
            {{ card.description }}
          </p>

          <div class="bento-footer">
            <span class="bento-tag">AI Swarm Ready</span>
            <span class="bento-explore-arrow">↗</span>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
const useCases = [
  {
    sector: 'STARTUPS / ENTREPRENEUR',
    subCategory: 'Business Strategy & Decision Intelligence',
    description: 'Test ideas, explore markets, simulate growth, pricing, competition, and business outcomes before investing.',
    icon: '⚡'
  },
  {
    sector: 'BRAND / MARKETING',
    subCategory: 'Marketing & Brand Intelligence',
    description: 'Simulate customer reactions to campaigns, launches, pricing, and messaging to refine brand strategy.',
    icon: '🎯'
  },
  {
    sector: 'ENTERPRISE / PR',
    subCategory: 'Public Opinion & Stakeholder Analysis',
    description: 'Simulate stakeholder reactions to policies, announcements, and changes to identify risks and response patterns.',
    icon: '🛡️'
  },
  {
    sector: 'ENTERTAINMENT / CREATIVE',
    subCategory: 'Story and Fiction Deduction',
    description: 'Build character worlds from novels and scripts, simulate plot developments, relationship dynamics and possible endings.',
    icon: '🎭'
  },
  {
    sector: 'RESEARCH / DEVELOPMENT',
    subCategory: 'Product Development & Market Research',
    description: 'Simulate customer reactions to products, features, pricing, and value propositions to identify what needs real-world validation.',
    icon: '🔬'
  },
  {
    sector: 'FINANCE / INVESTMENT',
    subCategory: 'Financial & Economic Scenarios',
    description: 'Simulate market narratives, stakeholder responses, and economic scenarios to support research and strategic planning.',
    icon: '📊'
  }
]
</script>

<style scoped>
.section-usecases {
  padding: 120px 24px;
  background: #070b0e;
  position: relative;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.container {
  max-width: 1240px;
  margin: 0 auto;
}

.section-header {
  text-align: center;
  max-width: 760px;
  margin: 0 auto 64px;
}

.category-pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 5px 14px;
  background: rgba(7, 65, 57, 0.3);
  border: 1px solid rgba(0, 229, 163, 0.2);
  border-radius: 9999px;
  font-family: 'Space Grotesk', sans-serif;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 1.5px;
  color: #00E5A3;
  margin-bottom: 20px;
}

.pill-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #00E5A3;
}

.section-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: clamp(2.2rem, 4vw, 3.2rem);
  font-weight: 800;
  color: #ffffff;
  margin: 0 0 16px 0;
}

.section-sub {
  font-size: 1.2rem;
  line-height: 1.6;
  color: #94a3b8;
  margin: 0;
}

.bento-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.bento-card {
  position: relative;
  background: rgba(12, 18, 22, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 18px;
  padding: 32px 28px;
  display: flex;
  flex-direction: column;
  backdrop-filter: blur(14px);
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.bento-card:hover {
  border-color: rgba(0, 229, 163, 0.4);
  transform: translateY(-4px);
  box-shadow: 0 16px 35px rgba(0, 0, 0, 0.5), 0 0 25px rgba(0, 229, 163, 0.1);
}

.card-glow {
  position: absolute;
  top: 0;
  right: 0;
  width: 140px;
  height: 140px;
  background: radial-gradient(circle, rgba(0, 229, 163, 0.12) 0%, transparent 70%);
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.bento-card:hover .card-glow {
  opacity: 1;
}

.card-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.sector-badge {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 1.5px;
  color: #00E5A3;
}

.bento-icon {
  font-size: 1.4rem;
}

.bento-heading {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 1.25rem;
  font-weight: 700;
  color: #ffffff;
  margin: 0 0 14px 0;
  line-height: 1.35;
}

.bento-desc {
  font-size: 0.95rem;
  line-height: 1.6;
  color: #94a3b8;
  margin: 0 0 28px 0;
  flex: 1;
}

.bento-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 16px;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
}

.bento-tag {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  color: #64748b;
}

.bento-explore-arrow {
  color: #00E5A3;
  font-size: 0.95rem;
  transition: transform 0.2s ease;
}

.bento-card:hover .bento-explore-arrow {
  transform: translate(2px, -2px);
}

@media (max-width: 1024px) {
  .bento-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .bento-grid {
    grid-template-columns: 1fr;
  }
}
</style>
