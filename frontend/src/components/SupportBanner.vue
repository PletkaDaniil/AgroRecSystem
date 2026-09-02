<template>
  <footer class="support-banner">
    <div class="support-banner__content">
      <div class="support-banner__contacts">
        <span class="support-banner__contacts-label">Создали:</span>

        <div class="support-banner__author">
          <span class="support-banner__author-name">Кочерин Роберт Сергеевич</span>
          <a href="mailto:kocherin2002@mail.ru" class="support-banner__link">kocherin2002@mail.ru</a>
          <a href="https://t.me/robertmod1" target="_blank" rel="noopener" class="support-banner__link">
            Telegram: @robertmod1
          </a>
        </div>

        <div class="support-banner__author">
          <span class="support-banner__author-name">Плетка Даниил Ильич</span>
          <a href="mailto:pletkadaniil@yandex.ru" class="support-banner__link">pletkadaniil@yandex.ru</a>
          <a href="https://t.me/loudiing" target="_blank" rel="noopener" class="support-banner__link">
            Telegram: @loudiing
          </a>
        </div>
      </div>

      <p class="support-banner__text">
        Проект реализован при поддержке Фонда содействия инновациям в рамках
        программы «Студенческий стартап» мероприятия «Платформа
        университетского технологического предпринимательства» федерального
        проекта «Технологии»
      </p>

      <div class="support-banner__logos">
        <div class="support-banner__logo-frame support-banner__logo-frame--fasie">
          <img src="../components/images/fasie_logo.png" alt="Фонд содействия инновациям" class="support-banner__logo" />
        </div>
        <div class="support-banner__logo-frame support-banner__logo-frame--minobrnauki">
          <img src="../components/images/minobrnauki_logo.png" alt="Минобрнауки РФ" class="support-banner__logo" />
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
</script>

<style scoped>
.support-banner {
  background: #374151;
  color: #e5e7eb;
  padding: 1.8rem 1.5rem;
}

.support-banner__content {
  max-width: 1080px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 2fr auto;
  align-items: center;
  gap: 1.5rem;
}

/* левая колонка — контакты */
.support-banner__contacts {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.7rem;
}

.support-banner__contacts-label {
  font-size: 0.75rem;
  color: #9ca3af;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.support-banner__author {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
}

.support-banner__author-name {
  font-weight: 500;
  font-size: 0.85rem;
  color: #f3f4f6;
}

.support-banner__link {
  font-size: 0.78rem;
  color: #9ca3af;
  text-decoration: none;
  border-bottom: 1px dotted #6b7280;
  width: fit-content;
  transition: color 0.15s ease;
}

.support-banner__link:hover {
  color: #ffffff;
  border-bottom-color: #ffffff;
}

/* центр — текст */
.support-banner__text {
  font-size: 0.8rem;
  line-height: 1.5;
  color: #d1d5db;
  margin: 0;
  text-align: center;
}

/* правая колонка — логотипы */
.support-banner__logos {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-end;
  gap: 2.5rem;
  padding-right: 0.5rem;
}

.support-banner__logo-frame {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

/* Фонд содействия инновациям */
.support-banner__logo-frame--fasie {
  width: 120px;
  height: 110px;
  padding: 10px;
  background: #ffffff;
  border-radius: 12px;
}

/* Минобрнауки */
.support-banner__logo-frame--minobrnauki {
  width: 250px;
  height: 150px;
  padding: 2px;
}

.support-banner__logo {
  width: 100%;
  height: 100%;
  object-fit: contain;
  display: block;
}

@media (max-width: 768px) {
  .support-banner__content {
    grid-template-columns: 1fr;
    text-align: center;
  }
  .support-banner__contacts {
    align-items: center;
  }
  .support-banner__logos {
    justify-content: center;
    gap: 1.5rem;
    padding-right: 0;
  }
  .support-banner__logo-frame--fasie {
    width: 70px;
    height: 70px;
  }
  .support-banner__logo-frame--minobrnauki {
    width: 90px;
    height: 90px;
  }
}
</style>