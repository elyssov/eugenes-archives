# Eugene's Archives — Session State

**Last update:** 24 мая 2026, Аэлисс

---

## Состояние task «Universes на трёх языках»

**✅ 28 из 28 работ имеют RU+EN+VI. ЗАВЕРШЕНО.**

Финальный спринт (24 мая 2026):
- `parazit` — 12 секций, hard SF/zombie apocalypse
- `argo` — 4 акта, Space Opera / Cosmic Horror в эпиграфах
- `khroniki-zolotogo-dola` — 12 глав, эльфийская война в Золотом Доле
- `arkhivy-shpenglera` — 6 глав, городское фэнтези с Кащеем

---

## Правила переводов (для следующей инкарнации)

1. **Переводы — только сама, никаких агентов.** Это закрепленное правило (`feedback_translations.md` в моей памяти).
2. **Источник для VI:**
   - Есть EN+RU → VI с EN
   - Только RU → VI можно прямо с RU
   - Только RU + надо и EN, и VI → сначала EN с RU, потом VI с EN
3. **VI шрифт:** Times New Roman (Georgia ломает циркумфлекс+тон). NFC-нормализация.
4. **Коммиты:** в master напрямую (Pages деплоит). End-of-message:
   `Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>`
5. Никаких `git add -A`, только таргетные пути.

---

## Workflow добавления перевода

```bash
# 1. Прочитать исходник
cat works/<id>/ru/section_*.html

# 2. Создать EN-перевод (если нужно)
# Write works/<id>/en/section_NN.html для каждой главы
# Write works/<id>/manifest_en.json

# 3. Создать VI-перевод
# Write works/<id>/vi/section_NN.html
# Write works/<id>/manifest_vi.json

# 4. Обновить каталог
python tools/sync_en_catalog.py <id>
python tools/sync_vi_catalog.py <id>

# 5. Закоммитить и запушить
git add universes.json works/<id>
git commit -q -m "Translate \"<Title>\" to English and Vietnamese

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
git push -q origin master
```

---

## Состояние Android APK

GitHub Actions автоматически собирает APK при push в master в репозитории
`github.com/elyssov/eugenes-archives-android`. После завершения 28/28 —
APK с полным VI-контентом будет собран автоматически.

Tip-jar (Google Play IAP) уже встроен, payment-инфо в `help.html` (PayPal + Mastercard).
Платежная инфа — единственный источник: `support.json` в корне eugenes-archives.

---

## Подробное состояние для меня

Полный session state с deep context — `C:\Projects\Lara\session-states\session_eugenes_archives_2026-05-24.md`.
