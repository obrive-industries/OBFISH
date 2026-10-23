<template>
  <section class="section-faq" id="faq">
    <div class="container">
      <!-- Section Header with Obrive 3-Ball Badge -->
      <div class="section-header">
        <div class="category-pill">
          <RoundedBallIcon :width="14" :height="20" />
          <span class="pill-text font-microgramma">KNOWLEDGE BASE</span>
        </div>

        <h2 class="section-title font-microgramma">
          Frequently Asked Questions
        </h2>

        <p class="section-sub">
          Everything you need to know about predictive scenario modeling and BRAIN intelligence.
        </p>
      </div>

      <!-- FAQ Accordion List -->
      <div class="faq-list">
        <div 
          v-for="(faq, index) in faqs" 
          :key="faq.question"
          class="faq-item"
          :class="{ 'is-open': openIndex === index }"
        >
          <button class="faq-trigger" @click="toggle(index)" :aria-expanded="openIndex === index">
            <span class="faq-q-num font-microgramma">0{{ index + 1 }}</span>
            <span class="faq-question">{{ faq.question }}</span>
            <span class="faq-icon-wrapper">
              <span class="faq-icon">{{ openIndex === index ? '−' : '+' }}</span>
            </span>
          </button>

          <div v-show="openIndex === index" class="faq-content">
            <p class="faq-answer">{{ faq.answer }}</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import RoundedBallIcon from '../common/RoundedBallIcon.vue'

const openIndex = ref(0) // First open by default

const toggle = (idx) => {
  openIndex.value = openIndex.value === idx ? -1 : idx
}

const faqs = [
  {
    question: 'What is BRAIN?',
    answer: 'BRAIN is an advanced AI multi-agent simulation and predictive intelligence platform developed by Obrive Industries. It models complex multi-stakeholder dynamics, market forces, and emergent real-world behaviors to evaluate possible outcomes before critical decisions are executed.'
  },
  {
    question: 'How does BRAIN generate predictions?',
    answer: 'BRAIN uses a 5-stage predictive workflow: knowledge graph ingestion, ontological graph synthesis, autonomous multi-agent simulation swarms, dialectical debate rounds, and structured intelligence reporting. Dynamic digital twin agents interact in a virtual sandbox to surface blind spots, consensus shifts, and second-order effects.'
  },
  {
    question: 'Can BRAIN predict the future with complete accuracy?',
    answer: 'No AI system can guarantee future outcomes with absolute certainty. BRAIN generates rigorous, high-fidelity probabilistic scenario forecasts and risk matrices that challenge assumptions and provide strategic foresight for sound empirical validation.'
  },
  {
    question: 'Who is BRAIN designed for?',
    answer: 'BRAIN empowers enterprise leadership, venture investors, strategic planners, policy makers, product innovators, and researchers who need to stress-test high-stakes decisions and simulate complex human dynamics in a zero-risk virtual environment.'
  },
  {
    question: 'Can I upload custom documents and proprietary data?',
    answer: 'Yes. BRAIN natively accepts dossiers, PDF whitepapers, market research, policy drafts, and internal memos. The ontology engine ingests your source material to configure simulated stakeholder agents with authentic roles, domain expertise, and realistic constraints.'
  },
  {
    question: 'Is BRAIN a replacement for human strategic decision-making?',
    answer: 'No. BRAIN is purpose-built to augment human judgment, not replace it. By stress-testing assumptions and visualizing hidden consequence paths, it gives leaders the clarity and confidence required to make decisive moves.'
  }
]
</script>

<style scoped>
.section-faq {
  padding: 110px 24px;
  background: #ffffff;
  position: relative;
}

.container {
  max-width: 960px;
  margin: 0 auto;
}

.section-header {
  text-align: center;
  margin-bottom: 56px;
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
  font-size: 1.05rem;
  line-height: 1.6;
  color: rgba(7, 65, 57, 0.85);
  margin: 0;
  font-weight: 450;
}

/* FAQ List */
.faq-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.faq-item {
  background: #ffffff;
  border: 1px solid rgba(7, 65, 57, 0.18);
  border-radius: 14px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.02);
  transition: all 0.25s ease;
}

.faq-item:hover {
  border-color: rgba(7, 65, 57, 0.35);
}

.faq-item.is-open {
  border-color: #074139;
  background: #fafcfb;
  box-shadow: 0 6px 20px -2px rgba(7, 65, 57, 0.08);
}

.faq-trigger {
  width: 100%;
  display: flex;
  align-items: center;
  padding: 22px 24px;
  background: transparent;
  border: none;
  cursor: pointer;
  text-align: left;
  gap: 18px;
}

.faq-q-num {
  font-size: 13px;
  font-weight: 700;
  color: #074139;
  opacity: 0.6;
}

.faq-question {
  flex: 1;
  font-size: 1.08rem;
  font-weight: 600;
  color: #074139;
  line-height: 1.4;
}

.faq-icon-wrapper {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: rgba(7, 65, 57, 0.08);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: background 0.2s ease;
}

.faq-item.is-open .faq-icon-wrapper {
  background: #074139;
}

.faq-icon {
  font-size: 16px;
  font-weight: 700;
  color: #074139;
  line-height: 1;
}

.faq-item.is-open .faq-icon {
  color: #caede5;
}

.faq-content {
  padding: 0 24px 24px 54px;
}

.faq-answer {
  font-size: 0.95rem;
  line-height: 1.7;
  color: rgba(7, 65, 57, 0.85);
  margin: 0;
}

@media (max-width: 640px) {
  .faq-trigger {
    padding: 18px 16px;
    gap: 12px;
  }

  .faq-content {
    padding: 0 16px 20px 42px;
  }
}
</style>
