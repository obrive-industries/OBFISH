<template>
  <section class="section-usecases" id="use-cases">
    <div class="container">
      <!-- Section Header with Obrive 3-Ball Badge -->
      <div class="section-header">
        <div class="category-pill">
          <RoundedBallIcon :width="14" :height="20" />
          <span class="pill-text font-microgramma">INDUSTRY SIMULATION</span>
        </div>

        <h2 class="section-title font-microgramma">
          BRAIN is Built to Explore
        </h2>

        <p class="section-sub">
          From a question to a structured exploration of possibilities.
        </p>
      </div>

      <!-- 6 Bento Cards styled with Obrive modern curves and borders -->
      <div class="bento-grid">
        <div 
          v-for="(card, index) in useCases" 
          :key="card.sector"
          class="bento-card"
          :class="`bento-card-${index + 1}`"
        >
          <div class="card-corner-accent"></div>
          
          <div class="card-top">
            <span class="sector-badge font-microgramma">{{ card.sector }}</span>
            <span class="bento-icon">{{ card.icon }}</span>
          </div>

          <h3 class="bento-heading font-microgramma">{{ card.subCategory }}</h3>

          <p class="bento-desc">
            {{ card.description }}
          </p>

          <div class="bento-footer">
            <span class="bento-tag font-microgramma">AI Swarm Ready</span>
            <router-link to="/console" class="bento-explore-link">
              <span>Simulate</span>
              <span class="bento-arrow">↗</span>
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import RoundedBallIcon from '../common/RoundedBallIcon.vue'

const useCases = [
  {
    sector: 'START UPS / ENTREPRENEUR',
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
    sector: 'Research / development',
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
  padding: 110px 24px;
  background: #ffffff;
  position: relative;
}

.container {
  max-width: 1240px;
  margin: 0 auto;
}

.section-header {
  text-align: center;
  max-width: 820px;
  margin: 0 auto 60px;
}

.category-pill {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 6px 14px;
  background: rgba(7, 65, 57, 0.06);
  border: 1px solid rgba(7, 65, 57, 0.18);
  border-radius: 9999px;
  margin-bottom: 20px;
}

.pill-text {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: #074139;
}

.section-title {
  font-size: clamp(2.2rem, 3.8vw, 3.2rem);
  font-weight: 700;
  color: #074139;
  margin: 0 0 16px 0;
  letter-spacing: -0.01em;
}

.section-sub {
  font-size: 1.1rem;
  line-height: 1.6;
  color: rgba(7, 65, 57, 0.85);
  margin: 0;
  font-weight: 450;
}

/* Bento Grid */
.bento-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.bento-card {
  background: #ffffff;
  border: 1px solid rgba(7, 65, 57, 0.18);
  border-radius: 18px;
  padding: 32px 28px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  position: relative;
  overflow: hidden;
  box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.03);
  transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
}

.bento-card:hover {
  transform: translateY(-4px);
  border-color: rgba(7, 65, 57, 0.35);
  box-shadow: 0 16px 40px -8px rgba(7, 65, 57, 0.12);
}

.card-corner-accent {
  position: absolute;
  top: 0;
  right: 0;
  width: 120px;
  height: 120px;
  background: radial-gradient(circle at top right, rgba(162, 241, 223, 0.35), transparent 70%);
  pointer-events: none;
}

.card-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.sector-badge {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.08em;
  padding: 5px 10px;
  background: rgba(7, 65, 57, 0.06);
  color: #074139;
  border-radius: 6px;
  border: 1px solid rgba(7, 65, 57, 0.14);
}

.bento-icon {
  font-size: 22px;
}

.bento-heading {
  font-size: 1.18rem;
  font-weight: 700;
  color: #074139;
  margin: 0 0 14px 0;
  line-height: 1.3;
}

.bento-desc {
  font-size: 0.88rem;
  line-height: 1.65;
  color: rgba(7, 65, 57, 0.85);
  margin: 0 0 28px 0;
  flex: 1;
}

.bento-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 18px;
  border-top: 1px solid rgba(7, 65, 57, 0.1);
}

.bento-tag {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.06em;
  color: #074139;
  opacity: 0.75;
}

.bento-explore-link {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #074139;
  text-decoration: none;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  transition: all 0.2s ease;
}

.bento-explore-link:hover {
  color: #0d5c52;
}

.bento-arrow {
  font-size: 13px;
  transition: transform 0.2s ease;
}

.bento-explore-link:hover .bento-arrow {
  transform: translate(2px, -2px);
}

@media (max-width: 1024px) {
  .bento-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 680px) {
  .bento-grid {
    grid-template-columns: 1fr;
  }
}
</style>
