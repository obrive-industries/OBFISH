<template>
  <section class="section-faq" id="faq">
    <div class="container">
      <div class="section-header">
        <div class="category-pill">
          <span class="pill-dot"></span>
          KNOWLEDGE BASE
        </div>

        <h2 class="section-title">
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
          :class="{ 'open': openIndex === index }"
        >
          <button class="faq-trigger" @click="toggle(index)">
            <span class="faq-q-num">0{{ index + 1 }}</span>
            <span class="faq-question">{{ faq.question }}</span>
            <span class="faq-icon">{{ openIndex === index ? '−' : '+' }}</span>
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
  padding: 120px 24px;
  background: #070b0e;
  position: relative;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.container {
  max-width: 960px;
  margin: 0 auto;
}

.section-header {
  text-align: center;
  margin-bottom: 60px;
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
  font-size: 1.15rem;
  line-height: 1.6;
  color: #94a3b8;
  margin: 0;
}

.faq-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.faq-item {
  background: rgba(12, 18, 22, 0.65);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 14px;
  overflow: hidden;
  backdrop-filter: blur(12px);
  transition: all 0.3s ease;
}

.faq-item.open {
  border-color: rgba(0, 229, 163, 0.35);
  background: rgba(12, 18, 22, 0.95);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
}

.faq-trigger {
  width: 100%;
  display: flex;
  align-items: center;
  padding: 22px 28px;
  background: transparent;
  border: none;
  cursor: pointer;
  text-align: left;
  gap: 16px;
}

.faq-q-num {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.85rem;
  font-weight: 700;
  color: #00E5A3;
}

.faq-question {
  flex: 1;
  font-family: 'Space Grotesk', sans-serif;
  font-size: 1.15rem;
  font-weight: 600;
  color: #ffffff;
}

.faq-icon {
  font-family: 'JetBrains Mono', monospace;
  font-size: 1.5rem;
  color: #00E5A3;
  width: 24px;
  text-align: center;
  line-height: 1;
}

.faq-content {
  padding: 0 28px 24px 68px;
  animation: fadeIn 0.3s ease;
}

.faq-answer {
  font-size: 1rem;
  line-height: 1.65;
  color: #94a3b8;
  margin: 0;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-4px); }
  to { opacity: 1; transform: translateY(0); }
}

@media (max-width: 640px) {
  .faq-trigger {
    padding: 18px 20px;
    gap: 12px;
  }

  .faq-content {
    padding: 0 20px 20px 20px;
  }

  .faq-question {
    font-size: 1rem;
  }
}
</style>
