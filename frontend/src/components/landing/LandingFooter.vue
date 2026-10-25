<template>
  <footer class="bg-transparent py-8 relative z-10" aria-label="Site footer">
    <div class="container-main">
      <div class="flex flex-col md:flex-row items-center justify-between gap-6">
        <!-- Left: Logo & Social Links -->
        <div class="flex items-center gap-4">
          <router-link to="/" class="logo" aria-label="Brain Home">
            <img src="/obrive-logo.svg" alt="Obrive" class="logo-img" />
            <span class="logo-divider">/</span>
            <span class="logo-text">BRAIN</span>
          </router-link>
          <span class="text-[#0a1c17]/30">|</span>
          <a
            href="https://www.linkedin.com/company/obrive-industries"
            target="_blank"
            rel="noopener noreferrer"
            class="text-[#163830] hover:text-[#0a1c17] transition-colors"
            aria-label="LinkedIn"
          >
            <svg class="w-4 h-4" viewBox="0 0 24 24" fill="currentColor">
              <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>
            </svg>
          </a>
          <a
            href="https://x.com/obriveinc"
            target="_blank"
            rel="noopener noreferrer"
            class="text-[#163830] hover:text-[#0a1c17] transition-colors"
            aria-label="X"
          >
            <svg class="w-4 h-4" viewBox="0 0 24 24" fill="currentColor">
              <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z" />
            </svg>
          </a>
          <a
            href="https://www.instagram.com/obrive.inc"
            target="_blank"
            rel="noopener noreferrer"
            class="text-[#163830] hover:text-[#0a1c17] transition-colors"
            aria-label="Instagram"
          >
            <svg class="w-4 h-4" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z" />
            </svg>
          </a>
        </div>

        <!-- Right: FAQs, Legal, Terms Links & Admin Wishlist -->
        <div class="flex flex-wrap items-center gap-4 md:gap-6 text-sm text-[#163830]">
          <a href="https://obrive.com/legal" target="_blank" rel="noopener noreferrer" class="hover:text-[#0a1c17] transition-colors">Legal</a>
          <a href="https://obrive.com/terms-accessibility" target="_blank" rel="noopener noreferrer" class="hover:text-[#0a1c17] transition-colors">Terms</a>
          <router-link
            v-if="authStore.isAdmin.value"
            to="/admin/wishlist"
            class="inline-flex items-center gap-2 px-4 py-2 bg-[#074139] text-white hover:bg-[#042823] rounded-lg font-semibold text-sm transition-all shadow-md"
            title="View Wishlist Submissions (Admin)"
          >
            📋 Wishlist Leads
          </router-link>
          <a
            href="/faqs"
            class="inline-flex items-center gap-2 px-4 py-2 bg-[#074139] text-white hover:bg-[#042823] rounded-lg font-semibold text-sm transition-all shadow-md"
          >
            FAQs
          </a>
        </div>
      </div>

      <div class="mt-6 pt-4 text-center text-xs text-[#2d554c]">
        © 2026 Obrive Industries. All rights reserved.
      </div>
    </div>
  </footer>
</template>

<script setup>
import authStore from '../../store/auth'
</script>

<style scoped>
.container-main {
  max-width: 80rem;
  margin-left: auto;
  margin-right: auto;
  padding-left: 1rem;
  padding-right: 1rem;
}

@media (min-width: 640px) {
  .container-main {
    padding-left: 1.5rem;
    padding-right: 1.5rem;
  }
}

@media (min-width: 1024px) {
  .container-main {
    padding-left: 2rem;
    padding-right: 2rem;
  }
}

.logo {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  transition: opacity 0.2s;
}

.logo:hover {
  opacity: 0.85;
}

.logo-img {
  height: 28px;
  width: auto;
  object-fit: contain;
}

.logo-divider {
  color: #074139;
  font-size: 1.35rem;
  font-weight: 500;
  line-height: 1;
  opacity: 0.85;
}

.logo-text {
  font-family: 'Space Grotesk', 'Inter', system-ui, sans-serif;
  font-weight: 800;
  font-size: 1.35rem;
  letter-spacing: 0.08em;
  color: #074139;
  line-height: 1;
}
</style>
