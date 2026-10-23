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
          Everything you need to know about predictive scenario modeling and OBMIND intelligence.
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
    question: 'What is OBMIND?',
    answer: 'OBMIND is envisioned as an AI-powered simulation and predictive intelligence platform for exploring scenarios, stakeholder responses, and possible outcomes.'
  },
  {
    question: 'How does OBMIND generate predictions?',
    answer: 'The proposed workflow uses source information, scenario modelling, simulated AI agents, and structured analysis to explore possible outcomes. Actual methodology and supported features will depend on the implemented product.'
  },
  {
    question: 'Can OBMIND predict the future accurately?',
    answer: "No AI simulation can guarantee future outcomes. OBMIND's outputs should be treated as model-generated scenarios and validated against reliable evidence."
  },
  {
    question: 'Who can use OBMIND?',
    answer: 'The intended audience includes businesses, founders, researchers, analysts, product teams, and professionals who need to explore complex decisions.'
  },
  {
    question: 'Can I upload my own documents?',
    answer: 'Document uploads can be offered if supported by the implemented platform. Supported formats, file limits, and data-handling policies should be documented before launch.'
  },
  {
    question: 'Is OBMIND a replacement for human decision-making?',
    answer: 'No. It is intended to support analysis and scenario exploration while leaving final decisions to people.'
  }
]
</script>

<style scoped>
.section-faq {
  padding: 110px 24px;
  background: #ffffff;
  position: relative;
  border-top: 1px solid rgba(7, 65, 57, 0.12);
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
