#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Сборка тестового Google Merchant XML-фида (RSS 2.0, namespace g:).

Версия 3 (24.09.2026): 20 офферов, Сербия.
Источник картинок — `~/Downloads/sr 2/bpolar`, магазин мультибрендовый (bpolar.rs),
бренд задаётся на уровне оффера. Турецкая партия (70 офферов) удалена целиком.

Все данные (цены, URL, GTIN, наличие) — ФЕЙКОВЫЕ, только для тестовой кампании.
Тайтлы/категории/цвета соответствуют тому, что реально нарисовано на картинке.
Тайтлы сербские, валюта RSD — как на баннерах.

Цены/наличие детерминированы от id оффера: пересборка не перетасовывает фид.

Меняется одна строка — IMAGE_BASE — и фид пересобирается под другой хостинг картинок.
"""
import html
import os
import random
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

# Куда залиты картинки. Внутри лежит bpolar/
IMAGE_BASE = "https://raw.githubusercontent.com/chubarkul/tr3-test-feed/main/images"

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "feed_tr3_test.xml")  # имя сохранено: на него настроена кампания

SHOP = dict(slug="bpolar", domain="bpolar.rs", path="proizvod")
CURRENCY = "RSD"
FREE_SHIPPING_FROM = 5000        # выше этой суммы доставка бесплатная
SHIPPING_FEE = "390.00 RSD"

# (file_id, brand, title, google_category_id, product_type, color, size, gender, age_group, price_range)
ITEMS = [
 ("207937-001","Crocs","Crocs Echo Clog Vodootporne Klompe - Crne",187,"Obuća > Klompe","Crna","43","unisex","adult",(9990,13990)),
 ("3WG10815373","On","On Cloudmonster Patike - Roze",187,"Obuća > Patike","Roze","39","female","adult",(24990,29990)),
 ("403688-05","Puma","Puma Speedcat Patike od Prevrnute Kože - Bordo",187,"Obuća > Patike","Bordo","42","unisex","adult",(12990,16990)),
 ("60856200","New Era","New Era Šorts sa Camo Printom - Sivi",207,"Muškarci > Odeća > Šorts","Siva","L","male","adult",(5990,8990)),
 ("80D2420030-D001","Moon Boot","Moon Boot Evolution Papuče - Crvene",187,"Obuća > Papuče","Crvena","40","unisex","adult",(9990,13990)),
 ("A555C24TBU-WHT","Stance","Stance Uniseks Čarape sa Prugama - Bele",213,"Odeća > Čarape","Bela","M (38-42)","unisex","adult",(1790,2690)),
 ("A556A20VIN-NAT","Stance","Stance Pamučne Čarape sa Printom - Bež",213,"Odeća > Čarape","Bež","L (43-47)","unisex","adult",(1790,2690)),
 ("EK00082LL831","Eastpak","Eastpak Transit'R L Kofer 75 cm - Teget",5181,"Torbe i Koferi > Kofer","Teget","75 cm / 121 L","unisex","adult",(19990,25990)),
 ("EK0A5BJEC0J1","Eastpak","Eastpak Cabin Kofer 34 L - Srebrni",5181,"Torbe i Koferi > Kofer","Srebrna","55 cm / 34 L","unisex","adult",(22990,28990)),
 ("EK0A5BJG4S11","Eastpak","Eastpak Tvrdi Kofer 90 L - Tamno Sivi",5181,"Torbe i Koferi > Kofer","Tamno siva","75 cm / 90 L","unisex","adult",(27990,34990)),
 ("F00890-1062","Scholl","Scholl Papuče od Prevrnute Kože - Kamel",187,"Obuća > Papuče","Kamel","41","unisex","adult",(8990,12990)),
 ("F32570-1004","Scholl","Scholl Papuče sa Kopčom - Crne",187,"Obuća > Papuče","Crna","42","unisex","adult",(8990,12990)),
 ("IF1310-696","Nike","Nike Šorts sa Printom - Šareni",207,"Žene > Odeća > Šorts","Šarena","M","female","adult",(5990,8990)),
 ("J2660-248","Fred Perry","Fred Perry Harrington Jakna - Teget",203,"Muškarci > Odeća > Jakna","Teget","M","male","adult",(29990,37990)),
 ("K2136IW-133","K-Way","K-Way Duga Prošivena Jakna - Siva",203,"Žene > Odeća > Jakna","Siva","L","female","adult",(39990,49990)),
 ("M12-G33","Fred Perry","Fred Perry Polo Majica - Bela",212,"Muškarci > Odeća > Polo Majica","Bela","L","male","adult",(12990,16990)),
 ("M3481-129","Fred Perry","Fred Perry Majica Kratkih Rukava - Bela",212,"Muškarci > Odeća > Majica","Bela","M","male","adult",(8990,11990)),
 ("M3600-87C","Fred Perry","Fred Perry Polo Majica - Crna",212,"Muškarci > Odeća > Polo Majica","Crna","XL","male","adult",(12990,16990)),
 ("M6006-350","Fred Perry","Fred Perry Polo Majica Dugih Rukava - Crna",212,"Muškarci > Odeća > Polo Majica","Crna","M","male","adult",(15990,19990)),
 ("WN0060","Wall Notion","Dečja Majica sa Printom - Bela",5424,"Deca > Odeća > Majica","Bela","134-140 cm","unisex","kids",(3990,5990)),
]


def slug(text):
    sr = str.maketrans("čćđšžČĆĐŠŽ", "ccdszCCDSZ")
    t = text.translate(sr).lower()
    out = []
    for ch in t:
        if ch.isalnum():
            out.append(ch)
        elif ch in " -/'":
            out.append("-")
    s = "".join(out)
    while "--" in s:
        s = s.replace("--", "-")
    return s.strip("-")


def gtin13(seed_str):
    """Фейковый, но валидный по контрольной цифре EAN-13."""
    rnd = random.Random(seed_str)
    body = "860" + "".join(str(rnd.randint(0, 9)) for _ in range(9))
    total = sum(int(d) * (3 if i % 2 else 1) for i, d in enumerate(body))
    return body + str((10 - total % 10) % 10)


def esc(s):
    return html.escape(str(s), quote=False)


def load_previous():
    """Цены/наличие ранее опубликованных офферов, чтобы не перетряхивать их при пересборке."""
    if not os.path.exists(OUT):
        return {}
    g = "{http://base.google.com/ns/1.0}"
    prev = {}
    for it in ET.parse(OUT).getroot().findall(".//item"):
        def get(tag):
            node = it.find(g + tag)
            return node.text if node is not None else None
        prev[it.find(g + "id").text] = dict(
            price=get("price"), sale_price=get("sale_price"),
            availability=get("availability"), quantity=get("quantity"))
    return prev


def commercials(offer_id, prange, prev):
    """Цена / скидка / наличие / остаток. Детерминированы от id оффера."""
    if offer_id in prev and prev[offer_id]["price"]:
        p = prev[offer_id]
        return p["price"], p["sale_price"], p["availability"], p["quantity"]

    rnd = random.Random("sr2::" + offer_id)
    price = round(rnd.uniform(*prange) / 100) * 100 - 10      # цены вида 24990
    sale = None
    if rnd.random() < 0.33:
        sale = "%.2f %s" % (round(price * rnd.uniform(0.6, 0.85) / 100) * 100 - 10, CURRENCY)
    roll = rnd.random()
    avail = "out of stock" if roll < 0.08 else ("preorder" if roll < 0.14 else "in stock")
    qty = 0 if avail == "out of stock" else rnd.randint(3, 250)
    return "%.2f %s" % (price, CURRENCY), sale, avail, str(qty)


def build():
    prev = load_previous()
    items = []
    sale_end = (datetime(2026, 9, 24) + timedelta(days=30)).strftime("%Y-%m-%dT23:59:59+0200")

    for (fid, brand, title, gcat, ptype, color, size, gender, age, prange) in ITEMS:
        offer_id = "BPO-%s" % fid
        price, sale, avail, qty = commercials(offer_id, prange, prev)

        link = "https://www.{d}/{p}/{s}-{i}".format(
            d=SHOP["domain"], p=SHOP["path"], s=slug(title), i=fid.lower())
        img = "{b}/{f}/{i}.jpg".format(b=IMAGE_BASE, f=SHOP["slug"], i=fid)

        x = []
        a = x.append
        a("    <item>")
        a("      <g:id>%s</g:id>" % offer_id)
        a("      <title>%s</title>" % esc(title))
        a("      <description>%s. Test proizvod, podaci su generisani za proveru kampanje.</description>"
          % esc(title))
        a("      <link>%s</link>" % esc(link))
        a("      <g:image_link>%s</g:image_link>" % esc(img))
        a("      <g:availability>%s</g:availability>" % avail)
        a("      <g:price>%s</g:price>" % price)
        if sale:
            a("      <g:sale_price>%s</g:sale_price>" % sale)
            a("      <g:sale_price_effective_date>2026-09-24T00:00:00+0200/%s</g:sale_price_effective_date>" % sale_end)
        a("      <g:brand>%s</g:brand>" % esc(brand))
        a("      <g:gtin>%s</g:gtin>" % gtin13(fid))
        a("      <g:mpn>%s</g:mpn>" % esc(fid))
        a("      <g:condition>new</g:condition>")
        a("      <g:google_product_category>%d</g:google_product_category>" % gcat)
        a("      <g:product_type>%s</g:product_type>" % esc(ptype))
        a("      <g:color>%s</g:color>" % esc(color))
        a("      <g:size>%s</g:size>" % esc(size))
        a("      <g:gender>%s</g:gender>" % gender)
        a("      <g:age_group>%s</g:age_group>" % age)
        a("      <g:item_group_id>BPO-%s</g:item_group_id>" % fid.split("-")[0])
        a("      <g:quantity>%s</g:quantity>" % qty)
        a("      <g:shipping>")
        a("        <g:country>RS</g:country>")
        a("        <g:service>Standardna dostava</g:service>")
        a("        <g:price>%s</g:price>"
          % ("0.00 %s" % CURRENCY if float(price.split()[0]) > FREE_SHIPPING_FROM else SHIPPING_FEE))
        a("      </g:shipping>")
        a("      <g:custom_label_0>%s</g:custom_label_0>" % esc(brand))
        a("      <g:custom_label_1>%s</g:custom_label_1>" % ("akcija" if sale else "puna cena"))
        a("      <g:custom_label_2>%s</g:custom_label_2>" % esc(ptype.split(" > ")[0]))
        a("    </item>")
        items.append("\n".join(x))

    head = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0" xmlns:g="http://base.google.com/ns/1.0">',
        '  <channel>',
        '    <title>bpolar Test Feed — Yango Ads / AIR</title>',
        '    <link>https://www.bpolar.rs</link>',
        '    <description>Тестовый фид на %d офферов (Сербия, RSD). Данные фейковые, картинки реальные.</description>' % len(items),
        '    <lastBuildDate>%s</lastBuildDate>' % datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0200"),
    ]
    tail = ['  </channel>', '</rss>', '']
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(head) + "\n" + "\n".join(items) + "\n" + "\n".join(tail))
    print("written: %s (%d offers)" % (OUT, len(items)))


if __name__ == "__main__":
    build()
