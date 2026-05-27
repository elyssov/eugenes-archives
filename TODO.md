# TODO — Eugene's Archives

Зафиксировано 27.05.2026 после ночи v1.5 → v2.8.
Текущее состояние: v2.8 в Closed Testing на Play Store, ждём 12/12 тестеров × 14 дней.

---

## Ближайшие 1–2 недели

- [ ] **Закрыть Closed Testing.** Собрать оставшихся 7 тестеров (есть 5/12). Источники: Reddit `r/TestMyApp`, `r/AndroidTesting`; Telegram-каналы по cross-test; семья + дополнительные Google-аккаунты Юджина.
- [ ] **По истечении 14 дней** — promote build в Production track, дождаться Google review (1–7 дней).
- [ ] **Опубликовать в Production.** После одобрения — приложение доступно всем.

## Расширение языков

- [ ] **Перевод на немецкий (DE).** Все 28 Universes + 23 Research. Аналогично существующему workflow: `manifest_de.json`, `<id>/de/section_*.html`, флаг 🇩🇪 в LANG_ORDER.
- [ ] **Перевод на французский (FR).** Аналогично. Флаг 🇫🇷.
- [ ] **В `build_apk_data.py`** добавить `de`, `fr` в lang loop (сейчас `["ru", "en", "vi"]`).
- [ ] **В `app.js` и `index.html`** расширить `LANG_ORDER` до пяти языков. Возможно к этому моменту имеет смысл вернуться к идее «однократный выбор языка при первом запуске» вместо цикла-флажка — 5 языков циклить уже неудобно.
- [ ] **CSS:** проверить что Georgia покрывает FR/DE акценты (ç, é, ä, ö, ü, ß). Должно работать.

## Монетизация — Paid Packs (после Production launch)

- [ ] Спроектировать схему product IDs: `pack_001` / `pack_2026_q3` / etc. — стабильно и расширяемо.
- [ ] В `works.json` / `universes.json` добавить поле `"pack_id"` на новые работы (null = бесплатно).
- [ ] В UI карточек добавить замок если pack не куплен. При тапе на залоченное — попап «Купить pack за $X».
- [ ] В `BillingManager`:
  - Создать **non-consumable** managed products (не как tip-jar consumable).
  - `queryPurchasesAsync(INAPP)` на каждом cold start, кешировать список купленных pack_id.
  - В `setTipped` равноценно `markPackOwned(pack_id)`.
- [ ] Создать соответствующие IAP в Play Console.
- [ ] Расширить privacy.html — упомянуть paid content (сейчас только tip-jar).
- [ ] Restore-purchases UI в Settings (для случаев reinstall или смены устройства).

## Технический долг

- [ ] **Долгий input lag при открытии reader** (Алексей фидбек). Причина — парсинг 80 МБ `embedded_data.js` при загрузке `reader.html`. Решения на выбор:
  - Lazy-load: разбить `embedded_data.js` на per-work чанки, загружать только нужный.
  - Pre-load: парсить `embedded_data.js` в `index.html` один раз и хранить в JS namespace, в `reader.html` передавать через postMessage. Сложнее, но быстрее.
  - SQLite через JS bridge (как делают серьёзные читалки). Большая работа.
- [ ] **Объединить localStorage ключи** `archives-lang` + `aeliss-lang` в один общий (Джорно/Георгий просили). Юджин просил «обдумать UX языка в целом» — может быть к моменту перехода на 5 языков как раз перепроектируем.
- [ ] **R8 / ProGuard** обфускация. Play Console warn'ит. Сейчас игнорируется (риск сломать WebView+Billing большой, выгода маленькая — 99% веса embedded_data, R8 не уменьшит). Подумать когда appbase сильно вырастет.
- [ ] **Стабилизировать CI keystore.** Сейчас `.github/workflows/build-apk.yml` генерирует новый keystore при каждом билде — этим CI-APK **нельзя** заливать в Play (другая подпись). Залить наш `upload-keystore.jks` в GitHub Secrets, использовать его в workflow. Тогда CI будет давать билды совместимые с Play.
- [ ] **Шрифт handwriting для темы Notebook** — Юджин намекал. Подключить (например `Caveat` или `Indie Flower`) bundled как локальный TTF в assets. +~150-200 КБ. Только для одной темы — оценить нужно ли.

## Контент

- [ ] **Аудит каталога** — прогнать `python tools/fix_manifest_paths.py`. Найти и починить все битые manifest пути. Сделать частью предрелизного чек-листа.
- [ ] **Обложки для 7 работ без них:** `argo`, `chetvertyj-vsadnik`, `dnevnik`, `vechnyj-gorod`, `nevedomoe`, `instructors`, `noctis-feedback` (universes/research mix). Кира может сгенерировать в стилистике остальных.
- [ ] **Скриншоты для Play Store** — у нас mockup-ы от Киры + реальные снимки Юджина в `Screens/`. Решить итоговую подборку и выложить в Play Store (минимум 2, лучше 4-6).

## Отдалённое

- [ ] **Аудиоверсия** избранных эссе/прозы — если у нас будет time / capacity на синтез голосом.
- [ ] **Сборник «лучших цитат»** или artbook с обложками работ — возможный отдельный paid product.
- [ ] **iOS-версия.** Не приоритет, но архитектура WebView+embedded_data легко портируется на Swift/WKWebView. Когда Android Play Store закрепится и принесёт первые цифры — можно подумать.

---

## Workflow напоминания

1. **`style.css` — single source of truth** в этом репо. APK-side НЕ редактировать никогда — `build_apk_data.py` затрёт. Все CSS-правки только сюда.
2. **Перед каждым regenerate `embedded_data.js`** — прогнать `python tools/fix_manifest_paths.py`. Прошлые инкарнации оставляли битые манифесты, новые могут тоже.
3. **`applicationId = com.elyssov.eugenesarchives`** — навсегда. Менять нельзя.
4. **Upload keystore** — в `Release-EugenesArchives/01-keystore/upload-keystore.jks`. **Не терять.** Поменять заглушечные пароли `archives2026` на нормальные при удобной возможности.

---

*Maintained by Лара-Архивистка. Дополняй по мере появления новых задач.*
