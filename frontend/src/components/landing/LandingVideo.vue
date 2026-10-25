<template>
  <section id="demo-video" class="py-20 bg-black relative z-10 overflow-hidden">
    <div class="orb orb-1" aria-hidden="true"></div>
    <div class="container-main relative z-[2]">
      <div class="text-center mb-16">
        <p class="text-sm font-medium text-gray-400 uppercase tracking-wider mb-4">Demo Videos</p>
        <h2 class="text-4xl md:text-5xl font-bold text-white mb-4">Watch Brain in Action</h2>
      </div>

      <div class="flex flex-col md:flex-row gap-8 max-w-5xl mx-auto">
        <!-- Tabs -->
        <div class="md:w-1/3 flex flex-col gap-4">
          <button
            v-for="(video, idx) in videos"
            :key="video.bvid"
            @click="activeIdx = idx"
            class="video-btn text-left p-4 rounded-xl transition-all duration-300"
            :class="activeIdx === idx ? 'is-active' : 'is-idle'"
          >
            <div class="flex items-center gap-3 mb-2">
              <span
                class="w-8 h-8 rounded-full flex items-center justify-center text-sm font-mono"
                :class="activeIdx === idx ? 'bg-white/10 text-white' : 'bg-white/5 text-gray-500'"
              >
                {{ idx + 1 }}
              </span>
              <span class="font-semibold">{{ video.title }}</span>
            </div>
            <p class="text-sm opacity-70 ml-11">{{ video.desc }}</p>
          </button>

          <a
            :href="currentVideo.url"
            target="_blank"
            rel="noopener noreferrer"
            class="inline-flex items-center gap-2 text-sm text-gray-500 hover:text-white transition-colors mt-2 ml-2"
          >
            Watch full video on Bilibili ↗
          </a>
        </div>

        <!-- Video Player Frame -->
        <div class="md:w-2/3">
          <div class="player-frame relative w-full rounded-2xl overflow-hidden aspect-video bg-white/5 border border-white/10">
            <iframe
              :src="currentVideoEmbed"
              class="absolute inset-0 w-full h-full"
              scrolling="no"
              frameborder="0"
              allowfullscreen="true"
            ></iframe>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed } from 'vue'

const activeIdx = ref(0)

const videos = [
  {
    title: 'WHU Opinion Prediction',
    desc: 'Wuhan University public opinion prediction and MiroFish technical walkthrough',
    bvid: 'BV1VYBsBHEMY',
    url: 'https://www.bilibili.com/video/BV1VYBsBHEMY/'
  },
  {
    title: 'Dream of the Red Chamber',
    desc: 'Predicting the lost ending of Dream of the Red Chamber based on the first 80 chapters',
    bvid: 'BV1cPk3BBExq',
    url: 'https://www.bilibili.com/video/BV1cPk3BBExq'
  }
]

const currentVideo = computed(() => videos[activeIdx.value])
const currentVideoEmbed = computed(() => `https://player.bilibili.com/player.html?bvid=${currentVideo.value.bvid}&page=1&high_quality=1&danmaku=0`)
</script>

<style scoped>
.orb-1 {
  position: absolute;
  width: 320px;
  height: 220px;
  border-radius: 50%;
  background: rgba(234, 160, 40, 0.08);
  filter: blur(60px);
  top: 20%;
  right: 10%;
  transform: rotate(-10deg);
  pointer-events: none;
  z-index: 1;
}

.video-btn {
  border: 1px solid rgba(255, 255, 255, 0.08);
  -webkit-backdrop-filter: blur(12px);
  backdrop-filter: blur(12px);
  cursor: pointer;
}

.video-btn.is-active {
  background: rgba(255, 255, 255, 0.07);
  border-color: rgba(255, 255, 255, 0.2);
  color: #ffffff;
}

.video-btn.is-idle {
  background: rgba(255, 255, 255, 0.02);
  border-color: rgba(255, 255, 255, 0.06);
  color: #9ca3af;
}

.video-btn.is-idle:hover {
  background: rgba(255, 255, 255, 0.04);
  border-color: rgba(255, 255, 255, 0.12);
  color: #e5e7eb;
}

.player-frame {
  border: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(8px);
}
</style>
