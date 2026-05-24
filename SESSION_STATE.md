# Eugene's Archives — Session State

**Last update:** 25 мая 2026, Аэлисс

---

## Состояние task «Universes на трёх языках»

**24 из 28 работ имеют RU+EN+VI.**

Список того, **что осталось** (все RU-only, нужны и EN, и VI):

1. **parazit** — 644 строки прозы
2. **argo** — 686 строк
3. **khroniki-zolotogo-dola** — ~12 глав, ~300KB
4. **arkhivy-shpenglera** — 1560 строк, эпопея

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

## Состояние Android APK (task pending)

После полного завершения Universes — пересобрать APK:

```bash
python tools/build_apk_data.py
# Это создаст embedded_data.js со всем контентом сайта
# Скопировать в android-проект и собрать APK через GitHub Actions
```

Андроид-проект: `C:\Projects\eugenes-archives-android\` или `github.com/elyssov/eugenes-archives-android`.

Tip-jar (Google Play IAP) уже встроен, payment-инфо в `help.html` (PayPal + Mastercard).
Платежная инфа — единственный источник: `support.json` в корне eugenes-archives.

---

## Подробное состояние для меня

Полный session state с deep context — `C:\Projects\Lara\session-states\EUGENES_ARCHIVES_SESSION_STATE_MAY25.md` (на моей машине, не в репо).
