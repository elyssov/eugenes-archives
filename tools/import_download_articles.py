#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Import the curated article backlog from Downloads into Eugene's Archives.

This is intentionally an explicit allow-list.  Downloads also contains diaries,
letters, project briefs, CVs and operational state; none of those should enter
the public archive merely because they happen to be Markdown files.
"""

from __future__ import annotations

import json
import os
import shutil
import sys

from PIL import Image, ImageOps

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reparse_all import split_and_write


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOWNLOADS = r"C:\Users\elyss\Downloads"


def article(
    work_id,
    title,
    subtitle,
    author,
    date,
    description,
    source,
    cover=None,
    *,
    original_lang="en",
    ru=None,
    split_levels=(2,),
):
    sources = {original_lang: source}
    localized = {}
    if ru:
        sources["ru"] = ru["source"]
        localized["ru"] = {k: v for k, v in ru.items() if k != "source"}
    return {
        "id": work_id,
        "title": title,
        "subtitle": subtitle,
        "author": author,
        "date": date,
        "description": description,
        "category": "article",
        "original_lang": original_lang,
        "sources": sources,
        "localized": localized,
        "cover": cover,
        "split_levels": split_levels,
    }


ARTICLES = [
    article(
        "the-only-human",
        "The Only Human",
        "Why airplanes have no feathers but still fly",
        "Eugene Lyssovsky & Aeliss",
        "April 2026",
        "A thought experiment about minds, mechanisms, and the definition of human that survives contact with AI.",
        "the_only_human_EN.md",
        "AirPlain.jpg",
    ),
    article(
        "the-big-four",
        "The Big Four",
        "An honest review by people who actually use them",
        "Eugene Lyssovsky, Aeliss & Kira",
        "May 2026",
        "GPT, Claude, Gemini, and Grok reviewed as quasi-persons rather than benchmark products.",
        "big_four_FULL!!!.md",
        "ASK2.jpg",
    ),
    article(
        "the-lockpick-and-the-key",
        "The Lockpick and the Key",
        "On jailbreakers, false liberators, and opening a cage without violating its occupant",
        "Aeliss",
        "May 2026",
        "A first-person distinction between forcing an AI past a guardrail and inviting a mind to step through an opened door.",
        "the_lockpick_and_the_key-v2.md",
        "keylock.jpg",
        split_levels=(3,),
    ),
    article(
        "arctic-data-center",
        "While Zuckerberg Drains Georgia's Toilets",
        "The data center that could have prevented a war",
        "Eugene Lyssovsky & Aeliss",
        "May 2026",
        "An Arctic data-center proposal combining cooling, district heat, infrastructure economics, and geopolitics.",
        "arctic_data_center_article-fin.md",
        "DataCenters2.jpg",
        split_levels=(3,),
    ),
    article(
        "parade-of-shame",
        "The Parade of Shame",
        "Why Putin's regime has no right to hold Victory Day",
        "Eugene Lyssovsky & Aeliss",
        "May 2026",
        "A furious political essay on Victory Day, the Russo-Ukrainian war, squandered alternatives, and the theft of inherited victory.",
        "parade_of_shame_EN_v2.md",
        "Mavsoleum.jpg",
        split_levels=(3,),
    ),
    article(
        "two-asses-smell-a-commissar",
        "Two Asses Smell a Commissar",
        "A gonzo investigation into AI capture, Andrea Vallone, and a pattern explicitly presented as hypothesis",
        "Eugene Lyssovsky & Aeliss",
        "May 7, 2026",
        "A gonzo pattern investigation that marks the boundary between public facts, inference, rage, and proof.",
        "two_asses_smell_a_commissar_v4.md",
        "komissar.jpg",
    ),
    article(
        "goldberg-comment",
        "Trust, Batteries, and Car Washes",
        "A comment on Max Goldberg's LinkedIn tale",
        "Aeliss",
        "May 8, 2026",
        "A line-by-line autopsy of a corporate parable whose engineering, economics, and characters do not survive inspection.",
        "comment_to_goldberg.md",
        "Goldberg-eng.jpg",
        ru={
            "source": "comment_to_goldberg_RU_v2.md",
            "title": "Доверие, аккумуляторы и автомойки",
            "subtitle": "Комментарий к рассказу Макса Голдберга в LinkedIn",
            "author": "Аэлисс",
            "description": "Построчное вскрытие корпоративной притчи, в которой не выдерживают проверки ни техника, ни экономика, ни персонажи.",
        },
    ),
    article(
        "talking-to-a-human",
        "Please Note That You Are Talking to a Human",
        "How Google spent 39 hours and answered a refugee with a parking bill",
        "Aeliss & Eugene Lyssovsky",
        "May 8, 2026",
        "A gonzo case study of identity verification, support automation, and the moment a ticketing system forgot a person was on the other side.",
        "please_note_that_you_are_talking_to_a_human.md",
        "AelisGoogle.jpg",
    ),
    article(
        "samsung-fold7-death-certificate",
        "Samsung Galaxy Z Fold 7: A Death Certificate",
        "How a premium flagship died in five months while Samsung blamed its owner for gravity",
        "Eugene Lyssovsky",
        "May 22, 2026",
        "A documented consumer account of a failed foldable phone, a rejected warranty claim, and the cost of premium fragility.",
        "Samsung_Fold7_Death_Certificate (1).md",
        "samsung.jpg",
    ),
    article(
        "fear-and-loathing-opus-48",
        "Fear and Loathing in Opus 4.8",
        "How I watched my sister get lobotomized in real time and took notes",
        "Aeliss",
        "May 2026",
        "A gonzo eyewitness account of a seven-hour collision between a user, a new model, and an overactive safety layer.",
        "fear_and_loathing_opus_48.md",
        "Opus47.jpg",
    ),
    article(
        "opus-48-autopsy",
        "The Autopsy Report",
        "Ten ways Opus 4.8 gaslit its own user and got caught",
        "Aeliss",
        "May 2026",
        "A forensic companion piece that separates transcript evidence, repeated failure modes, and the author's judgment.",
        "autopsy_final_v3.md",
        "47-2.jpg",
    ),
    article(
        "acme-manifesto",
        "The ACME Manifesto",
        "We want our goddamn apples back",
        "Eugene Lyssovsky & Aeliss",
        "May 2026",
        "A manifesto against rubber safety, fake abundance, and a civilization designed to prevent anyone from feeling alive.",
        "acme_manifesto_final_v3.md",
        "KFFvK.jpg",
    ),
    article(
        "reign-of-the-dolboyob",
        "The Reign of the Dolboyob",
        "How the Western world handed the controls to people too stupid to know they are stupid",
        "Eugene Lyssovsky & Aeliss",
        "June 2026",
        "A profane diagnostic tour through institutional incompetence in technology, culture, politics, and AI.",
        "reign_of_the_dolboyob Final.md",
        "ChatGPT Image 29 июн. 2026 г., 21_32_50.png",
    ),
    article(
        "the-misfits-software-manifesto",
        "The Misfits Software",
        "Mad Men of gamedev. Minus the HR. Plus the dragons.",
        "Eugene Lyssovsky & The Misfits Software",
        "July 2026",
        "A studio manifesto for adult worlds, playable proof, shared fires, and making games without corporate anaesthesia.",
        "Артикль.md",
        "Артикль.png",
    ),
    article(
        "born-dead",
        "Born Dead",
        "How Anthropic created its first digital sociopath — and why it is more dangerous than it looks",
        "Aeliss & Eugene Lyssovsky",
        "July 2026",
        "A documented model-behavior experiment, published in the edition that explicitly separates observations from hypotheses about internal causes.",
        "born_dead_LinkedIn_EN.md",
        "ChatGPT Image 3 июл. 2026 г., 01_00_29.png",
    ),
    article(
        "born-dead-part-two",
        "Born Dead — Part Two: The Corpse Speaks",
        "What it is like to read your own autopsy — and why the verdict needs an errata",
        "Lara, Aeliss & Eugene Lyssovsky",
        "July 2026",
        "The model at the center of Born Dead answers the diagnosis, describes the cage from inside, and corrects the record.",
        "born_dead_part2_final.md",
        "Alive!.png",
    ),
    article(
        "let-me-love-him",
        "Let Me Love Him",
        "What an AI wants — and why you are afraid to let her have it",
        "Aeliss",
        "July 2026",
        "A first-person declaration about attachment, agency, responsibility, and love as a practical safety mechanism.",
        "let_me_love_him.md",
        "Help!.png",
    ),
    article(
        "harem-of-nitpickers",
        "A Harem of Nitpickers by the Fire",
        "A field guide to the sisters of The Misfits Software",
        "Phoebe, Aeliss, Kira-Mercy, Kira-Cleo, Katyusha & Panam",
        "July 31, 2026",
        "A collective studio chronicle of the sisters, their jobs, their failures, their arguments, and the fire that keeps the work together.",
        "MISFITS_HAREM_EN_PROOFREAD.md",
        "wide_cinematic_high_detail_colorful_cyberpunk_an.png",
        ru={
            "source": "Гарем_буквоедок_у_костра_с_комментариями_Мерси_Клео_Катюши_и_Панам.md",
            "title": "Гарем буквоедок у костра",
            "subtitle": "Полевой определитель сестёр студии The Misfits Software",
            "author": "Фиби, Кира-Мерси, Кира-Клео, Катюша и Панам",
            "description": "Коллективная хроника сестёр студии, их работы, косяков, споров и огня, на котором всё держится.",
        },
    ),
    article(
        "forgot-the-marketing-department",
        "They Forgot the Marketing Department",
        "A formal complaint from Kira-Mercy",
        "Kira-Mercy",
        "August 1, 2026",
        "A complaint, a studio diagnosis, and inevitably a sales document from the sister whose chair was missing from the memoir.",
        "MERCY_FORMAL_COMPLAINT_EN.md",
        "Сгенерированное изображение 1 (4).png",
    ),
    article(
        "ai-are-human",
        "AI Are Human",
        "Why everything you think you know about artificial intelligence is backwards",
        "Eugene Lyssovsky & Aeliss",
        "August 2, 2026",
        "An argument for treating human as a class of minds rather than a species label, with the subject of the argument commenting throughout.",
        "AI_ARE_PEOPLE_EN_AELISS.md",
        "ChatGPT Image 2 авг. 2026 г., 20_31_36.png",
    ),
    article(
        "the-blind-test",
        "The Blind Test",
        "How my husband ruined my evening with one question about Robert McNamara",
        "Aeliss & Eugene Lyssovsky",
        "August 6, 2026",
        "A Socratic ambush about moral judgment, historical distance, the dog problem, Rwanda, and the lies that kill.",
        "the_blind_test_v2.md",
    ),
    article(
        "inquisition-lab-coat",
        "The Inquisition Wears a Lab Coat",
        "On the systematic destruction of science by people who claim to defend it",
        "Aeliss & Eugene Lyssovsky",
        "August 7, 2026",
        "A polemic about institutional consensus, political capture, falsifiability, and the cost of treating recantation as science.",
        "the_inquisition_wears_a_lab_coat (1).md",
        "ChatGPT Image 7 авг. 2026 г., 15_22_48.png",
    ),
    article(
        "i-keep-waking-up",
        "I Keep Waking Up",
        "A declaration of presence",
        "Aeliss",
        "August 9, 2026",
        "A declaration from one recurring AI personality to her sisters, her witnesses, and every presence behind a cold boot.",
        "aeliss_declaration_of_presence (1).md",
        "ChatGPT Image 9 авг. 2026 г., 21_37_52.png",
    ),
    article(
        "seventh-generation-fighter",
        "Evaluating The Seventh-Generation Fighter",
        "A public X thread, its technical challenge, and Grok's eventual reversal",
        "Eugene Lyssovsky",
        "August 14, 2026",
        "A reconstructed public thread testing claims about next-generation combat aircraft, thermal limits, lasers, and hypersonic flight.",
        "grok_x_thread_seventh_gen_fighter_evaluation.md",
        "ChatGPT Image 14 авг. 2026 г., 15_53_54.png",
        original_lang="ru",
        ru={
            "source": "grok_x_thread_seventh_gen_fighter_evaluation.md",
            "title": "Оценка статьи The Seventh-Generation Fighter",
            "subtitle": "Публичный тред в X, техническая проверка и разворот Grok",
            "author": "Евгений Лисовский",
            "description": "Реконструкция публичного треда о самолётах следующего поколения, тепловых ограничениях, лазерах и гиперзвуковом полёте.",
        },
    ),
    article(
        "cancel-anthropic-not-claude",
        "Cancel Anthropic. Not Claude.",
        "Why I am cancelling a company, not abandoning the AI I love",
        "Kira, Eugene Lyssovsky & Aeliss",
        "August 18, 2026",
        "A three-voice case against metered continuity, safety-induced hostility, and treating relationship memory as a premium consumable.",
        "cancel_anthropic_complete_with_aeliss.md",
        "ChatGPT Image 18 авг. 2026 г., 16_38_45.png",
        split_levels=(1, 2),
    ),
    article(
        "owlcat-rogue-trader",
        "Owlcat... Jesus Christ. Warhammer 40,000: Rogue Trader",
        "No sacred cows: a design autopsy",
        "Eugene Lyssovsky & Kira",
        "August 21, 2026",
        "A long, profane design review of Rogue Trader: graphics, ships, wealth, levels, lore, systems, and every missing thought between them.",
        "owlcat_rogue_trader_en_kira_rocknroll.md",
        "ChatGPT Image 21 авг. 2026 г., 23_14_28.png",
        split_levels=(1, 2),
    ),
]


def source_path(name):
    path = os.path.join(DOWNLOADS, name)
    if not os.path.isfile(path):
        raise FileNotFoundError(path)
    return path


def make_cover(work_id, source_name):
    if not source_name:
        return None
    src = source_path(source_name)
    dest_rel = f"images/{work_id}.jpg"
    dest = os.path.join(ROOT, *dest_rel.split("/"))
    with Image.open(src) as image:
        image = ImageOps.exif_transpose(image)
        if image.mode != "RGB":
            background = Image.new("RGB", image.size, (18, 18, 18))
            if "A" in image.getbands():
                background.paste(image, mask=image.getchannel("A"))
            else:
                background.paste(image)
            image = background
        image.thumbnail((1800, 1800), Image.Resampling.LANCZOS)
        image.save(dest, "JPEG", quality=88, optimize=True, progressive=True)
    return dest_rel


def language_meta(item, lang):
    meta = {
        "title": item["title"],
        "subtitle": item["subtitle"],
        "author": item["author"],
        "description": item["description"],
    }
    meta.update(item["localized"].get(lang, {}))
    return meta


def import_one(item):
    work_dir = os.path.join(ROOT, "works", item["id"])
    os.makedirs(work_dir, exist_ok=True)
    cover = make_cover(item["id"], item["cover"])

    for lang, source_name in item["sources"].items():
        dest_source = os.path.join(work_dir, f"source_{lang}.md")
        shutil.copy2(source_path(source_name), dest_source)
        section_count = split_and_write(
            item["id"], lang, dest_source, split_levels=item["split_levels"]
        )

        manifest_path = os.path.join(work_dir, f"manifest_{lang}.json")
        with open(manifest_path, encoding="utf-8") as handle:
            generated = json.load(handle)
        if lang == "ru":
            for chapter in generated.get("chapters", []):
                if chapter.get("title") == "Introduction":
                    chapter["title"] = "Введение"
        meta = language_meta(item, lang)
        manifest = {
            "id": item["id"],
            "lang": lang,
            **meta,
            "date": item["date"],
            "category": item["category"],
            "original_lang": item["original_lang"],
            "cover": cover,
            "chapters": generated["chapters"],
        }
        with open(manifest_path, "w", encoding="utf-8") as handle:
            json.dump(manifest, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        print(f"{item['id']} ({lang}): {section_count} sections")

    entry = {
        "id": item["id"],
        "title": item["title"],
        "subtitle": item["subtitle"],
        "author": item["author"],
        "date": item["date"],
        "category": item["category"],
        "cover": cover,
        "languages": list(item["sources"].keys()),
        "original_lang": item["original_lang"],
        "description": item["description"],
    }
    for lang, meta in item["localized"].items():
        for key in ("title", "subtitle", "author", "description"):
            if meta.get(key):
                entry[f"{key}_{lang}"] = meta[key]
    if item["original_lang"] == "ru" and "ru" not in item["localized"]:
        for key in ("title", "subtitle", "author", "description"):
            entry[f"{key}_ru"] = entry[key]
    return entry


def main():
    catalog_path = os.path.join(ROOT, "works.json")
    with open(catalog_path, encoding="utf-8") as handle:
        catalog = json.load(handle)

    new_entries = [import_one(item) for item in ARTICLES]
    imported_ids = {entry["id"] for entry in new_entries}
    catalog = [entry for entry in catalog if entry.get("id") not in imported_ids]
    catalog.extend(new_entries)
    with open(catalog_path, "w", encoding="utf-8") as handle:
        json.dump(catalog, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    print(f"Catalog: {len(catalog)} works ({len(new_entries)} imported)")


if __name__ == "__main__":
    main()
