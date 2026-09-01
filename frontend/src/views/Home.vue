<template>
  <div class="page">
    <section class="hero">
      <div class="hero-inner">
        <div class="hero-text">
          <div class="hero-eyebrow">
            <span class="dot"></span>
            Дистанционное зондирование
          </div>
          <h1 class="hero-title">
            Анализ<br/>
            сельскохозяйственных<br/>
            <em>угодий</em>
          </h1>
          <p class="hero-desc">
            Мы разрабатываем систему анализа состояния посевов пшеницы на основе мультиспектральных и гиперспектральных снимков. Решение позволяет оценивать состояние растений по вегетационным индексам, выявлять стресс-зоны и формировать рекомендации по дифференцированному внесению азотных удобрений.
          </p>
          <p class="hero-desc">
            Наши алгоритмы работают с данными спутников и БПЛА, позволяя агрономам и аналитикам принимать решения на основе актуальных данных о состоянии полей.
          </p>
          <div class="hero-stats">
            <div class="stat">
              <span class="stat-num">3</span>
              <span class="stat-label">Метода анализа</span>
            </div>
            <div class="stat-div"></div>
            <div class="stat">
              <span class="stat-num">High</span>
              <span class="stat-label">Точность</span>
            </div>
            <div class="stat-div"></div>
            <div class="stat">
              <span class="stat-num">Real-Time</span>
              <span class="stat-label">Обработка</span>
            </div>
          </div>
        </div>

        <div class="hero-gallery">
          <p class="gallery-label">Примеры сегментации полей</p>
          <div class="gallery-grid">
            <div
              v-for="(card, i) in galleryCards"
              :key="i"
              class="gallery-card"
              @mousemove="onCardMove($event, i)"
              @mouseleave="onCardLeave(i)"
              :style="cardStyles[i]"
            >
              <div class="gallery-card-img">
                <div class="img-placeholder">
                  <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
                  <span>Фото {{ i + 1 }}</span>
                </div>
              </div>
              <div class="gallery-card-info">
                <span class="gallery-card-title">{{ card.title }}</span>
                <span class="gallery-card-badge">{{ card.method }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="tool-section">
      <div class="tool-header">
        <h2 class="tool-title">Инструмент анализа</h2>
        <p class="tool-subtitle">Введите координаты или загрузите снимок — получите карту сегментации</p>
      </div>

      <div class="workspace">
        <div class="panel panel-left">
          <div class="panel-header">
            <span class="panel-label">ПАРАМЕТРЫ</span>
          </div>

          <div class="mode-toggle">
            <button :class="['mode-btn', inputMode === 'coords' ? 'mode-btn--active' : '']" @click="inputMode = 'coords'">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3"/></svg>
              Координаты
            </button>
            <button :class="['mode-btn', inputMode === 'file' ? 'mode-btn--active' : '']" @click="inputMode = 'file'">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
              Файл
            </button>
          </div>

          <Transition name="slide-fade" mode="out-in">
            <div v-if="inputMode === 'coords'" key="coords" class="input-section">
              <div class="coord-group">
                <div class="coord-group-label">
                  <span class="coord-corner-icon coord-corner-icon--bl">
                    <svg width="10" height="10" viewBox="0 0 10 10" fill="none"><path d="M1 1v8h8" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
                  </span>
                  Левый нижний
                </div>
                <div class="coord-row">
                  <div class="field field--half">
                    <label class="field-label">Широта</label>
                    <input v-model="coordLat1" type="number" step="0.000001" placeholder="55.000000" class="field-input" @keypress.enter="runAnalysis" />
                  </div>
                  <div class="field field--half">
                    <label class="field-label">Долгота</label>
                    <input v-model="coordLon1" type="number" step="0.000001" placeholder="37.000000" class="field-input" @keypress.enter="runAnalysis" />
                  </div>
                </div>
              </div>

              <div class="coord-connector">
                <div class="coord-connector-line"></div>
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="3" width="18" height="18" rx="2"/></svg>
                <div class="coord-connector-line"></div>
              </div>

              <div class="coord-group">
                <div class="coord-group-label">
                  <span class="coord-corner-icon coord-corner-icon--tr">
                    <svg width="10" height="10" viewBox="0 0 10 10" fill="none"><path d="M9 9V1H1" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
                  </span>
                  Правый верхний
                </div>
                <div class="coord-row">
                  <div class="field field--half">
                    <label class="field-label">Широта</label>
                    <input v-model="coordLat2" type="number" step="0.000001" placeholder="55.100000" class="field-input" @keypress.enter="runAnalysis" />
                  </div>
                  <div class="field field--half">
                    <label class="field-label">Долгота</label>
                    <input v-model="coordLon2" type="number" step="0.000001" placeholder="37.100000" class="field-input" @keypress.enter="runAnalysis" />
                  </div>
                </div>
              </div>

              <div class="section-sep"><span>Дата снимка</span></div>
              <div class="date-block">
                <div class="date-row">
                  <div class="field field--date-sm">
                    <label class="field-label">День</label>
                    <input
                      v-model.number="snapDay"
                      type="number" min="1" max="31"
                      placeholder="01"
                      :class="['field-input', dateError && !snapDay ? 'field-input--error' : '']"
                    />
                  </div>
                  <div class="field field--date-sm">
                    <label class="field-label">Месяц</label>
                    <input
                      v-model.number="snapMonth"
                      type="number" min="1" max="12"
                      placeholder="06"
                      :class="['field-input', dateError && !snapMonth ? 'field-input--error' : '']"
                    />
                  </div>
                  <div class="field field--date-md">
                    <label class="field-label">Год</label>
                    <input
                      v-model.number="snapYear"
                      type="number" min="2000" max="2100"
                      placeholder="2024"
                      :class="['field-input', dateError && !snapYear ? 'field-input--error' : '']"
                    />
                  </div>
                </div>
                <span v-if="dateError" class="band-error">{{ dateError }}</span>
                <span v-else-if="snapDay && snapMonth && snapYear" class="date-preview">
                  {{ formatDate(snapDay, snapMonth, snapYear) }}
                </span>
              </div>

              <div class="section-sep"><span>Фаза роста</span></div>
              <div class="growth-list">
                <div
                  v-for="g in growthStages"
                  :key="g.id"
                  :class="['formula-item', coordSelectedGrowth === g.id ? 'formula-item--active' : '']"
                  @click="coordSelectedGrowth = g.id"
                >
                  <div class="formula-radio">
                    <div v-if="coordSelectedGrowth === g.id" class="formula-radio-dot"></div>
                  </div>
                  <div class="growth-info">
                    <span class="formula-name">{{ g.label }}</span>
                    <span class="growth-sub">{{ g.sub }}</span>
                  </div>
                </div>
              </div>

              <div class="section-sep"><span>Сегментация</span></div>
              <div class="seg-block">
                <div class="seg-header">
                  <span class="seg-label">Число сегментов разделения поля</span>
                  <span class="seg-val">{{ coordSegmentationLevel }}</span>
                </div>
                <div class="seg-track-wrap">
                  <input type="range" min="3" max="5" step="1" v-model.number="coordSegmentationLevel" class="seg-range" />
                  <div class="seg-ticks">
                    <span v-for="n in [3,4,5]" :key="n" :class="['seg-tick', coordSegmentationLevel === n ? 'seg-tick--active' : '']">{{ n }}</span>
                  </div>
                </div>
                <p class="seg-hint">{{ segHints[coordSegmentationLevel] }}</p>
              </div>
            </div>

            <div v-else key="file" class="input-section">
              <div
                :class="['dropzone', dragOver ? 'dropzone--active' : '', uploadedFile ? 'dropzone--filled' : '']"
                @dragover.prevent="dragOver = true"
                @dragleave="dragOver = false"
                @drop.prevent="handleDrop"
                @click="$refs.fileInput.click()"
              >
                <input ref="fileInput" type="file" accept=".tif,.tiff" style="display:none" @change="handleFileChange" />
                <template v-if="!uploadedFile">
                  <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="dz-icon"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
                  <span class="dz-text">Перетащите или нажмите</span>
                  <span class="dz-hint">GeoTIFF (.tif / .tiff)</span>
                </template>
                <template v-else>
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="dz-icon dz-icon--ok"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
                  <span class="dz-text dz-text--name">{{ uploadedFile.name }}</span>
                  <span class="dz-hint">{{ formatSize(uploadedFile.size) }} · нажмите чтобы заменить</span>
                </template>
              </div>

              <div class="section-sep"><span>Фаза роста</span></div>
              <div class="growth-list">
                <div
                  v-for="g in growthStages"
                  :key="g.id"
                  :class="['formula-item', fileSelectedGrowth === g.id ? 'formula-item--active' : '']"
                  @click="fileSelectedGrowth = g.id"
                >
                  <div class="formula-radio">
                    <div v-if="fileSelectedGrowth === g.id" class="formula-radio-dot"></div>
                  </div>
                  <div class="growth-info">
                    <span class="formula-name">{{ g.label }}</span>
                    <span class="growth-sub">{{ g.sub }}</span>
                  </div>
                </div>
              </div>

              <div class="section-sep"><span>Разрешение снимка</span></div>
              <div class="resolution-block">
                <div class="band-field-head">
                  <label class="field-label">Размер пикселя (см)</label>
                  <div class="tip-wrap" @mouseenter="activeTooltip = 'resolution'" @mouseleave="activeTooltip = null">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/>
                      <line x1="12" y1="8" x2="12.01" y2="8"/>
                    </svg>
                    <Transition name="tip">
                      <div v-if="activeTooltip === 'resolution'" class="tip-box tip-box--band">
                        Пространственное разрешение снимка — размер одного пикселя в сантиметрах. Например, 3.56 означает, что каждый пиксель соответствует 3,56 × 3,56 см на местности.
                      </div>
                    </Transition>
                  </div>
                </div>
                <input
                  v-model.number="resolution"
                  type="number"
                  min="0.01"
                  step="0.01"
                  placeholder="например, 3.56"
                  :class="['field-input', resolutionError ? 'field-input--error' : '']"
                />
                <span v-if="resolutionError" class="band-error">{{ resolutionError }}</span>
              </div>

              <div class="section-sep"><span>Спектральные каналы</span></div>
              <div class="bands-grid">
                <div v-for="b in bandFields" :key="b.key" class="band-field">
                  <div class="band-field-head">
                    <label class="field-label">{{ b.label }}</label>
                    <div class="tip-wrap" @mouseenter="activeTooltip = b.key" @mouseleave="activeTooltip = null">
                      <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/>
                        <line x1="12" y1="8" x2="12.01" y2="8"/>
                      </svg>
                      <Transition name="tip">
                        <div v-if="activeTooltip === b.key" class="tip-box tip-box--band">{{ b.hint }}</div>
                      </Transition>
                    </div>
                  </div>
                  <input
                    v-model.number="bands[b.key]"
                    type="number"
                    min="1"
                    :placeholder="b.placeholder"
                    :class="['field-input', bandErrors[b.key] ? 'field-input--error' : '']"
                  />
                  <span v-if="bandErrors[b.key]" class="band-error">{{ bandErrors[b.key] }}</span>
                </div>
              </div>

              <div class="section-sep"><span>Сегментация</span></div>
              <div class="seg-block">
                <div class="seg-header">
                  <span class="seg-label">Число сегментов разделения поля</span>
                  <span class="seg-val">{{ fileSegmentationLevel }}</span>
                </div>
                <div class="seg-track-wrap">
                  <input type="range" min="3" max="5" step="1" v-model.number="fileSegmentationLevel" class="seg-range" />
                  <div class="seg-ticks">
                    <span v-for="n in [3,4,5]" :key="n" :class="['seg-tick', fileSegmentationLevel === n ? 'seg-tick--active' : '']">{{ n }}</span>
                  </div>
                </div>
                <p class="seg-hint">{{ segHints[fileSegmentationLevel] }}</p>
              </div>
            </div>
          </Transition>

          <div class="section-sep"><span>Метод анализа</span></div>

          <div class="formula-list">
            <div
              v-for="f in availableFormulas"
              :key="f.id"
              :class="['formula-item', selectedFormula === f.id ? 'formula-item--active' : '']"
              @click="selectedFormula = f.id"
            >
              <div class="formula-radio">
                <div v-if="selectedFormula === f.id" class="formula-radio-dot"></div>
              </div>
              <span class="formula-name">{{ f.name }}</span>

              <div class="tip-wrap" @mouseenter="activeTooltip = f.id" @mouseleave="activeTooltip = null">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
                <Transition name="tip">
                  <div v-if="activeTooltip === f.id" class="tip-box">{{ f.description }}</div>
                </Transition>
              </div>
            </div>
          </div>

          <Transition name="slide-fade">
            <div v-if="validationError" class="validation-error">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/>
                <line x1="12" y1="16" x2="12.01" y2="16"/>
              </svg>
              {{ validationError }}
            </div>
          </Transition>

          <button class="run-btn" :disabled="isLoading || !selectedFormula" @click="runAnalysis">
            <template v-if="isLoading">
              <span class="spinner"></span>Обработка...
            </template>
            <template v-else>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="5 3 19 12 5 21 5 3"/></svg>
              Запустить анализ
            </template>
          </button>
        </div>

        <div class="panel panel-right">
          <div class="panel-header">
            <span class="panel-label">РЕЗУЛЬТАТ СЕГМЕНТАЦИИ</span>
            <button v-if="resultImage && resultArchiveUrl" class="export-btn export-btn--tif" @click="exportResult">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
              Скачать результат
            </button>
          </div>

          <div class="result-area">
            <Transition name="res-fade" mode="out-in">
              <div v-if="!resultImage && !isLoading" key="empty" class="empty-state">
                <div class="empty-dots">
                  <span v-for="n in 9" :key="n" class="empty-dot"></span>
                </div>
                <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
                <p class="empty-text">Результат отобразится здесь</p>
                <p class="empty-hint">Задайте параметры и запустите анализ</p>
              </div>

              <div v-else-if="isLoading" key="loading" class="loading-state">
                <div class="scan-line-wrap"><div class="scan-line"></div></div>
                <p class="loading-text">{{ stageLabel }}</p>
                <div class="progress-bar">
                  <div
                    class="progress-fill"
                    :class="{ 'progress-fill--det': uploadStage === 'uploading' }"
                    :style="uploadStage === 'uploading'
                      ? { width: uploadProgress + '%', marginLeft: '0' }
                      : {}"
                  ></div>
                </div>
                <span v-if="uploadStage === 'uploading'" class="progress-pct">
                  {{ uploadProgress }}&thinsp;%
                </span>
              </div>

              <div v-else key="result" class="result-content">
                <div class="result-img-wrap">
                  <img :src="resultImage" alt="Результат сегментации" class="result-img" />
                  <div class="result-badge-wrap">
                    <span class="result-badge">{{ getFormulaName(resultMeta.formula) }}</span>
                  </div>
                </div>

                <Transition name="slide-fade">
                  <div v-if="nitrogenZones && nitrogenZones.length" class="nitrogen-panel">
                    <div class="nitrogen-header">
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M12 2C8 2 4 6 4 10c0 5 8 12 8 12s8-7 8-12c0-4-4-8-8-8z"/>
                        <circle cx="12" cy="10" r="2.5"/>
                      </svg>
                      <span class="nitrogen-title">Вносимое количество азота</span>
                    </div>
                    <div class="nitrogen-zones">
                      <div
                        v-for="(zone, idx) in nitrogenZones"
                        :key="idx"
                        class="nitrogen-zone"
                      >
                        <div class="zone-color-bar">
                          <div class="zone-swatch" :style="{ background: zone.color }"></div>
                          <div class="zone-pulse" :style="{ background: zone.color }"></div>
                        </div>
                        <div class="zone-info">
                          <span class="zone-label">{{ zone.label }}</span>
                          <span class="zone-desc">класс {{ zone.classIdx }} в TIFF файле</span>
                        </div>
                        <div class="zone-amount-wrap">
                          <span class="zone-amount">{{ zone.nitrogen }}</span>
                          <span class="zone-unit">кг/га</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </Transition>

                <div class="result-meta">
                  <div class="meta-grid">
                    <div class="meta-item meta-item--method">
                      <span class="meta-label">Метод</span>
                      <div class="meta-method">
                        <span class="meta-method-icon" v-html="getFormulaIcon(resultMeta.formula)"></span>
                        <span class="meta-val">{{ getFormulaName(resultMeta.formula) }}</span>
                      </div>
                    </div>
                    <div class="meta-item" v-if="resultMeta.area">
                      <span class="meta-label">Область</span>
                      <span class="meta-val">{{ resultMeta.area }}</span>
                    </div>
                    <div class="meta-item" v-if="resultMeta.date">
                      <span class="meta-label">Дата снимка</span>
                      <span class="meta-val">{{ resultMeta.date }}</span>
                    </div>
                    <div class="meta-item" v-if="resultMeta.file">
                      <span class="meta-label">Источник</span>
                      <span class="meta-val">{{ resultMeta.file }}</span>
                    </div>
                    <div class="meta-item">
                      <span class="meta-label">Обработано</span>
                      <span class="meta-val">{{ resultMeta.timestamp }}</span>
                    </div>
                  </div>
                  <p class="result-desc">{{ resultMeta.description }}</p>
                </div>
              </div>
            </Transition>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import api from '@/api/http'
import { uploadFile } from '@/utils/uploadFile'

const galleryCards = [
  { title: '', method: '' },
  { title: '',    method: '' },
  { title: '',   method: '' },
  { title: '',   method: '' }
]
const cardStyles = reactive(galleryCards.map(() => ({
  transform: 'perspective(700px) rotateX(0deg) rotateY(0deg) scale(1)',
  transition: 'transform 0.4s cubic-bezier(0.16,1,0.3,1)',
})))
const onCardMove = (e, i) => {
  const el = e.currentTarget, rect = el.getBoundingClientRect()
  const dx = (e.clientX - rect.left - rect.width  / 2) / (rect.width  / 2)
  const dy = (e.clientY - rect.top  - rect.height / 2) / (rect.height / 2)
  cardStyles[i] = {
    transform:  `perspective(700px) rotateX(${-dy * 8}deg) rotateY(${dx * 8}deg) scale(1.04)`,
    transition: 'transform 0.08s ease',
    boxShadow:  '0 16px 48px rgba(61,108,232,0.14)',
  }
}
const onCardLeave = (i) => {
  cardStyles[i] = {
    transform:  'perspective(700px) rotateX(0deg) rotateY(0deg) scale(1)',
    transition: 'transform 0.5s cubic-bezier(0.16,1,0.3,1)',
    boxShadow:  '',
  }
}

const inputMode    = ref('coords')
const uploadedFile = ref(null)
const dragOver     = ref(false)
const activeTooltip = ref(null)
const validationError = ref('')

const coordLat1 = ref('')
const coordLon1 = ref('')
const coordLat2 = ref('')
const coordLon2 = ref('')

const snapDay   = ref(null)
const snapMonth = ref(null)
const snapYear  = ref(null)
const dateError = ref('')

const formatDate = (d, m, y) => {
  const months = ['января','февраля','марта','апреля','мая','июня',
                  'июля','августа','сентября','октября','ноября','декабря']
  return `${d} ${months[m - 1]} ${y} г.`
}

const resolution      = ref(null)
const resolutionError = ref('')

const selectedFormula = ref(null)

const coordSelectedGrowth = ref(null)
const fileSelectedGrowth  = ref(null)

const selectedGrowth = computed(() =>
  inputMode.value === 'coords' ? coordSelectedGrowth.value : fileSelectedGrowth.value
)

const growthStages = [
  { id: 'tillering', label: 'Кущение',  sub: 'Ранняя вегетация, формирование побегов' },
  { id: 'booting',   label: 'В трубку', sub: 'Активный рост стебля' },
]

const bands = reactive({ nir: null, red: null, red_edge: null, blue: null, b1: null, b2: null })

const bandFields = [
  {
    key: 'nir',
    label: 'NIR',
    placeholder: '175',
    hint: 'Ближний инфракрасный диапазон (NIR, ~740–1300 нм).'
  },
  {
    key: 'red_edge',
    label: 'Red Edge',
    placeholder: '152',
    hint: 'Диапазон красного края (Red Edge, ~700–740 нм).'
  },
  {
    key: 'red',
    label: 'Red',
    placeholder: '140',
    hint: 'Красный диапазон (Red, ~600–700 нм).'
  },
  {
    key: 'blue',
    label: 'Blue',
    placeholder: '29',
    hint: 'Синий диапазон (Blue, ~380–450 нм).'
  },
  {
    key: 'b1',
    label: 'B1',
    placeholder: '88',
    hint: 'Дополнительный спектральный канал, используемый при расчете PRI_mod (~570 нм).'
  },
  {
    key: 'b2',
    label: 'B2',
    placeholder: '70',
    hint: 'Дополнительный спектральный канал, применяемый совместно с B1 для анализа состояния растительности (~531 нм).'
  },
]

const algorithmBands = { ChlRI: ['nir', 'red_edge', 'blue'], NDVI: ['nir', 'red'], RPImod: ['b1', 'b2'] }
const bandErrors = reactive({ nir: '', red: '', red_edge: '', blue: '', b1: '', b2: '' })

const clearBandErrors = () => { Object.keys(bandErrors).forEach(k => { bandErrors[k] = '' }) }

const coordSegmentationLevel = ref(3)
const fileSegmentationLevel  = ref(3)

const segmentationLevel = computed(() =>
  inputMode.value === 'coords' ? coordSegmentationLevel.value : fileSegmentationLevel.value
)

const segHints = {
  3: 'Крупное деление — 3 зоны',
  4: 'Среднее деление — 4 зоны',
  5: 'Точное деление — 5 зон',
}

const formulas = [
  {
    id: 'ChlRI',
    name: 'ChlRI',
    description: 'Chlorophyll Reflectance Index: (NIR − RedEdge) / (NIR + RedEdge − 2×Blue). Каналы: NIR, RedEdge, Blue.',
    icon: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22C6 22 2 16 2 10c0 0 4-6 10-6s10 6 10 6c0 6-4 12-10 12z"/><line x1="12" y1="22" x2="12" y2="10"/></svg>`,
  },
  {
    id: 'NDVI',
    name: 'NDVI',
    description: 'Normalized Difference Vegetation Index: (NIR − Red) / (NIR + Red). Каналы: NIR, Red.',
    icon: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M2 8 Q6 4 10 8 Q14 12 18 8 Q20 6 22 8"/><path d="M2 16 Q6 12 10 16 Q14 20 18 16 Q20 14 22 16"/></svg>`,
  },
  {
    id: 'RPImod',
    name: 'RPImod',
    description: 'Modified Red-edge Position Index: c1 − (B1 − B2) / (B1 + B2). Каналы: B1, B2, c1 = 0.5.',
    icon: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>`,
  },
]

const availableFormulas = computed(() =>
  inputMode.value === 'coords'
    ? formulas.filter(f => f.id !== 'RPImod')
    : formulas
)

const getFormulaName = (id) => formulas.find(f => f.id === id)?.name ?? id
const getFormulaIcon = (id) => formulas.find(f => f.id === id)?.icon ?? ''

const isLoading      = ref(false)
const uploadProgress = ref(0)
const uploadStage    = ref('')

const stageLabel = computed(() => ({
  uploading:  'Загрузка файла на сервер...',
  merging:    'Объединение фрагментов...',
  processing: 'Сегментация изображения...',
  done:       'Почти готово...',
}[uploadStage.value] ?? 'Обработка...'))

const resultImage  = ref(null)
const resultArchiveUrl = ref(null)

const nitrogenZones = ref(null)
const resultMeta = reactive({
  formula: null,
  mode: null,
  area: null,
  date: null,
  file: null,
  timestamp: '',
  description: '',
})

const ZONE_LABELS = [
  'Критическая зона',
  'Зона стресса',
  'Умеренная зона',
  'Удовлетворительная зона',
  'Оптимальная зона',
]

const buildNitrogenZones = (json) => {
  return Object.entries(json).map(([classIdx, zone], idx) => ({
    color: zone.color,
    nitrogen: zone.value,
    label: ZONE_LABELS[idx] ?? `Зона ${idx + 1}`,
    classIdx: Number(classIdx),
  }))
}

const formatSize = (b) =>
  b < 1_048_576
    ? (b / 1024).toFixed(1) + ' КБ'
    : (b / 1_048_576).toFixed(1) + ' МБ'

const handleDrop = (e) => {
  dragOver.value = false
  const f = e.dataTransfer.files[0]
  if (!f) return
  const name = f.name.toLowerCase()
  if (!name.endsWith('.tif') && !name.endsWith('.tiff')) return
  uploadedFile.value = f
}
const handleFileChange = (e) => {
  const f = e.target.files[0]
  if (f) uploadedFile.value = f
}

const validateCoords = () => {
  if (!coordLat1.value || !coordLon1.value || !coordLat2.value || !coordLon2.value) {
    validationError.value = 'Заполните все поля координат'
    return false
  }
  dateError.value = ''
  if (!snapDay.value || !snapMonth.value || !snapYear.value) {
    dateError.value = 'Укажите полную дату снимка'
    validationError.value = 'Укажите дату снимка (день, месяц, год)'
    return false
  }
  if (snapDay.value < 1 || snapDay.value > 31) {
    dateError.value = 'День: от 1 до 31'
    validationError.value = 'Некорректный день в дате снимка'
    return false
  }
  if (snapMonth.value < 1 || snapMonth.value > 12) {
    dateError.value = 'Месяц: от 1 до 12'
    validationError.value = 'Некорректный месяц в дате снимка'
    return false
  }
  return true
}

const validateFile = () => {
  if (!uploadedFile.value) {
    validationError.value = 'Загрузите файл GeoTIFF'
    return false
  }
  if (!resolution.value || isNaN(resolution.value) || resolution.value <= 0) {
    resolutionError.value = 'Укажите разрешение снимка (> 0 см)'
    validationError.value = 'Разрешение снимка не было указано'
    return false
  }
  clearBandErrors()
  const required = algorithmBands[selectedFormula.value] ?? []
  let hasError = false
  for (const key of required) {
    const val = bands[key]
    if (val === null || val === undefined || val === '' || isNaN(val)) {
      bandErrors[key] = 'Обязательный канал для ' + selectedFormula.value
      hasError = true
    } else if (val < 1) {
      bandErrors[key] = 'Номер канала должен быть ≥ 1'
      hasError = true
    }
  }
  if (hasError) {
    const names = required
      .filter(k => !bands[k])
      .map(k => bandFields.find(f => f.key === k)?.label ?? k)
      .join(', ')
    validationError.value = `Для алгоритма ${selectedFormula.value} необходимо указать: ${names}`
    return false
  }
  return true
}

const validate = () => {
  validationError.value = ''
  resolutionError.value = ''
  dateError.value = ''

  if (!selectedFormula.value) {
    validationError.value = 'Выберите метод анализа'
    return false
  }
  if (!selectedGrowth.value) {
    validationError.value = 'Выберите фазу роста'
    return false
  }
  if (inputMode.value === 'coords') return validateCoords()
  return validateFile()
}

const runAnalysis = async () => {
  if (!validate()) return

  try {
    await api.post('/auth/validate')
  } catch {
    return
  }

  isLoading.value      = true
  uploadProgress.value = 0
  uploadStage.value    = ''
  resultImage.value    = null
  resultArchiveUrl.value   = null
  nitrogenZones.value  = null

  const processPayload = {
    algorithm:          selectedFormula.value,
    growth_stage:       selectedGrowth.value,
    segmentation_level: segmentationLevel.value,
  }

  try {
    let imageUrl, archiveUrl, fertUrl, uploadId

    if (inputMode.value === 'file' && uploadedFile.value) {
      const filePayload = {
        ...processPayload,
        resolution: resolution.value,
        bands: { nir: bands.nir, red: bands.red, red_edge: bands.red_edge, blue: bands.blue, b1: bands.b1, b2: bands.b2 },
      }
      ;({ imageUrl, archiveUrl, fertUrl, uploadId } = await uploadFile(
        uploadedFile.value,
        selectedFormula.value,
        filePayload,
        {
          onProgress: (pct)   => { uploadProgress.value = pct },
          onStage:    (stage) => { uploadStage.value    = stage },
        }
      ))
      uploadStage.value = 'done'
    } else {
      uploadStage.value = 'processing'
      const { data } = await api.post('/calculator', {
        lat1:      coordLat1.value,
        lon1:      coordLon1.value,
        lat2:      coordLat2.value,
        lon2:      coordLon2.value,
        snap_date: `${snapYear.value}-${String(snapMonth.value).padStart(2,'0')}-${String(snapDay.value).padStart(2,'0')}`,
        ...processPayload,
      })
      imageUrl = data.image_url
      archiveUrl = data.archive_url
      uploadId = data.upload_id
      fertUrl = data.fert_url
    }

    const imageResp   = await api.get(imageUrl, { responseType: 'blob' })
    resultImage.value  = URL.createObjectURL(imageResp.data)
    resultArchiveUrl.value = archiveUrl

    if (fertUrl || uploadId) {
      try {
        const url = fertUrl ?? `/fertilization/${uploadId}/${selectedFormula.value}`
        const { data: fertData } = await api.get(url)
        if (fertData && typeof fertData === 'object' && Object.keys(fertData).length) {
          nitrogenZones.value = buildNitrogenZones(fertData)
        }
      } catch {}
    }

    const _ts     = new Date().toLocaleString('ru-RU')
    const _growth = growthStages.find(g => g.id === selectedGrowth.value)?.label
    const _seg    = segmentationLevel.value
    const _dateStr = (inputMode.value === 'coords' && snapDay.value)
      ? formatDate(snapDay.value, snapMonth.value, snapYear.value)
      : null

    resultMeta.formula    = selectedFormula.value
    resultMeta.mode       = inputMode.value
    resultMeta.area       = inputMode.value === 'coords'
      ? `${coordLat1.value}, ${coordLon1.value} → ${coordLat2.value}, ${coordLon2.value}`
      : null
    resultMeta.date       = _dateStr
    resultMeta.file       = inputMode.value === 'file' && uploadedFile.value ? uploadedFile.value.name : null
    resultMeta.timestamp  = _ts
    resultMeta.description =
      `Результат получен методом ${getFormulaName(selectedFormula.value)}. ` +
      `Фаза: ${_growth}. Сегментов: ${_seg}.` +
      (_dateStr ? ` Снимок за ${_dateStr}.` : '')

  } catch {}
  finally {
    isLoading.value = false
  }
}

const exportResult = () => {
  if (!resultArchiveUrl.value) return
  const a = document.createElement('a')
  a.href     = api.defaults.baseURL + resultArchiveUrl.value
  a.download = `result_${selectedFormula.value}_${Date.now()}.zip`
  a.click()
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

.page {
  background: #ffffff;
  font-family: 'Manrope', sans-serif;
  color: #1a1d23;
  min-height: 100vh;
}

.hero {
  padding: 72px 0 80px;
  border-bottom: 1px solid #e8eaee;
  background: #fafbfc;
}
.hero-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 48px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 80px;
  align-items: start;
}
.hero-eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 1.8px;
  text-transform: uppercase;
  color: #3d6ce8;
  margin-bottom: 24px;
  font-family: 'JetBrains Mono', monospace;
}
.dot {
  width: 6px; height: 6px;
  background: #3d6ce8;
  border-radius: 50%;
  animation: pulse 2s ease-in-out infinite;
}
@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50%       { opacity: 0.35; transform: scale(0.6); }
}
.hero-title {
  font-size: clamp(30px, 3.5vw, 46px);
  font-weight: 800;
  line-height: 1.15;
  letter-spacing: -1.5px;
  color: #0d0f14;
  margin-bottom: 24px;
}
.hero-title em {
  font-style: normal;
  color: #3d6ce8;
  position: relative;
}
.hero-title em::after {
  content: '';
  position: absolute;
  bottom: 2px; left: 0; right: 0;
  height: 3px;
  background: #3d6ce8;
  opacity: 0.18;
  border-radius: 2px;
}
.hero-desc {
  font-size: 14px;
  font-weight: 400;
  line-height: 1.8;
  color: #6b7280;
  margin-bottom: 14px;
}
.hero-stats {
  display: flex;
  align-items: center;
  gap: 28px;
  margin-top: 40px;
  padding-top: 32px;
  border-top: 1px solid #e8eaee;
}
.stat { display: flex; flex-direction: column; gap: 3px; }
.stat-num {
  font-size: 22px; font-weight: 800;
  color: #0d0f14; letter-spacing: -0.5px;
  font-family: 'JetBrains Mono', monospace;
}
.stat-label {
  font-size: 10px; color: #9ca3af;
  font-weight: 600; text-transform: uppercase; letter-spacing: 0.8px;
}
.stat-div { width: 1px; height: 32px; background: #e8eaee; }

.hero-gallery { padding-top: 8px; }
.gallery-label {
  font-size: 10px; font-weight: 700;
  letter-spacing: 1.8px; text-transform: uppercase;
  color: #c5c9d4; margin-bottom: 18px;
  font-family: 'JetBrains Mono', monospace;
}
.gallery-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.gallery-card {
  border: 1px solid #e8eaee; border-radius: 12px;
  overflow: hidden; cursor: default;
  will-change: transform; background: #fff;
  transition: box-shadow 0.2s ease;
}
.gallery-card-img { aspect-ratio: 4/3; overflow: hidden; }
.img-placeholder {
  width: 100%; height: 100%;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  gap: 8px; color: #c5c9d4;
  font-size: 11px; font-family: 'JetBrains Mono', monospace;
  background:
    repeating-linear-gradient(45deg, transparent 0px, transparent 12px, rgba(0,0,0,0.018) 12px, rgba(0,0,0,0.018) 24px),
    #f6f7f9;
}
.gallery-card-info {
  display: flex; align-items: center;
  justify-content: space-between;
  padding: 10px 14px;
  border-top: 1px solid #f0f1f3;
}
.gallery-card-title { font-size: 12px; font-weight: 600; color: #374151; }
.gallery-card-badge {
  font-size: 10px; font-weight: 600;
  font-family: 'JetBrains Mono', monospace;
  color: #3d6ce8; background: rgba(61,108,232,0.08);
  padding: 3px 8px; border-radius: 4px; letter-spacing: 0.3px;
}

.tool-section {
  max-width: 1200px; margin: 0 auto;
  padding: 52px 48px 72px;
}
.tool-header { margin-bottom: 28px; }
.tool-title {
  font-size: 22px; font-weight: 800;
  letter-spacing: -0.6px; color: #0d0f14; margin-bottom: 5px;
}
.tool-subtitle { font-size: 13px; color: #9ca3af; }

.workspace {
  display: grid;
  grid-template-columns: 310px 1fr;
  align-items: start;
  border: 1px solid #e8eaee;
  border-radius: 14px;
  box-shadow: 0 2px 16px rgba(0,0,0,0.05);
  overflow: hidden;
}
.panel { background: #fff; display: flex; flex-direction: column; }
.panel-left {
  border-right: 1px solid #e8eaee;
  overflow-x: visible;
  padding-bottom: 28px;
}
.panel-right {
  background: #fafbfc;
  min-height: 480px;
  display: flex;
  flex-direction: column;
}
.panel-header {
  display: flex; align-items: center;
  justify-content: space-between;
  padding: 15px 20px;
  border-bottom: 1px solid #e8eaee;
  background: #fff;
  flex-shrink: 0;
}
.panel-label {
  font-size: 10px; font-weight: 700;
  letter-spacing: 1.8px; color: #c5c9d4;
  text-transform: uppercase;
  font-family: 'JetBrains Mono', monospace;
}

.mode-toggle {
  display: flex; margin: 16px 20px 0;
  background: #f3f4f6; border-radius: 8px;
  padding: 3px; gap: 2px;
}
.mode-btn {
  flex: 1; display: flex; align-items: center;
  justify-content: center; gap: 6px;
  padding: 8px 10px; background: none; border: none;
  border-radius: 6px; font-size: 12px; font-weight: 600;
  color: #9ca3af; cursor: pointer; transition: all 0.2s;
  font-family: 'Manrope', sans-serif;
}
.mode-btn:hover { color: #374151; }
.mode-btn--active { background: #fff; color: #1a1d23; box-shadow: 0 1px 4px rgba(0,0,0,0.08); }

.input-section { padding: 16px 20px 0; }
.field { margin-bottom: 13px; }
.field-label {
  display: block; font-size: 10px; font-weight: 700;
  letter-spacing: 1.2px; color: #c5c9d4;
  text-transform: uppercase; margin-bottom: 7px;
  font-family: 'JetBrains Mono', monospace;
}
.field-input {
  width: 100%; padding: 9px 12px;
  background: #f9fafb; border: 1px solid #e8eaee;
  border-radius: 7px; font-size: 13px; color: #1a1d23;
  font-family: 'JetBrains Mono', monospace;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.field-input:focus {
  outline: none; border-color: #3d6ce8;
  box-shadow: 0 0 0 3px rgba(61,108,232,0.1);
  background: #fff;
}
.field-input::placeholder { color: #d1d5db; }

.coord-group {
  background: #f9fafb; border: 1px solid #e8eaee;
  border-radius: 9px; padding: 12px 12px 10px;
}
.coord-group-label {
  display: flex; align-items: center; gap: 6px;
  font-size: 10px; font-weight: 700; letter-spacing: 1.1px;
  text-transform: uppercase; color: #9ca3af;
  font-family: 'JetBrains Mono', monospace; margin-bottom: 10px;
}
.coord-corner-icon {
  display: flex; align-items: center; justify-content: center;
  width: 18px; height: 18px; border-radius: 4px; flex-shrink: 0;
}
.coord-corner-icon--bl { background: rgba(107,181,106,0.12); color: #5a9e59; }
.coord-corner-icon--tr { background: rgba(61,108,232,0.10); color: #3d6ce8; }

.coord-row { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
.field--half { margin-bottom: 0; }
.coord-connector {
  display: flex; align-items: center; gap: 8px;
  padding: 6px 14px; color: #d1d5db;
}
.coord-connector-line { flex: 1; height: 1px; background: #e8eaee; }

.date-block {
  display: flex;
  flex-direction: column;
  gap: 5px;
}
.date-row {
  display: grid;
  grid-template-columns: 1fr 1fr 1.4fr;
  gap: 8px;
  align-items: end;
}
.field--date-sm,
.field--date-md { margin-bottom: 0; }
.date-preview {
  font-size: 11px;
  color: #6bb56a;
  font-family: 'JetBrains Mono', monospace;
  font-weight: 500;
  letter-spacing: 0.2px;
}

.dropzone {
  border: 1.5px dashed #d1d5db; border-radius: 9px;
  padding: 26px 16px; display: flex; flex-direction: column;
  align-items: center; gap: 6px; cursor: pointer;
  transition: all 0.2s; background: #f9fafb;
}
.dropzone:hover,
.dropzone--active { border-color: #3d6ce8; background: rgba(61,108,232,0.03); }
.dropzone--filled  { border-style: solid; border-color: #6bb56a; background: rgba(107,181,106,0.04); }
.dz-icon       { color: #d1d5db; }
.dz-icon--ok   { color: #6bb56a; }
.dz-text       { font-size: 12px; color: #9ca3af; font-weight: 500; }
.dz-text--name { color: #374151; font-weight: 600; }
.dz-hint       { font-size: 11px; color: #c5c9d4; font-family: 'JetBrains Mono', monospace; }

.section-sep {
  display: flex; align-items: center; gap: 10px;
  margin: 20px 20px 14px;
  font-size: 10px; font-weight: 700; letter-spacing: 1.5px;
  color: #c5c9d4; text-transform: uppercase;
  font-family: 'JetBrains Mono', monospace;
}
.section-sep::after { content: ''; flex: 1; height: 1px; background: #e8eaee; }

.formula-list { padding: 0 20px; display: flex; flex-direction: column; gap: 3px; }
.formula-item {
  display: flex; align-items: center; gap: 10px;
  padding: 11px 12px; border: 1px solid transparent;
  border-radius: 8px; cursor: pointer; transition: all 0.15s;
}
.formula-item:hover { background: #f3f4f6; }
.formula-item--active { background: rgba(61,108,232,0.05); border-color: rgba(61,108,232,0.18); }

.formula-radio {
  width: 16px; height: 16px; border: 1.5px solid #d1d5db;
  border-radius: 50%; display: flex; align-items: center;
  justify-content: center; flex-shrink: 0; transition: border-color 0.15s;
}
.formula-item--active .formula-radio { border-color: #3d6ce8; }
.formula-radio-dot { width: 8px; height: 8px; background: #3d6ce8; border-radius: 50%; }
.formula-name {
  flex: 1; font-size: 13px; font-weight: 600;
  color: #9ca3af; font-family: 'JetBrains Mono', monospace; letter-spacing: 0.3px;
}
.formula-item--active .formula-name { color: #1a1d23; }

.tip-wrap {
  position: relative; color: #d1d5db;
  display: flex; align-items: center;
  cursor: default; transition: color 0.15s;
}
.tip-wrap:hover { color: #9ca3af; }
.tip-box {
  position: absolute; right: 0; top: calc(100% + 8px);
  width: 210px; padding: 10px 12px;
  background: #fff; border: 1px solid #e8eaee;
  border-radius: 8px; font-size: 12px; color: #374151;
  line-height: 1.6; z-index: 100; pointer-events: none;
  font-family: 'Manrope', sans-serif;
  box-shadow: 0 8px 24px rgba(0,0,0,0.1);
}

.run-btn {
  display: flex; align-items: center; justify-content: center;
  gap: 8px; margin: 20px 20px 0; padding: 12px 20px;
  background: #1a1d23; border: none; border-radius: 8px;
  font-size: 13px; font-weight: 700; color: #fff;
  cursor: pointer; transition: all 0.2s;
  font-family: 'Manrope', sans-serif;
}
.run-btn:hover:not(:disabled) { background: #2e3440; }
.run-btn:disabled { opacity: 0.32; cursor: not-allowed; }

.export-btn {
  display: flex; align-items: center; gap: 6px;
  padding: 7px 13px; background: none;
  border: 1px solid #e8eaee; border-radius: 6px;
  font-size: 12px; font-weight: 600; color: #6b7280;
  cursor: pointer; transition: all 0.2s;
  font-family: 'Manrope', sans-serif;
}
.export-btn--tif {
  border-color: rgba(61,108,232,0.35);
  color: #3d6ce8;
  background: rgba(61,108,232,0.05);
}
.export-btn--tif:hover {
  border-color: #3d6ce8;
  background: rgba(61,108,232,0.12);
  box-shadow: 0 0 0 3px rgba(61,108,232,0.08);
}

.result-area {
  flex: 1;
  display: flex;
  align-items: stretch;
  overflow: hidden;
  min-height: 0;
}

.empty-state {
  flex: 1; display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  gap: 10px; position: relative;
}
.empty-dots {
  position: absolute; display: grid;
  grid-template-columns: repeat(3,1fr);
  gap: 36px; opacity: 0.05;
}
.empty-dot { width: 4px; height: 4px; background: #1a1d23; border-radius: 50%; }
.empty-state svg { color: #d1d5db; position: relative; }
.empty-text  { font-size: 13px; color: #9ca3af; font-weight: 500; position: relative; }
.empty-hint  { font-size: 11px; color: #c5c9d4; font-family: 'JetBrains Mono', monospace; position: relative; }

.loading-state {
  flex: 1; display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  gap: 20px; position: relative; overflow: hidden;
}
.scan-line-wrap { position: absolute; inset: 0; overflow: hidden; pointer-events: none; }
.scan-line {
  position: absolute; left: 0; right: 0; height: 1px;
  background: linear-gradient(90deg, transparent, rgba(61,108,232,0.45), transparent);
  animation: scan 2s linear infinite;
}
@keyframes scan { 0% { top: 0; } 100% { top: 100%; } }
.loading-text {
  font-size: 12px; color: #9ca3af;
  font-family: 'JetBrains Mono', monospace;
  letter-spacing: 0.5px; min-height: 18px;
}
.progress-bar {
  width: 160px; height: 2px;
  background: #e8eaee; border-radius: 2px; overflow: hidden;
}
.progress-fill {
  height: 100%; background: #3d6ce8; border-radius: 2px;
  animation: prog 1.6s ease-in-out infinite alternate;
}
.progress-fill--det {
  animation: none; transition: width 0.25s ease; margin-left: 0 !important;
}
@keyframes prog { 0% { width: 10%; margin-left: 0; } 100% { width: 40%; margin-left: 60%; } }
.progress-pct {
  font-size: 11px; color: #9ca3af;
  font-family: 'JetBrains Mono', monospace;
  letter-spacing: 0.3px; min-height: 16px;
}

.result-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}
.result-img-wrap {
  position: relative;
  overflow: hidden;
  background: #f3f4f6;
  min-height: 220px;
  flex-shrink: 0;
}
.result-img { width: 100%; height: 100%; object-fit: contain; display: block; }
.result-badge-wrap { position: absolute; top: 14px; left: 14px; }
.result-badge {
  padding: 4px 10px;
  background: rgba(255,255,255,0.92);
  border: 1px solid #e8eaee; border-radius: 4px;
  font-size: 11px; font-family: 'JetBrains Mono', monospace;
  color: #3d6ce8; letter-spacing: 0.3px;
  backdrop-filter: blur(4px);
}

.nitrogen-panel {
  border-top: 1px solid #e8eaee;
  border-bottom: 1px solid #e8eaee;
  background: #fff;
  padding: 16px 20px;
  flex-shrink: 0;
}
.nitrogen-header {
  display: flex;
  align-items: center;
  gap: 7px;
  margin-bottom: 13px;
}
.nitrogen-header svg { color: #3d6ce8; flex-shrink: 0; }
.nitrogen-title {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 1.6px;
  text-transform: uppercase;
  color: #6b7280;
  font-family: 'JetBrains Mono', monospace;
}
.nitrogen-zones { display: flex; flex-direction: column; gap: 6px; }
.nitrogen-zone {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 9px 12px;
  border-radius: 8px;
  background: #fafbfc;
  border: 1px solid #f0f1f3;
  transition: background 0.15s, border-color 0.15s;
}
.nitrogen-zone:hover { background: #f3f4f6; border-color: #e8eaee; }
.zone-color-bar {
  position: relative;
  flex-shrink: 0;
  width: 4px;
  height: 36px;
  border-radius: 3px;
  overflow: visible;
}
.zone-swatch { width: 4px; height: 100%; border-radius: 3px; }
.zone-pulse {
  position: absolute;
  inset: 0;
  border-radius: 3px;
  opacity: 0.3;
  animation: zonePulse 2.4s ease-in-out infinite;
}
@keyframes zonePulse {
  0%, 100% { transform: scaleX(1);   opacity: 0.3; }
  50%       { transform: scaleX(2.5); opacity: 0.12; }
}
.zone-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}
.zone-label {
  font-size: 12px; font-weight: 600; color: #374151;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.zone-desc {
  font-size: 10px; color: #9ca3af;
  font-family: 'JetBrains Mono', monospace;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.zone-amount-wrap {
  display: flex; align-items: baseline; gap: 3px; flex-shrink: 0;
}
.zone-amount {
  font-size: 18px; font-weight: 800;
  font-family: 'JetBrains Mono', monospace;
  color: #0d0f14; letter-spacing: -0.5px; line-height: 1;
}
.zone-unit {
  font-size: 10px; font-weight: 600; color: #9ca3af;
  font-family: 'JetBrains Mono', monospace; letter-spacing: 0.3px;
}

.result-meta { padding: 14px 20px; background: #fff; flex-shrink: 0; }
.meta-grid { display: flex; flex-wrap: wrap; gap: 8px 24px; margin-bottom: 10px; }
.meta-item { display: flex; flex-direction: column; gap: 2px; }
.meta-label {
  font-size: 10px; letter-spacing: 1.2px; color: #c5c9d4;
  text-transform: uppercase; font-family: 'JetBrains Mono', monospace;
}
.meta-val { font-size: 12px; color: #374151; font-family: 'JetBrains Mono', monospace; font-weight: 500; }
.result-desc { font-size: 12px; color: #9ca3af; line-height: 1.7; }
.meta-method { display: flex; align-items: center; gap: 6px; }
.meta-method-icon {
  display: flex; align-items: center; justify-content: center;
  width: 22px; height: 22px; border-radius: 5px;
  background: rgba(61,108,232,0.07); color: #3d6ce8; flex-shrink: 0;
}

.spinner {
  width: 13px; height: 13px;
  border: 2px solid rgba(255,255,255,0.2);
  border-top-color: white; border-radius: 50%;
  animation: spin 0.7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

.slide-fade-enter-active, .slide-fade-leave-active { transition: all 0.18s ease; }
.slide-fade-enter-from { opacity: 0; transform: translateY(5px); }
.slide-fade-leave-to   { opacity: 0; transform: translateY(-5px); }

.res-fade-enter-active { animation: rfIn 0.35s cubic-bezier(0.16,1,0.3,1); }
.res-fade-leave-active { animation: rfOut 0.18s ease; }
@keyframes rfIn  { from { opacity: 0; transform: scale(0.98); } to { opacity: 1; transform: scale(1); } }
@keyframes rfOut { from { opacity: 1; } to { opacity: 0; } }

.tip-enter-active { animation: tipIn  0.12s ease; }
.tip-leave-active { animation: tipOut 0.10s ease; }
@keyframes tipIn  { from { opacity: 0; transform: translateY(-3px); } to { opacity: 1; transform: none; } }
@keyframes tipOut { from { opacity: 1; } to { opacity: 0; } }

.panel-left::-webkit-scrollbar       { width: 4px; }
.panel-left::-webkit-scrollbar-track { background: transparent; }
.panel-left::-webkit-scrollbar-thumb { background: #e8eaee; border-radius: 2px; }

.growth-list { padding: 0 20px; display: flex; flex-direction: column; gap: 3px; }
.growth-info { display: flex; flex-direction: column; gap: 2px; flex: 1; }
.growth-sub  { font-size: 10px; color: #9ca3af; font-weight: 500; line-height: 1.4; }

.bands-grid {
  padding: 0 20px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}
.band-field { display: flex; flex-direction: column; gap: 4px; }
.band-field-head {
  display: flex; align-items: center; justify-content: space-between;
}
.field-input--error {
  border-color: #f87171 !important;
  background: #fff8f8 !important;
  box-shadow: 0 0 0 3px rgba(248,113,113,0.1) !important;
}
.band-error {
  font-size: 10px; color: #ef4444;
  font-family: 'JetBrains Mono', monospace;
  line-height: 1.3;
}
.tip-box--band { right: auto; left: 0; width: 220px; }

.seg-block { padding: 0 20px; }
.seg-header {
  display: flex; align-items: center;
  justify-content: space-between; margin-bottom: 10px;
}
.seg-label {
  font-size: 11px; color: #6b7280;
  font-weight: 600; line-height: 1.4; max-width: 180px;
}
.seg-val {
  font-size: 20px; font-weight: 800;
  color: #3d6ce8; font-family: 'JetBrains Mono', monospace; line-height: 1;
}
.seg-track-wrap { position: relative; margin-bottom: 6px; }
.seg-range {
  width: 100%; appearance: none;
  height: 3px; background: #e8eaee;
  border-radius: 2px; outline: none; cursor: pointer; accent-color: #3d6ce8;
}
.seg-range::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 18px; height: 18px; border-radius: 50%;
  background: #3d6ce8; border: 3px solid #fff;
  box-shadow: 0 1px 6px rgba(61,108,232,0.35); cursor: pointer;
}
.seg-ticks { display: flex; justify-content: space-between; padding: 4px 2px 0; }
.seg-tick {
  font-size: 10px; font-family: 'JetBrains Mono', monospace;
  color: #c5c9d4; font-weight: 600; transition: color 0.15s;
}
.seg-tick--active { color: #3d6ce8; }
.seg-hint {
  font-size: 11px; color: #9ca3af; line-height: 1.6;
  margin-top: 6px; min-height: 34px;
}

.validation-error {
  display: flex; align-items: flex-start; gap: 7px;
  margin: 12px 20px 0; padding: 10px 12px;
  background: #fff8f8; border: 1px solid rgba(248,113,113,0.35);
  border-radius: 8px; font-size: 12px; color: #ef4444;
  line-height: 1.5; font-family: 'Manrope', sans-serif;
}
.validation-error svg { flex-shrink: 0; margin-top: 1px; }

.resolution-block {
  padding: 0 20px; display: flex; flex-direction: column; gap: 4px; margin-bottom: 4px;
}

@media (max-width: 960px) {
  .hero-inner   { grid-template-columns: 1fr; gap: 48px; padding: 0 24px; }
  .tool-section { padding: 40px 24px 56px; }
  .workspace    { grid-template-columns: 1fr; }
  .panel-left   { border-right: none; border-bottom: 1px solid #e8eaee; }
}
</style>