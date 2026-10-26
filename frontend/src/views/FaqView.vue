<template>
  <div class="marketing-page faq-page">
    <LandingHeader @open-auth="openAuth" />

    <main class="faq-main">
      <div class="faq-glow" aria-hidden="true"></div>

      <div class="page-container">
        <header class="faq-hero">
          <div class="category-pill">
            <RoundedBallIcon :width="14" :height="20" />
            <span class="pill-text">SUPPORT</span>
          </div>
          <h1 class="faq-title">Frequently Asked Questions</h1>
          <p class="faq-intro">
            What Brain is, how it works, and where its limits are.
          </p>
        </header>

        <section class="faq-list" aria-label="Frequently asked questions">
          <article
            v-for="(faq, index) in faqs"
            :key="faq.question"
            class="faq-item"
            :class="{ 'is-open': openIndex === index }"
          >
            <h2 class="faq-heading">
              <button
                :id="`faq-trigger-${index}`"
                type="button"
                class="faq-trigger"
                :aria-expanded="openIndex === index"
                :aria-controls="`faq-panel-${index}`"
                @click="toggle(index)"
              >
                <span class="faq-q-num">{{ String(index + 1).padStart(2, '0') }}</span>
                <span class="faq-question">{{ faq.question }}</span>
                <span class="faq-icon-wrapper" aria-hidden="true">
                  <span class="faq-icon">{{ openIndex === index ? '−' : '+' }}</span>
                </span>
              </button>
            </h2>

            <div
              v-show="openIndex === index"
              :id="`faq-panel-${index}`"
              class="faq-content"
              role="region"
              :aria-labelledby="`faq-trigger-${index}`"
            >
              <p class="faq-answer">{{ faq.answer }}</p>
            </div>
          </article>
        </section>

        <section class="faq-cta">
          <div class="faq-cta-copy">
            <p class="cta-eyebrow">STILL CURIOUS</p>
            <p class="cta-text">The fastest way to understand Brain is to run a scenario.</p>
          </div>
          <router-link to="/console" class="cta-btn">Open the console</router-link>
        </section>
      </div>
    </main>

    <LandingFooter />
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from 'vue'
import authStore from '../store/auth'
import LandingHeader from '../components/landing/LandingHeader.vue'
import LandingFooter from '../components/landing/LandingFooter.vue'
import RoundedBallIcon from '../components/common/RoundedBallIcon.vue'

const openAuth = () => {
  authStore.openAuthModal('login')
}

onMounted(() => {
  document.body.style.backgroundColor = '#A2F1DF'
  window.scrollTo(0, 0)
})

onUnmounted(() => {
  document.body.style.backgroundColor = ''
})

const openIndex = ref(0)

const toggle = (index) => {
  openIndex.value = openIndex.value === index ? -1 : index
}

const faqs = [
  {
    question: 'What is Brain?',
    answer:
      'Brain is envisioned as an AI-powered simulation and predictive intelligence platform for exploring scenarios, stakeholder responses, and possible outcomes.',
  },
  {
    question: 'How does Brain generate predictions?',
    answer:
      'The proposed workflow uses source information, scenario modelling, simulated AI agents, and structured analysis to explore possible outcomes. Actual methodology and supported features will depend on the implemented product.',
  },
  {
    question: 'Can Brain predict the future accurately?',
    answer:
      "No AI simulation can guarantee future outcomes. Brain's outputs should be treated as model-generated scenarios and validated against reliable evidence.",
  },
  {
    question: 'Who can use Brain?',
    answer:
      'The intended audience includes businesses, founders, researchers, analysts, product teams, and professionals who need to explore complex decisions.',
  },
  {
    question: 'Can I upload my own documents?',
    answer:
      'Document uploads can be offered if supported by the implemented platform. Supported formats, file limits, and data-handling policies should be documented before launch.',
  },
  {
    question: 'Is Brain a replacement for human decision-making?',
    answer:
      'No. It is intended to support analysis and scenario exploration while leaving final decisions to people.',
  },
  {
    question: 'What kinds of scenarios can I explore with Brain?',
    answer:
      'Brain is intended for decisions that involve multiple stakeholders and uncertain outcomes, such as market entry, product launches, policy changes, or shifts in public sentiment. The scenario types available to you depend on the features enabled for your account.',
  },
  {
    question: 'How do I get started with Brain?',
    answer:
      'Start from the Brain console: describe the scenario you want to explore, add any supporting material the platform supports, and review the simulated outcomes and generated report. Access and available features may vary during rollout.',
  },
  {
    question: 'How is my data handled?',
    answer:
      'Uploaded documents and simulation data are used to run your scenarios and generate reports. Retention and privacy practices depend on the deployed configuration, and data-handling policies should be reviewed before uploading sensitive material.',
  },
]
</script>

<style scoped>
.faq-page {
  min-height: 100vh;
  background-color: #A2F1DF;
  color: #0a1c17;
}

.faq-main {
  position: relative;
  padding: 9rem 1.5rem 6rem;
  overflow: hidden;
}

.faq-glow {
  position: absolute;
  top: 4rem;
  left: 50%;
  width: min(720px, 90vw);
  height: 360px;
  transform: translateX(-50%);
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.45), transparent 70%);
  filter: blur(50px);
  pointer-events: none;
}

.page-container {
  position: relative;
  z-index: 1;
  max-width: 56rem;
  margin: 0 auto;
}

.faq-hero {
  text-align: center;
  margin-bottom: 4rem;
}

.category-pill {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 6px 14px;
  margin-bottom: 22px;
  background: rgba(255, 255, 255, 0.65);
  border: 1px solid rgba(7, 57, 51, 0.15);
  border-radius: 9999px;
  backdrop-filter: blur(10px);
}

.pill-text {
  font-family: 'Michroma', sans-serif;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.15em;
  color: #073933;
}

.faq-title {
  margin: 0 0 16px;
  font-family: 'Microgramma', 'Microgramma Bold', sans-serif !important;
  font-size: clamp(2.2rem, 3.8vw, 3.4rem);
  font-weight: 800;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  line-height: 1.15;
  color: #073933;
}

.faq-intro {
  margin: 0 auto;
  max-width: 34rem;
  font-family: Michroma, "Michroma Fallback", sans-serif;
  font-size: 14px;
  font-weight: 500;
  line-height: 22.75px;
  color: rgb(0, 0, 0);
}

.faq-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.faq-item {
  background: rgba(255, 255, 255, 0.7);
  border: 1px solid rgba(7, 57, 51, 0.15);
  border-radius: 1rem;
  overflow: hidden;
  box-shadow: 0 4px 18px rgba(7, 57, 51, 0.06);
  backdrop-filter: blur(12px);
  transition: background-color 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
}

.faq-item:hover {
  border-color: rgba(7, 57, 51, 0.35);
  background: rgba(255, 255, 255, 0.85);
}

.faq-item.is-open {
  background: rgba(255, 255, 255, 0.95);
  border-color: #073933;
  box-shadow: 0 8px 25px rgba(7, 57, 51, 0.12);
}

.faq-heading {
  margin: 0;
  font-size: inherit;
  font-weight: inherit;
}

.faq-trigger {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 24px 26px;
  background: transparent;
  border: none;
  text-align: left;
  cursor: pointer;
  color: inherit;
}

.faq-trigger:focus-visible {
  outline: 2px solid #073933;
  outline-offset: -2px;
  border-radius: 1rem;
}

.faq-q-num {
  font-family: 'Michroma', sans-serif;
  font-size: 13px;
  font-weight: 700;
  color: #2d554c;
}

.faq-question {
  flex: 1;
  font-family: 'Inter', sans-serif;
  font-size: 1.12rem;
  font-weight: 600;
  line-height: 1.4;
  letter-spacing: -0.01em;
  color: #073933;
}

.faq-icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  border: 1px solid rgba(7, 57, 51, 0.16);
  background: rgba(7, 57, 51, 0.08);
  transition: background-color 0.2s ease, border-color 0.2s ease;
}

.faq-item.is-open .faq-icon-wrapper {
  background: #073933;
  border-color: #073933;
}

.faq-icon {
  font-size: 16px;
  font-weight: 700;
  line-height: 1;
  color: #073933;
}

.faq-item.is-open .faq-icon {
  color: #ffffff;
}

.faq-content {
  padding: 0 26px 26px 58px;
}

.faq-answer {
  margin: 0;
  font-size: 0.95rem;
  line-height: 1.7;
  color: #000000;
}

.faq-cta {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  margin-top: 4rem;
  padding: 28px 30px;
  border: 1px solid rgba(7, 57, 51, 0.15);
  border-radius: 1rem;
  background: rgba(255, 255, 255, 0.65);
  backdrop-filter: blur(12px);
}

.cta-eyebrow {
  margin: 0 0 8px;
  font-family: 'Michroma', sans-serif;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.15em;
  color: #2d554c;
}

.cta-text {
  margin: 0;
  font-size: 1rem;
  line-height: 1.5;
  color: #073933;
  font-weight: 600;
}

.cta-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.85rem 1.75rem;
  border-radius: 0.75rem;
  background: #073933;
  color: #ffffff;
  font-family: 'Inter', sans-serif;
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  text-decoration: none;
  transition: all 0.25s ease;
  box-shadow: 0 2px 8px rgba(7, 57, 51, 0.2);
}

.cta-btn:hover {
  background: #042823;
  transform: translateY(-1px);
  box-shadow: 0 4px 14px rgba(7, 57, 51, 0.35);
}

@media (max-width: 640px) {
  .faq-main {
    padding: 7rem 1rem 4rem;
  }

  .faq-hero {
    margin-bottom: 2.5rem;
  }

  .faq-trigger {
    padding: 18px;
    gap: 14px;
  }

  .faq-content {
    padding: 0 18px 22px 46px;
  }

  .faq-cta {
    padding: 22px;
  }
}
</style>
