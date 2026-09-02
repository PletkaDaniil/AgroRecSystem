<template>
  <div class="page">
    <div class="scroll-rail"><div class="scroll-rail-fill" :style="{ width: scrollPct + '%' }"></div></div>

    <section class="hero" @mousemove="onHeroMove" @mouseleave="onHeroLeave">
      <div class="hero-bg">
        <div class="mesh-blob mesh-blob--blue"></div>
        <div class="mesh-blob mesh-blob--green"></div>
        <div class="mesh-blob mesh-blob--amber"></div>

        <div class="cursor-glow" :style="cursorGlowStyle"></div>

        <div class="hero-grid"></div>

        <div class="coord-marks">
          <span class="coord coord--tl">N 54.2°</span>
          <span class="coord coord--tr">E 39.6°</span>
          <span class="coord coord--bl">ALT 512km</span>
        </div>

        <div class="hero-bg-word" aria-hidden="true">N₂</div>

        <svg class="spectral-svg" viewBox="0 0 900 260" preserveAspectRatio="none">
          <defs>
            <linearGradient id="spectralGrad" x1="0" y1="0" x2="1" y2="0.3">
              <stop offset="0%"  stop-color="#3d6ce8"/>
              <stop offset="50%" stop-color="#6bb56a"/>
              <stop offset="100%" stop-color="#e8973d"/>
            </linearGradient>
            <linearGradient id="spectralGradGhost" x1="0" y1="0" x2="1" y2="0">
              <stop offset="0%"  stop-color="#3d6ce8"/>
              <stop offset="100%" stop-color="#e8973d"/>
            </linearGradient>
          </defs>

          <path
            class="spectral-path spectral-path--ghost"
            d="M0,120 C50,150 80,60 120,55 C160,50 190,140 230,150 C270,160 300,40 340,30 C380,20 410,110 450,120 C490,130 520,35 560,25 C600,15 630,100 670,105 C710,110 740,50 780,45 C820,40 860,90 900,85"
          />
          <path
            class="spectral-path"
            d="M0,190 C60,188 90,150 130,140 C170,130 190,175 230,180 C270,185 300,90 340,70 C380,50 410,120 450,130 C490,140 520,60 560,45 C600,30 630,95 670,110 C710,125 740,80 780,70 C820,60 860,100 900,95"
          />
          <line class="spectral-scan" x1="0" y1="0" x2="0" y2="260" />
        </svg>
      </div>

      <div class="hero-inner">
        <div class="hero-eyebrow reveal">
          <span class="dot"></span>
          О проекте
          <span class="eyebrow-tag">// 00</span>
        </div>
        <h1 class="hero-title reveal" style="transition-delay:.05s">
          Рекомендации по<br/>
          азотным подкормкам<br/>
          <em>из космоса</em>
        </h1>
        <p class="hero-desc reveal" style="transition-delay:.1s">
          Цель проекта — создать рекомендательную систему по азотным подкормкам зерновых культур на основе данных дистанционного зондирования Земли. Система помогает снизить затраты на удобрения, повысить качество зерна и уменьшить экологические риски.
        </p>

        <div class="hero-stats reveal" style="transition-delay:.15s" ref="statsEl">
          <div class="stat">
            <span class="stat-num">{{ heroStat1 }}</span>
            <span class="stat-label">Ключевых индекса</span>
          </div>
          <div class="stat-div"></div>
          <div class="stat">
            <span class="stat-num">3–5</span>
            <span class="stat-label">Зон дозирования</span>
          </div>
          <div class="stat-div"></div>
          <div class="stat">
            <span class="stat-num">−{{ heroStat2 }}%</span>
            <span class="stat-label">Расход азота</span>
          </div>
        </div>
      </div>
    </section>

    <!-- КОНКУРЕНТНОЕ ПРЕИМУЩЕСТВО -->
    <section class="split-section split-section--photo-wide">
      <div class="section-bg-word section-bg-word--left" aria-hidden="true">01</div>
      <div class="mesh-blob mesh-blob--green mesh-blob--corner-tr"></div>
      <div class="split-inner split-inner--photo-left">
        <div class="split-media reveal reveal--left">
          <div
            class="media-tall media-tall--square media-tall--large"
            @mousemove="onMediaMove($event, 0)"
            @mouseleave="onMediaLeave(0)"
            :style="mediaStyles[0]"
          >
            <img :src="aboutPhoto1" alt="" class="media-photo" />
          </div>
        </div>
        <div class="split-text reveal reveal--right" style="transition-delay:.1s">
          <div class="section-eyebrow"><span class="section-eyebrow-num">01</span>Конкурентное преимущество</div>
          <h2 class="split-title">Аналитика,<br/>подтверждённая<br/>исследованиями</h2>
          <p class="split-desc">
            В основе системы — уникальный аналитический аппарат, построенный на взаимосвязи индексов ChlRI и PRImod с фактической дозой внесённого азота. Методика подтверждена научными исследованиями, включая проект РФФИ № 19-29-05184-мк.
          </p>
          <div class="badge-row">
            <span class="badge-chip badge-chip--blue">РФФИ № 19-29-05184-мк</span>
            <span class="badge-chip badge-chip--amber">Лобачевский CubeSat-16U</span>
          </div>
          <p class="split-desc split-desc--muted">
            Система рассчитана на отечественные спутниковые данные повышенного разрешения со спутника «Лобачевский» (CubeSat-16U), что снижает зависимость от зарубежных источников снимков.
          </p>
        </div>
      </div>
    </section>

    <!-- ЧТО ДЕЛАЕТ СИСТЕМА -->
    <section class="tool-section">
      <div class="section-bg-word section-bg-word--right" aria-hidden="true">GIS</div>
      <div class="mesh-blob mesh-blob--blue mesh-blob--corner-bl"></div>

      <div class="tool-header reveal">
        <div class="section-eyebrow"><span class="section-eyebrow-num">02</span>Что делает система</div>
        <h2 class="tool-title">От снимка — к карте-заданию</h2>
        <p class="tool-subtitle">
          Программный комплекс анализирует мульти- и гиперспектральные снимки (400–800 нм) со спутников и БПЛА и рассчитывает три ключевых индекса
        </p>
      </div>

      <div class="workspace-grid">
        <div class="index-list reveal reveal--left">
          <div
            v-for="(idx, i) in indices"
            :key="idx.name"
            class="index-item-wrap"
            :style="{ transitionDelay: (i * 0.08) + 's' }"
          >
            <button
              class="index-item"
              :class="['index-item--' + idx.color, { 'index-item--open': openIndexName === idx.name }]"
              @click="toggleIndex(idx.name)"
            >
              <span class="index-icon" v-html="idx.icon"></span>
              <div class="index-info">
                <span class="index-name">{{ idx.name }}</span>
                <span class="index-desc">{{ idx.desc }}</span>
              </div>
              <span class="index-arrow index-arrow--toggle">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
              </span>
            </button>

            <transition name="index-detail">
              <div v-if="openIndexName === idx.name" class="index-detail">
                <p class="index-detail-text">{{ idx.detail }}</p>
                <div class="index-detail-wave">
                  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M2 8 Q6 4 10 8 Q14 12 18 8 Q20 6 22 8"/></svg>
                  Диапазоны: {{ idx.wavelength }}
                </div>
              </div>
            </transition>
          </div>


          <div class="flow-note">
            <div class="flow-note-line"></div>
            <p>
              По динамике трёх индексов система определяет степень азотного голодания для каждого участка поля и формирует карту-задание с дозами азота в действующем веществе — с делением поля на 3–5 зон.
            </p>
          </div>

          <div class="export-note">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
            Результат выгружается в ГИС-формате ShapeFile — для бортового компьютера техники
          </div>
        </div>

        <div class="split-media reveal reveal--right" style="transition-delay:.1s">
          <div
            class="media-tall media-tall--in-grid media-tall--wide"
            @mousemove="onMediaMove($event, 1)"
            @mouseleave="onMediaLeave(1)"
            :style="mediaStyles[1]"
          >
            <img :src="aboutPhoto2" alt="" class="media-photo" />
            <div class="media-scan"></div>
          </div>
        </div>
      </div>

      <p class="footnote">* система преимущественно рассчитана на гиперспектральные снимки</p>
    </section>

    <!-- ЭКОНОМИЧЕСКИЙ ЭФФЕКТ -->
    <section class="split-section split-section--rev">
      <div class="section-bg-word section-bg-word--left" aria-hidden="true">ROI</div>
      <div class="mesh-blob mesh-blob--amber mesh-blob--corner-tr"></div>

      <div class="split-inner split-inner--rev">
        <div class="split-media reveal reveal--left">
          <div
            class="media-tall media-tall--wide-narrow"
            @mousemove="onMediaMove($event, 2)"
            @mouseleave="onMediaLeave(2)"
            :style="mediaStyles[2]"
          >
            <img :src="aboutPhoto3" alt="" class="media-photo" />
            <div class="media-scan"></div>
          </div>
        </div>
        <div class="split-text reveal reveal--right" style="transition-delay:.1s">
          <div class="section-eyebrow"><span class="section-eyebrow-num">03</span>Экономический эффект</div>
          <h2 class="split-title">Меньше азота —<br/>выше прибыль</h2>
          <p class="split-desc">
            Дифференцированное внесение позволяет снизить расход азотных удобрений и повысить качество зерна, что увеличивает прибыль сельхозпредприятия или фермы.
          </p>

          <div class="big-stat" ref="bigStatEl">
            <span class="big-stat-num">до {{ bigStatNum }}%</span>
            <span class="big-stat-label">снижение расхода азотных удобрений</span>
            <div class="big-stat-bar"><div class="big-stat-bar-fill" :style="{ width: bigStatNum + '%' }"></div></div>
          </div>
        </div>
      </div>
    </section>

    <!-- КОМУ ПРИГОДИТСЯ -->
    <section class="audience-section">
      <div class="section-bg-word section-bg-word--right" aria-hidden="true">AGRO</div>
      <div class="mesh-blob mesh-blob--green mesh-blob--corner-bl"></div>

      <div class="tool-header reveal">
        <div class="section-eyebrow"><span class="section-eyebrow-num">04</span>Кому это может пригодиться</div>
        <h2 class="tool-title">Для тех, кто внедряет точное земледелие</h2>
      </div>

      <div class="audience-grid">
        <div
          v-for="(a, i) in audiences"
          :key="a.title"
          class="audience-card"
          :class="'audience-card--' + a.color"
          :style="{ transitionDelay: (i * 0.1) + 's' }"
        >
          <span class="audience-icon" v-html="a.icon"></span>
          <span class="audience-title">{{ a.title }}</span>
          <p class="audience-desc">{{ a.desc }}</p>
        </div>
      </div>
    </section>
  </div>

  <SupportBanner />
</template>

<script setup>
import SupportBanner from '@/components/SupportBanner.vue'
import aboutPhoto1 from '../components/images/about_photo_1.png'
import aboutPhoto2 from '../components/images/about_photo_2.png'
import aboutPhoto3 from '../components/images/about_photo_3.png'
import { reactive, ref, onMounted, onBeforeUnmount } from 'vue'

/* ---------- прокрутка ---------- */
const scrollPct = ref(0)
const onScroll = () => {
  const h = document.documentElement
  const scrolled = h.scrollTop
  const max = h.scrollHeight - h.clientHeight
  scrollPct.value = max > 0 ? Math.min(100, (scrolled / max) * 100) : 0
}

/* ---------- появление блоков ---------- */
let revealObserver
const setupReveal = () => {
  const els = document.querySelectorAll('.reveal')
  revealObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('reveal--visible')
        revealObserver.unobserve(entry.target)
      }
    })
  }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' })
  els.forEach((el) => revealObserver.observe(el))
}

/* ---------- подсветка курсора ---------- */
const cursorGlowStyle = ref({ opacity: 0 })
const onHeroMove = (e) => {
  const rect = e.currentTarget.getBoundingClientRect()
  cursorGlowStyle.value = {
    left: (e.clientX - rect.left) + 'px',
    top: (e.clientY - rect.top) + 'px',
    opacity: 1,
  }
}
const onHeroLeave = () => {
  cursorGlowStyle.value = { ...cursorGlowStyle.value, opacity: 0 }
}

/* ---------- счётчики ---------- */
const heroStat1 = ref(0)
const heroStat2 = ref(0)
const bigStatNum = ref(0)
const statsEl = ref(null)
const bigStatEl = ref(null)
const openIndexName = ref(null)
const toggleIndex = (name) => {
  openIndexName.value = openIndexName.value === name ? null : name
}

const countTo = (targetRef, target, duration = 900) => {
  const start = performance.now()
  const tick = (now) => {
    const p = Math.min(1, (now - start) / duration)
    const eased = 1 - Math.pow(1 - p, 3)
    targetRef.value = Math.round(eased * target)
    if (p < 1) requestAnimationFrame(tick)
  }
  requestAnimationFrame(tick)
}

let countObserver
const setupCounters = () => {
  countObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return
      if (entry.target === statsEl.value) {
        countTo(heroStat1, 3)
        countTo(heroStat2, 30)
      }
      if (entry.target === bigStatEl.value) {
        countTo(bigStatNum, 30, 1100)
      }
      countObserver.unobserve(entry.target)
    })
  }, { threshold: 0.5 })
  if (statsEl.value) countObserver.observe(statsEl.value)
  if (bigStatEl.value) countObserver.observe(bigStatEl.value)
}

/* ---------- наклон изображений ---------- */
const mediaStyles = reactive([{}, {}, {}])
const onMediaMove = (e, i) => {
  const el = e.currentTarget, rect = el.getBoundingClientRect()
  const dx = (e.clientX - rect.left - rect.width  / 2) / (rect.width  / 2)
  const dy = (e.clientY - rect.top  - rect.height / 2) / (rect.height / 2)
  mediaStyles[i] = {
    transform:  `perspective(900px) rotateX(${-dy * 6}deg) rotateY(${dx * 6}deg) scale(1.015)`,
    transition: 'transform 0.08s ease',
  }
}
const onMediaLeave = (i) => {
  mediaStyles[i] = {
    transform:  'perspective(900px) rotateX(0deg) rotateY(0deg) scale(1)',
    transition: 'transform 0.5s cubic-bezier(0.16,1,0.3,1)',
  }
}

/* ---------- данные ---------- */
const indices = [
  {
    name: 'ChlRI',
    desc: 'Содержание хлорофилла в листе',
    color: 'blue',
    wavelength: '445 / 705 / 750 нм',
    detail: 'Оценивает содержание хлорофилла — основного пигмента, отвечающего за фотосинтез. Использует контраст между сильным поглощением света хлорофиллом в синей области (445 нм) и высоким отражением в ближнем ИК (750 нм), с опорой на чувствительную зону «красного края» (705 нм).',
    icon: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22C6 22 2 16 2 10c0 0 4-6 10-6s10 6 10 6c0 6-4 12-10 12z"/><line x1="12" y1="22" x2="12" y2="10"/></svg>`,
  },
  {
    name: 'PRImod',
    desc: 'Фотохимическая активность растений',
    color: 'amber',
    wavelength: '531 / 570 нм',
    detail: 'Показывает эффективность фотосинтеза и позволяет выявлять стресс у растений. Фиксирует изменения в ксантофилловом цикле — механизме защиты от избыточного света — сравнивая отражение на 531 нм с более стабильной опорной точкой на 570 нм.',
    icon: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>`,
  },
  {
    name: 'NDVI',
    desc: 'Общий вегетационный индекс',
    color: 'green',
    wavelength: '680 / 750 нм',
    detail: 'Даёт общую оценку состояния и активности растительного покрова. Использует контраст между сильным поглощением света хлорофиллом в красной области (680 нм) и высоким отражением в ближнем ИК (750 нм) — чем плотнее и здоровее растительность, тем сильнее этот контраст.',
    icon: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M2 8 Q6 4 10 8 Q14 12 18 8 Q20 6 22 8"/><path d="M2 16 Q6 12 10 16 Q14 20 18 16 Q20 14 22 16"/></svg>`,
  },
]

const audiences = [
  {
    title: 'Сельхозтоваропроизводители',
    desc: 'Средние и крупные хозяйства, готовые использовать технологии точного земледелия для снижения издержек и роста урожайности.',
    color: 'blue',
    icon: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M2 22h20"/><path d="M4 22V10l8-6 8 6v12"/><path d="M9 22v-6h6v6"/></svg>`,
  },
  {
    title: 'Государственные учреждения',
    desc: 'Организации, осуществляющие поддержку сельхозпроизводителей и заинтересованные в снижении экологических рисков отрасли.',
    color: 'green',
    icon: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21h18"/><path d="M5 21V7l7-4 7 4v14"/><path d="M9 9h1M9 13h1M14 9h1M14 13h1"/></svg>`,
  },
]

onMounted(() => {
  window.addEventListener('scroll', onScroll, { passive: true })
  onScroll()
  setupReveal()
  setupCounters()
})
onBeforeUnmount(() => {
  window.removeEventListener('scroll', onScroll)
  revealObserver && revealObserver.disconnect()
  countObserver && countObserver.disconnect()
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

.page {
  --c-blue: #3d6ce8;
  --c-green: #6bb56a;
  --c-amber: #e8973d;
  background: #ffffff;
  font-family: 'Manrope', sans-serif;
  color: #1a1d23;
  min-height: 100vh;
  position: relative;
}

/* ---------- полоса прокрутки ---------- */
.scroll-rail {
  position: sticky;
  top: 0; left: 0; right: 0;
  height: 2px;
  background: transparent;
  z-index: 40;
}
.scroll-rail-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--c-blue), var(--c-green), var(--c-amber));
  transition: width 0.1s linear;
}

/* ---------- общие фоновые элементы ---------- */
.mesh-blob {
  position: absolute;
  width: 640px; height: 640px;
  border-radius: 50%;
  filter: blur(70px);
  pointer-events: none;
}
.mesh-blob--blue   { background: radial-gradient(circle, rgba(61,108,232,0.16), transparent 68%); }
.mesh-blob--green  { background: radial-gradient(circle, rgba(107,181,106,0.15), transparent 68%); }
.mesh-blob--amber  { background: radial-gradient(circle, rgba(232,151,61,0.14), transparent 68%); }
.mesh-blob--corner-tr { top: -260px; right: -180px; width: 480px; height: 480px; }
.mesh-blob--corner-bl { bottom: -260px; left: -180px; width: 480px; height: 480px; }

.section-bg-word {
  position: absolute;
  font-family: 'JetBrains Mono', monospace;
  font-size: 200px;
  font-weight: 800;
  line-height: 1;
  color: rgba(61,108,232,0.045);
  user-select: none;
  pointer-events: none;
  z-index: 0;
}
.section-bg-word--left  { left: -12px; bottom: -36px; }
.section-bg-word--right { right: -12px; bottom: -36px; }

.split-section, .tool-section, .audience-section {
  position: relative;
  overflow: hidden;
}

/* ---------- главный экран ---------- */
.hero {
  position: relative;
  padding: 88px 0 64px;
  border-bottom: 1px solid #e8eaee;
  background: #fdfdfe;
  overflow: hidden;
}
.hero-bg {
  position: absolute; inset: 0;
  pointer-events: none;
  overflow: hidden;
}

.mesh-blob--blue   { top: -260px; right: -160px; }
.hero-bg .mesh-blob--blue  { top: -260px; right: -160px; }
.hero-bg .mesh-blob--green { bottom: -280px; left: -180px; }
.hero-bg .mesh-blob--amber { top: 40%; left: 30%; width: 460px; height: 460px; opacity: 0.7; }

.cursor-glow {
  position: absolute;
  width: 380px; height: 380px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(61,108,232,0.09), transparent 70%);
  transform: translate(-50%, -50%);
  opacity: 0;
  transition: opacity 0.3s ease;
  pointer-events: none;
}

.hero-grid {
  position: absolute; inset: 0;
  background-image:
    linear-gradient(rgba(13,15,20,0.045) 1px, transparent 1px),
    linear-gradient(90deg, rgba(13,15,20,0.045) 1px, transparent 1px);
  background-size: 42px 42px;
  mask-image: radial-gradient(ellipse 80% 60% at 70% 20%, rgba(0,0,0,0.7), transparent 75%);
}

.coord-marks {
  position: absolute; inset: 0;
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  font-weight: 500;
  letter-spacing: 0.5px;
  color: rgba(61,108,232,0.45);
}
.coord { position: absolute; }
.coord::before { content: '+'; margin-right: 4px; opacity: 0.6; }
.coord--tl { top: 24px; left: 24px; }
.coord--tr { top: 24px; right: 24px; color: rgba(232,151,61,0.55); }
.coord--bl { bottom: 24px; left: 24px; color: rgba(107,181,106,0.55); }

.hero-bg-word {
  position: absolute;
  right: -10px;
  bottom: -60px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 320px;
  font-weight: 800;
  line-height: 1;
  color: rgba(61,108,232,0.05);
  user-select: none;
  pointer-events: none;
}

/* волнистая линия — сдвинута правее, компактнее, градиентная */
.spectral-svg {
  position: absolute;
  right: -14%;
  top: 2%;
  width: 52%;
  height: 66%;
  overflow: visible;
  transform: rotate(-4deg);
}
.spectral-path {
  fill: none;
  stroke: url(#spectralGrad);
  stroke-width: 2.4;
  stroke-linecap: round;
  opacity: 0.75;
  stroke-dasharray: 1400;
  stroke-dashoffset: 1400;
  animation: draw 2.4s cubic-bezier(0.16,1,0.3,1) 0.2s forwards;
}
.spectral-path--ghost {
  stroke: url(#spectralGradGhost);
  stroke-width: 12;
  opacity: 0.08;
  stroke-dasharray: none;
  stroke-dashoffset: 0;
  animation: none;
  filter: blur(1.5px);
}
@keyframes draw { to { stroke-dashoffset: 0; } }
.spectral-scan {
  stroke: var(--c-amber);
  stroke-width: 1;
  opacity: 0;
  animation: scanX 5s ease-in-out 2.6s infinite;
}
@keyframes scanX {
  0%   { transform: translateX(0);   opacity: 0; }
  8%   { opacity: 0.4; }
  50%  { transform: translateX(500px); opacity: 0.4; }
  58%  { opacity: 0; }
  100% { transform: translateX(500px); opacity: 0; }
}

.hero-inner {
  position: relative;
  max-width: 780px;
  margin: 0 auto;
  padding: 0 48px;
}
.hero-eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 1.8px;
  text-transform: uppercase;
  color: var(--c-blue);
  margin-bottom: 24px;
  font-family: 'JetBrains Mono', monospace;
}
.eyebrow-tag { color: #c5c9d4; font-weight: 500; letter-spacing: 0.5px; margin-left: 4px; }
.dot {
  width: 6px; height: 6px;
  background: var(--c-blue);
  border-radius: 50%;
  animation: pulse 2s ease-in-out infinite;
}
@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50%       { opacity: 0.35; transform: scale(0.6); }
}
.hero-title {
  font-size: clamp(32px, 4vw, 50px);
  font-weight: 800;
  line-height: 1.14;
  letter-spacing: -1.6px;
  color: #0d0f14;
  margin-bottom: 24px;
}
.hero-title em {
  font-style: normal;
  background: linear-gradient(120deg, var(--c-blue), var(--c-green));
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  position: relative;
}
.hero-title em::after {
  content: '';
  position: absolute;
  bottom: 2px; left: 0; right: 0;
  height: 3px;
  background: linear-gradient(90deg, var(--c-blue), var(--c-green));
  opacity: 0.25;
  border-radius: 2px;
}
.hero-desc {
  font-size: 14px;
  font-weight: 400;
  line-height: 1.8;
  color: #6b7280;
  margin-bottom: 14px;
  max-width: 560px;
}
.hero-stats {
  display: flex;
  align-items: center;
  gap: 28px;
  margin-top: 36px;
  padding: 24px 28px;
  background: rgba(255,255,255,0.65);
  backdrop-filter: blur(6px);
  border: 1px solid rgba(61,108,232,0.14);
  border-radius: 14px;
  width: fit-content;
}
.stat { display: flex; flex-direction: column; gap: 3px; }
.stat-num {
  font-size: 22px; font-weight: 800;
  color: #0d0f14; letter-spacing: -0.5px;
  font-family: 'JetBrains Mono', monospace;
  font-variant-numeric: tabular-nums;
}
.stat-label {
  font-size: 10px; color: #9ca3af;
  font-weight: 600; text-transform: uppercase; letter-spacing: 0.8px;
}
.stat-div { width: 1px; height: 32px; background: #e8eaee; }

/* ---------- появление блоков ---------- */
.reveal {
  opacity: 0;
  transform: translateY(16px);
  transition: opacity 0.7s cubic-bezier(0.16,1,0.3,1), transform 0.7s cubic-bezier(0.16,1,0.3,1);
}
.reveal--left  { transform: translateX(-18px) translateY(0); }
.reveal--right { transform: translateX(18px) translateY(0); }
.reveal--visible { opacity: 1; transform: translate(0,0); }

/* ---------- общие элементы секций ---------- */
.section-eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 1.6px;
  text-transform: uppercase;
  color: #9ca3af;
  margin-bottom: 16px;
  font-family: 'JetBrains Mono', monospace;
}
.section-eyebrow-num {
  color: var(--c-blue);
  background: rgba(61,108,232,0.08);
  border-radius: 4px;
  padding: 2px 6px;
}

.tool-section {
  max-width: 1200px; margin: 0 auto;
  padding: 64px 48px 24px;
}
.tool-header { position: relative; z-index: 1; margin-bottom: 32px; max-width: 640px; }
.tool-title {
  font-size: 22px; font-weight: 800;
  letter-spacing: -0.6px; color: #0d0f14; margin-bottom: 10px;
}
.tool-subtitle { font-size: 13px; color: #9ca3af; line-height: 1.7; }

.footnote {
  position: relative; z-index: 1;
  max-width: 1200px;
  margin: 8px auto 0;
  padding: 0 48px 8px;
  font-size: 11px;
  color: #696b72;
  font-family: 'JetBrains Mono', monospace;
}

/* ---------- секции с текстом и изображением ---------- */
.split-section {
  border-bottom: 1px solid #e8eaee;
}
.split-section--rev { background: #fafbfc; }
.split-inner {
  position: relative; z-index: 1;
  max-width: 1200px;
  margin: 0 auto;
  padding: 64px 48px;
  display: grid;
  grid-template-columns: 1.15fr 0.85fr;
  gap: 64px;
  align-items: center;
}
.split-section--photo-wide .split-inner {
  grid-template-columns: 0.7fr 1.3fr;
}
.split-section--photo-wide .split-inner--photo-left {
  grid-template-columns: 1.2fr 0.7fr;
}
.split-inner--rev { grid-template-columns: 0.85fr 1.15fr; }
.split-inner--rev .split-media { order: 1; }
.split-inner--rev .split-text  { order: 2; }

.split-title {
  font-size: 26px;
  font-weight: 800;
  letter-spacing: -0.8px;
  line-height: 1.2;
  color: #0d0f14;
  margin-bottom: 18px;
}
.split-desc {
  font-size: 14px;
  line-height: 1.8;
  color: #6b7280;
  margin-bottom: 16px;
}
.split-desc--muted { color: #9ca3af; margin-bottom: 0; }

.badge-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 18px;
}
.badge-chip {
  position: relative;
  overflow: hidden;
  font-size: 11px;
  font-family: 'JetBrains Mono', monospace;
  font-weight: 600;
  padding: 5px 10px;
  border-radius: 6px;
  letter-spacing: 0.2px;
  transition: border-color 0.2s, background 0.2s, transform 0.2s;
}
.badge-chip--blue {
  color: var(--c-blue);
  background: rgba(61,108,232,0.08);
  border: 1px solid rgba(61,108,232,0.2);
}
.badge-chip--amber {
  color: #b56b1a;
  background: rgba(232,151,61,0.12);
  border: 1px solid rgba(232,151,61,0.28);
}
.badge-chip::before {
  content: '';
  position: absolute; top: 0; left: -60%;
  width: 40%; height: 100%;
  background: linear-gradient(120deg, transparent, rgba(255,255,255,0.6), transparent);
  transform: skewX(-20deg);
  transition: left 0.5s ease;
}
.badge-chip:hover { transform: translateY(-1px); }
.badge-chip--blue:hover  { border-color: rgba(61,108,232,0.45); background: rgba(61,108,232,0.13); }
.badge-chip--amber:hover { border-color: rgba(232,151,61,0.5);  background: rgba(232,151,61,0.18); }
.badge-chip:hover::before { left: 130%; }

.big-stat {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 24px;
  padding: 18px 22px;
  background: #fff;
  border: 1px solid #e8eaee;
  border-radius: 12px;
  width: fit-content;
  min-width: 240px;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.big-stat:hover {
  border-color: rgba(232,151,61,0.35);
  box-shadow: 0 8px 28px rgba(232,151,61,0.1);
}
.big-stat-num {
  font-size: 34px;
  font-weight: 800;
  letter-spacing: -1px;
  background: linear-gradient(120deg, var(--c-amber), var(--c-green));
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  font-family: 'JetBrains Mono', monospace;
  line-height: 1;
  font-variant-numeric: tabular-nums;
}
.big-stat-label { font-size: 11px; color: #9ca3af; font-weight: 600; }
.big-stat-bar {
  width: 100%; height: 3px;
  background: #e8eaee; border-radius: 2px; overflow: hidden;
  margin-top: 2px;
}
.big-stat-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--c-amber), var(--c-green));
  border-radius: 2px;
  transition: width 1.1s cubic-bezier(0.16,1,0.3,1);
}

/* ---------- блоки изображений ---------- */
.media-tall {
  position: relative;
  width: 100%;
  aspect-ratio: 3 / 4;
  border: 1px solid #e8eaee;
  border-radius: 14px;
  overflow: hidden;
  background: #fff;
  will-change: transform;
}
.media-photo {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
.media-tall--square {
  aspect-ratio: 16 / 9;
}
.media-tall--large {
  max-width: 900px;
}
.media-tall--wide {
  aspect-ratio: 16 / 9;
  transform-origin: center;
}
.media-tall--wide-narrow {
  aspect-ratio: 4 / 3;
}

.media-tall--in-grid { align-self: start; }
.media-placeholder {
  width: 100%; height: 100%;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  gap: 8px; color: #c5c9d4;
  font-size: 11px; font-family: 'JetBrains Mono', monospace;
  background:
    repeating-linear-gradient(45deg, transparent 0px, transparent 12px, rgba(0,0,0,0.018) 12px, rgba(0,0,0,0.018) 24px),
    #f6f7f9;
}
.media-hint { font-size: 9px; color: #d1d5db; letter-spacing: 0.3px; }

/* ---------- список индексов ---------- */
.workspace-grid {
  position: relative; z-index: 1;
  display: grid;
  grid-template-columns: 0.6fr 0.8fr;
  gap: 50px;
  align-items: start;
}
.index-list {
  border: 1px solid #e8eaee;
  border-radius: 14px;
  overflow: hidden;
  background: #fff;
}
.index-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 20px;
  border-bottom: 1px solid #f0f1f3;
  transition: background 0.2s, transform 0.2s, padding-left 0.2s;
}
.index-item:hover { background: #fafbfc; transform: translateX(3px); }
.index-icon {
  display: flex; align-items: center; justify-content: center;
  width: 32px; height: 32px; border-radius: 8px;
  flex-shrink: 0;
  transition: background 0.2s, color 0.2s, transform 0.3s;
}
.index-item--blue  .index-icon { background: rgba(61,108,232,0.09);  color: var(--c-blue); }
.index-item--amber .index-icon { background: rgba(232,151,61,0.12); color: #b56b1a; }
.index-item--green .index-icon { background: rgba(107,181,106,0.12); color: #4c8a4a; }
.index-item--blue:hover  .index-icon { background: var(--c-blue);  color: #fff; transform: scale(1.08) rotate(-4deg); }
.index-item--amber:hover .index-icon { background: var(--c-amber); color: #fff; transform: scale(1.08) rotate(-4deg); }
.index-item--green:hover .index-icon { background: var(--c-green); color: #fff; transform: scale(1.08) rotate(-4deg); }
.index-info { display: flex; flex-direction: column; gap: 2px; flex: 1; }
.index-name {
  font-size: 13px; font-weight: 700;
  font-family: 'JetBrains Mono', monospace;
  color: #1a1d23; letter-spacing: 0.3px;
}
.index-desc { font-size: 12px; color: #9ca3af; }
.index-arrow {
  color: #d1d5db;
  display: flex;
  opacity: 0;
  transform: translateX(-4px);
  transition: opacity 0.2s, transform 0.2s, color 0.2s;
}
.index-item:hover .index-arrow { opacity: 1; transform: translateX(0); color: var(--c-blue); }

.index-item-wrap {
  border-bottom: 1px solid #f0f1f3;
}
.index-item-wrap:last-of-type { border-bottom: none; }

/* index-item теперь кнопка, сбрасываем нативные стили */
.index-item {
  width: 100%;
  border: none;
  background: none;
  font: inherit;
  text-align: left;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 20px;
  transition: background 0.2s, transform 0.2s;
}
.index-item:hover { background: #fafbfc; transform: translateX(3px); }

.index-arrow--toggle {
  transition: opacity 0.2s, transform 0.3s, color 0.2s;
}
.index-item--open .index-arrow--toggle {
  opacity: 1;
  color: var(--c-blue);
  transform: rotate(90deg);
}

.index-detail {
  padding: 4px 20px 18px 64px;
  background: #fafbfc;
}
.index-detail-text {
  font-size: 12.5px;
  line-height: 1.75;
  color: #6b7280;
  margin-bottom: 10px;
}
.index-detail-wave {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  font-family: 'JetBrains Mono', monospace;
  font-weight: 600;
  color: var(--c-blue);
  background: rgba(61,108,232,0.08);
  padding: 4px 10px;
  border-radius: 6px;
}

.index-detail-enter-active,
.index-detail-leave-active {
  transition: all 0.25s ease;
  overflow: hidden;
}
.index-detail-enter-from,
.index-detail-leave-to {
  opacity: 0;
  max-height: 0;
  padding-top: 0;
  padding-bottom: 0;
}
.index-detail-enter-to,
.index-detail-leave-from {
  opacity: 1;
  max-height: 200px;
}

.flow-note {
  padding: 18px 20px;
  border-bottom: 1px solid #f0f1f3;
  background: #fafbfc;
}
.flow-note-line {
  width: 28px; height: 2px;
  background: linear-gradient(90deg, var(--c-blue), var(--c-amber));
  border-radius: 2px; margin-bottom: 10px;
}
.flow-note p { font-size: 12.5px; line-height: 1.75; color: #6b7280; }

.export-note {
  display: flex; align-items: center; gap: 8px;
  padding: 14px 20px;
  font-size: 12px; color: var(--c-blue); font-weight: 600;
}
.export-note svg { flex-shrink: 0; animation: bob 2.6s ease-in-out infinite; }
@keyframes bob {
  0%, 100% { transform: translateY(0); }
  50%       { transform: translateY(-2px); }
}

/* ---------- аудитория ---------- */
.audience-section {
  max-width: 1200px; margin: 0 auto;
  padding: 56px 48px 96px;
}
.audience-grid {
  position: relative; z-index: 1;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}
.audience-card {
  display: flex; flex-direction: column; gap: 10px;
  padding: 24px;
  border: 1px solid #e8eaee;
  border-radius: 14px;
  background: #fafbfc;
  transition: border-color 0.25s, background 0.25s, transform 0.25s, box-shadow 0.25s;
}
.audience-card--blue:hover {
  border-color: rgba(61,108,232,0.35);
  background: #fff;
  transform: translateY(-3px);
  box-shadow: 0 14px 32px rgba(61,108,232,0.1);
}
.audience-card--green:hover {
  border-color: rgba(107,181,106,0.4);
  background: #fff;
  transform: translateY(-3px);
  box-shadow: 0 14px 32px rgba(107,181,106,0.12);
}
.audience-icon {
  display: flex; align-items: center; justify-content: center;
  width: 38px; height: 38px; border-radius: 9px;
  transition: transform 0.3s cubic-bezier(0.16,1,0.3,1), background 0.25s, color 0.25s;
}
.audience-card--blue  .audience-icon { background: rgba(61,108,232,0.09);  color: var(--c-blue); }
.audience-card--green .audience-icon { background: rgba(107,181,106,0.12); color: #4c8a4a; }
.audience-card--blue:hover  .audience-icon { background: var(--c-blue);  color: #fff; transform: rotate(-8deg) scale(1.08); }
.audience-card--green:hover .audience-icon { background: var(--c-green); color: #fff; transform: rotate(-8deg) scale(1.08); }
.audience-title { font-size: 14px; font-weight: 700; color: #0d0f14; }
.audience-desc { font-size: 12.5px; line-height: 1.7; color: #9ca3af; }

/* ---------- адаптивность ---------- */
@media (max-width: 960px) {
  .hero-inner       { padding: 0 24px; }
  .tool-section     { padding: 48px 24px 24px; }
  .audience-section { padding: 48px 24px 72px; }
  .footnote         { padding: 0 24px 8px; }
  .spectral-svg     { width: 80%; right: -30%; opacity: 0.6; }
  .section-bg-word  { font-size: 120px; }

  .split-inner,
  .split-inner--rev,
  .split-inner--photo-left {
    grid-template-columns: 1fr;
    gap: 32px;
    padding: 48px 24px;
  }
  .split-inner--rev .split-media { order: 2; }
  .split-inner--rev .split-text  { order: 1; }
  .media-tall { aspect-ratio: 16 / 9; }

  .workspace-grid { grid-template-columns: 1fr; }
  .audience-grid  { grid-template-columns: 1fr; }
}

/* ---------- уменьшение анимации ---------- */
@media (prefers-reduced-motion: reduce) {
  .reveal { opacity: 1; transform: none; transition: none; }
  .dot, .spectral-path, .spectral-scan, .media-tall:hover .media-scan,
  .export-note svg, .scroll-rail-fill, .big-stat-bar-fill { animation: none !important; }
  .index-item, .audience-card, .media-tall { transition: none !important; }
}
</style>