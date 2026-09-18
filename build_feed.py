#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Сборка тестового Google Merchant XML-фида (RSS 2.0, namespace g:).

Версия 2 (18.09.2026): 70 офферов.
  - 40 старых картинок из `tr 3/` (по 10 на каждый из 4 брендов)
  - 30 новых картинок из `en/` (по 6 на бренд, включая новый бренд Mavi)

Все данные (цены, URL, GTIN, наличие) — ФЕЙКОВЫЕ, только для тестовой кампании.
Тайтлы/категории/цвета соответствуют тому, что реально нарисовано на картинке.
Тайтлы везде турецкие, в т.ч. у новых офферов (баннеры у них англоязычные).

Цены/наличие детерминированы от id оффера: пересборка не перетасовывает фид,
у старых офферов цифры остаются те же, что были в первой версии.

Меняется одна строка — IMAGE_BASE — и фид пересобирается под другой хостинг картинок.
"""
import html
import os
import random
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

# Куда залиты картинки. Внутри лежат defacto/, manuka/, fresh_scarf/, sporthink/, mavi/
IMAGE_BASE = "https://raw.githubusercontent.com/chubarkul/tr3-test-feed/main/images"

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "feed_tr3_test.xml")

SHOPS = {
    "manuka": dict(brand="Manuka", domain="manuka.com.tr", path="urun"),
    "defacto": dict(brand="DeFacto", domain="defacto.com.tr", path="p"),
    "fresh_scarf": dict(brand="Fresh Scarf", domain="freshscarf.com", path="products"),
    "sporthink": dict(brand="Sporthink", domain="sporthink.com", path="p"),
    "mavi": dict(brand="Mavi", domain="mavi.com", path="p"),
}

# (file_id, title, google_category_id, product_type, color, size, gender, age_group, price_range)
# OLD — картинки из `tr 3` (вертикальные турецкие баннеры), по 10 на бренд
OLD_ITEMS = {
"manuka": [
 ("10211","Kaşe Dokulu Oversize Blazer Ceket - Lacivert",1604,"Kadın > Dış Giyim > Ceket","Lacivert","M","female","adult",(2490,3990)),
 ("11052","Keten Dokulu Kolsuz Midi Elbise - Bej",2271,"Kadın > Giyim > Elbise","Bej","S","female","adult",(1790,2590)),
 ("11181","Deri Görünümlü Shopper Çanta - Siyah",6551,"Kadın > Aksesuar > Çanta","Siyah","Std","female","adult",(1990,3490)),
 ("12817","Fitilli Dokulu Mini Etek - Camel",1581,"Kadın > Giyim > Etek","Camel","M","female","adult",(1290,1890)),
 ("12960","Volan Detaylı Midi Etek - Ekru",1581,"Kadın > Giyim > Etek","Ekru","L","female","adult",(1490,2190)),
 ("13557","Uzun Kollu Body - Kahve",212,"Kadın > Giyim > Body","Kahve","S","female","adult",(890,1290)),
 ("14496","Keten Dokulu Beli Büzgülü Tunik - Haki",1604,"Kadın > Giyim > Tunik","Haki","M","female","adult",(1590,2290)),
 ("15367","Pileli Katlı Uzun Abiye Elbise - Kırık Beyaz",2271,"Kadın > Giyim > Abiye Elbise","Kırık Beyaz","M","female","adult",(3990,6490)),
 ("16373","Keten Dokulu Oversize Gömlek - Beyaz",212,"Kadın > Giyim > Gömlek","Beyaz","L","female","adult",(1390,1990)),
 ("16749","Kemerli Geniş Kollu Gömlek - Antrasit",212,"Kadın > Giyim > Gömlek","Antrasit","M","female","adult",(1690,2390)),
],
"defacto": [
 ("A0566AX26SPBK81","Slim Fit Dar Paça Eşofman Altı - Siyah",5697,"Kadın > Spor Giyim > Eşofman Altı","Siyah","M","female","adult",(599,999)),
 ("B5867A8GR525","Erkek Çocuk Esnek Belli Şort - Ekru",5424,"Çocuk > Erkek Çocuk > Şort","Ekru","9-10 Yaş","male","kids",(249,449)),
 ("B7786A8AR162","Kız Çocuk Yüksek Bel Tayt - Antrasit",5424,"Çocuk > Kız Çocuk > Tayt","Antrasit","7-8 Yaş","female","kids",(199,399)),
 ("C4474AX25WNBK27","Regular Fit Bisiklet Yaka Kazak - Siyah",212,"Kadın > Giyim > Kazak","Siyah","L","female","adult",(699,1199)),
 ("C7660AXBN564","Kısa Kollu Keten Görünümlü Gömlek - Turuncu",212,"Erkek > Giyim > Gömlek","Turuncu","M","male","adult",(549,899)),
 ("E0990AX25SMWT34","Regular Fit Düğmeli Triko Yelek - Beyaz",212,"Kadın > Giyim > Yelek","Beyaz","S","female","adult",(499,849)),
 ("E8355A5PN648","Bebek Kız Uzun Kollu Basic Tişört - Pembe",5424,"Bebek > Kız Bebek > Tişört","Pembe","12-18 Ay","female","infant",(149,279)),
 ("E8688A8BR194","Erkek Çocuk Kapüşonlu Şişme Mont - Bordo",5424,"Çocuk > Erkek Çocuk > Mont","Bordo","10-11 Yaş","male","kids",(899,1499)),
 ("F0236AXPN141","2'li Paket Dantel Detaylı Külot - Pudra",213,"Kadın > İç Giyim > Külot","Pudra","M","female","adult",(179,329)),
 ("F3969AXGD1","14 Ayar Altın Kaplama İnce Bileklik",200,"Kadın > Aksesuar > Takı","Altın","Std","female","adult",(399,749)),
],
"fresh_scarf": [
 ("43725440385159","Terletmeyen Dokuma Şal 75x75 cm - Zümrüt Yeşili",167,"Kadın > Tesettür > Şal","Zümrüt Yeşili","75x75 cm","female","adult",(349,649)),
 ("43725442711687","Yumuşak Dokulu Düz Şal 190 cm - Bordo",167,"Kadın > Tesettür > Şal","Bordo","190 cm","female","adult",(299,549)),
 ("43725451788423","Floş Pamuk Karışımlı Şal 73x200 cm - Haki",167,"Kadın > Tesettür > Şal","Haki","73x200 cm","female","adult",(349,599)),
 ("43725488324743","Çiçek Desenli Viskon Şal 72x194 cm - Lacivert",167,"Kadın > Tesettür > Şal","Lacivert","72x194 cm","female","adult",(379,679)),
 ("43725504872583","İpeksi Jakarlı Şal - Gri",167,"Kadın > Tesettür > Şal","Gri","70x180 cm","female","adult",(399,699)),
 ("43725507887239","Kendinden Kırışık Dokulu Şal 190 cm - Pudra",167,"Kadın > Tesettür > Şal","Pudra","190 cm","female","adult",(329,589)),
 ("43725517357191","Etnik Desenli Akışkan Şal - Ekru",167,"Kadın > Tesettür > Şal","Ekru","70x190 cm","female","adult",(289,529)),
 ("43725524140167","Desenli Viskon Şal 95x95 cm - Kahve",167,"Kadın > Tesettür > Şal","Kahve","95x95 cm","female","adult",(359,629)),
 ("43725524172935","Çiçek Desenli Şal 72x194 cm - Siyah",167,"Kadın > Tesettür > Şal","Siyah","72x194 cm","female","adult",(379,679)),
 ("43725556940935","Floş Pamuk Şal 73x200 cm - Gri",167,"Kadın > Tesettür > Şal","Gri","73x200 cm","female","adult",(349,599)),
],
"sporthink": [
 ("191448735651","Çocuk Terlik - Lila",1933,"Çocuk > Ayakkabı > Terlik","Lila","31","female","kids",(499,899)),
 ("197804464081","Unisex Bilekli Sneaker - Siyah",187,"Ayakkabı > Sneaker","Siyah","42","unisex","adult",(2199,3499)),
 ("197862929119","Erkek Koşu Ayakkabısı - Antrasit",187,"Erkek > Ayakkabı > Koşu","Antrasit","43","male","adult",(3499,5999)),
 ("198633912958","Erkek Koşu Ayakkabısı - Siyah",187,"Erkek > Ayakkabı > Koşu","Siyah","44","male","adult",(2999,4999)),
 ("198688415459","Unisex Günlük Spor Ayakkabı - Gri",187,"Ayakkabı > Sneaker","Gri","41","unisex","adult",(3299,5499)),
 ("198739960242","Kız Çocuk Spor Ayakkabı - Lila",187,"Çocuk > Ayakkabı > Spor Ayakkabı","Lila","33","female","kids",(1299,2199)),
 ("4052605639136","Çocuk Cırt Cırtlı Sandalet - Gri",1933,"Çocuk > Ayakkabı > Sandalet","Gri","29","unisex","kids",(699,1199)),
 ("4066746467275","3'lü Paket Antrenman Çorabı - Beyaz",213,"Spor > Aksesuar > Çorap","Beyaz","40-42","unisex","adult",(299,549)),
 ("4067887357500","Erkek Antrenman Şortu - Siyah",5697,"Erkek > Spor Giyim > Şort","Siyah","L","male","adult",(799,1399)),
 ("4067889667706","Erkek Koşu Ayakkabısı - Siyah / Beyaz",187,"Erkek > Ayakkabı > Koşu","Siyah","42","male","adult",(2799,4599)),
],
}

# NEW — картинки из `en` (горизонтальные англоязычные баннеры), по 6 на бренд
NEW_ITEMS = {
"manuka": [
 ("12816","Fitilli Dokulu Uzun Etek - Krem",1581,"Kadın > Giyim > Etek","Krem","M","female","adult",(1590,2390)),
 ("16203","Altın Kaplama Madalyon Kolye",200,"Kadın > Aksesuar > Takı","Altın","Std","female","adult",(790,1490)),
 ("16577","Kruvaze Detaylı Bol Paça Pantolon - Kahve",204,"Kadın > Giyim > Pantolon","Kahve","M","female","adult",(1890,2790)),
 ("16854","Kısa Boy Kaban - Siyah",1604,"Kadın > Dış Giyim > Kaban","Siyah","S","female","adult",(3990,5990)),
 ("18472","Yüksek Bel Bol Kesim Pantolon - Haki",204,"Kadın > Giyim > Pantolon","Haki","L","female","adult",(1490,2290)),
 ("18549","Dantel Detaylı Desenli Şal - Beyaz",167,"Kadın > Aksesuar > Şal","Beyaz","Std","female","adult",(890,1590)),
],
"defacto": [
 ("F7608AXBN341","Saten Görünümlü Dantel Detaylı Atlet - Kahve",213,"Kadın > İç Giyim > Atlet","Kahve","M","female","adult",(299,549)),
 ("F9835AXPN186","Regular Fit Pamuklu Pantolon - Pembe",204,"Kadın > Giyim > Pantolon","Pembe","S","female","adult",(499,899)),
 ("G2999AXBK81","Kolsuz Saten Görünümlü Bluz - Siyah",212,"Kadın > Giyim > Bluz","Siyah","M","female","adult",(549,949)),
 ("G6134A526SPER98","Erkek Çocuk Baskılı Oversize Tişört - Ekru",5424,"Çocuk > Erkek Çocuk > Tişört","Ekru","6-7 Yaş","male","kids",(199,379)),
 ("G7436A5RD345","Kız Çocuk 2'li Tişört ve Pantolon Takımı - Kırmızı",5424,"Çocuk > Kız Çocuk > Takım","Kırmızı","4-5 Yaş","female","kids",(399,699)),
 ("H4043A826SMPN105","Çocuk Desenli Pamuklu Bandana - Pudra",167,"Çocuk > Aksesuar > Bandana","Pudra","Std","unisex","kids",(99,199)),
],
"fresh_scarf": [
 ("43725505593479","Kendinden Kırışık Dokulu Şal 190 cm - Bej",167,"Kadın > Tesettür > Şal","Bej","190 cm","female","adult",(329,589)),
 ("43725520732295","İç Göstermez Serin Tutan Şal 95x95 cm - Ekru",167,"Kadın > Tesettür > Şal","Ekru","95x95 cm","female","adult",(379,669)),
 ("43725530333319","Desenli Viskon Şal 72x194 cm - Antrasit",167,"Kadın > Tesettür > Şal","Antrasit","72x194 cm","female","adult",(379,679)),
 ("43725558579335","Çiçek Desenli Viskon Şal 72x194 cm - Siyah",167,"Kadın > Tesettür > Şal","Siyah","72x194 cm","female","adult",(379,679)),
 ("43725568180359","Düz Renk Şal 105x185 cm - Krem",167,"Kadın > Tesettür > Şal","Krem","105x185 cm","female","adult",(419,729)),
 ("43725595508871","Çiçek Desenli Viskon Şal 72x194 cm - Kahve",167,"Kadın > Tesettür > Şal","Kahve","72x194 cm","female","adult",(379,679)),
],
"sporthink": [
 ("197627551227","Çocuk Cırt Cırtlı Spor Ayakkabı - Lila",187,"Çocuk > Ayakkabı > Spor Ayakkabı","Lila","32","female","kids",(1299,2199)),
 ("4069161956324","Kız Çocuk Baskılı Tişört - Kırmızı",5424,"Çocuk > Spor Giyim > Tişört","Kırmızı","7-8 Yaş","female","kids",(399,749)),
 ("5715603342611","Erkek Kapüşonlu Sweatshirt - Siyah",5697,"Erkek > Spor Giyim > Sweatshirt","Siyah","L","male","adult",(1499,2499)),
 ("8683031010600","Erkek Hafif Yürüyüş Ayakkabısı - Siyah",187,"Erkek > Ayakkabı > Yürüyüş","Siyah","43","male","adult",(2499,3999)),
 ("8684571007693","Erkek Dik Yakalı Sweatshirt - Siyah",5697,"Erkek > Spor Giyim > Sweatshirt","Siyah","M","male","adult",(1299,2199)),
 ("8720245437837","2'li Paket Boxer - Beyaz",213,"Erkek > İç Giyim > Boxer","Beyaz","L","male","adult",(499,899)),
],
"mavi": [
 ("8684434177051","Erkek Baskılı Relaxed Fit Tişört - Siyah",212,"Erkek > Giyim > Tişört","Siyah","L","male","adult",(699,1199)),
 ("8684518154732","Erkek Düğmeli Polo Yaka Tişört - Ekru",212,"Erkek > Giyim > Polo Tişört","Ekru","M","male","adult",(899,1499)),
 ("8684713643598","Erkek Slim Fit Jean Pantolon - Koyu Lacivert",2271,"Erkek > Giyim > Jean","Koyu Lacivert","32/32","male","adult",(1899,2999)),
 ("8684908742068","Erkek Relaxed Fit Polo Yaka Tişört - Bej",212,"Erkek > Giyim > Polo Tişört","Bej","L","male","adult",(899,1499)),
 ("8684908799918","Erkek Lyocell Karışımlı Bisiklet Yaka Tişört - Gri",212,"Erkek > Giyim > Tişört","Gri","M","male","adult",(799,1299)),
 ("8685099011209","Erkek Baskılı Bisiklet Yaka Tişört - Bordo",212,"Erkek > Giyim > Tişört","Bordo","XL","male","adult",(699,1199)),
],
}


def slug(text):
    tr = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")
    t = text.translate(tr).lower()
    out = []
    for ch in t:
        if ch.isalnum():
            out.append(ch)
        elif ch in " -/":
            out.append("-")
    s = "".join(out)
    while "--" in s:
        s = s.replace("--", "-")
    return s.strip("-")


def gtin13(seed_str):
    """Фейковый, но валидный по контрольной цифре EAN-13."""
    rnd = random.Random(seed_str)
    body = "869" + "".join(str(rnd.randint(0, 9)) for _ in range(9))
    total = sum(int(d) * (3 if i % 2 else 1) for i, d in enumerate(body))
    return body + str((10 - total % 10) % 10)


def esc(s):
    return html.escape(str(s), quote=False)


def load_previous():
    """Цены/наличие ранее опубликованных офферов, чтобы старые не перетряхивать."""
    if not os.path.exists(OUT):
        return {}
    g = "{http://base.google.com/ns/1.0}"
    prev = {}
    for it in ET.parse(OUT).getroot().findall(".//item"):
        oid = it.find(g + "id").text
        def get(tag):
            node = it.find(g + tag)
            return node.text if node is not None else None
        prev[oid] = dict(
            price=get("price"),
            sale_price=get("sale_price"),
            availability=get("availability"),
            quantity=get("quantity"),
        )
    return prev


def commercials(offer_id, prange, prev):
    """Цена / скидка / наличие / остаток. Детерминированы от id оффера."""
    if offer_id in prev and prev[offer_id]["price"]:
        p = prev[offer_id]
        return p["price"], p["sale_price"], p["availability"], p["quantity"]

    rnd = random.Random("tr3::" + offer_id)
    price = round(rnd.uniform(*prange) / 10) * 10 - 0.01
    sale = None
    if rnd.random() < 0.33:
        sale = "%.2f TRY" % (round(price * rnd.uniform(0.6, 0.85) / 10) * 10 - 0.01)
    roll = rnd.random()
    avail = "out of stock" if roll < 0.08 else ("preorder" if roll < 0.14 else "in stock")
    qty = 0 if avail == "out of stock" else rnd.randint(3, 250)
    return "%.2f TRY" % price, sale, avail, str(qty)


def build():
    items = []
    stats = {"old": 0, "new": 0}
    prev = load_previous()

    rows = []
    for shop in SHOPS:
        for row in OLD_ITEMS.get(shop, []):
            rows.append((shop, "old", row))
        for row in NEW_ITEMS.get(shop, []):
            rows.append((shop, "new", row))

    for shop, vintage, (fid, title, gcat, ptype, color, size, gender, age, prange) in rows:
        meta = SHOPS[shop]
        offer_id = "%s-%s" % (shop.upper()[:3], fid)
        price, sale, avail, qty = commercials(offer_id, prange, prev)
        stats[vintage] += 1

        link = "https://www.{d}/{p}/{s}-{i}".format(
            d=meta["domain"], p=meta["path"], s=slug(title), i=fid)
        img = "{b}/{f}/{i}.jpg".format(b=IMAGE_BASE, f=shop, i=fid)
        sale_end = (datetime(2026, 9, 18) + timedelta(days=30)).strftime("%Y-%m-%dT23:59:59+0300")

        x = []
        a = x.append
        a("    <item>")
        a("      <g:id>%s</g:id>" % offer_id)
        a("      <title>%s</title>" % esc(title))
        a("      <description>%s. %s koleksiyonundan, test amaçlı oluşturulmuş ürün kaydı.</description>"
          % (esc(title), esc(meta["brand"])))
        a("      <link>%s</link>" % esc(link))
        a("      <g:image_link>%s</g:image_link>" % esc(img))
        a("      <g:availability>%s</g:availability>" % avail)
        a("      <g:price>%s</g:price>" % price)
        if sale:
            a("      <g:sale_price>%s</g:sale_price>" % sale)
            a("      <g:sale_price_effective_date>2026-09-18T00:00:00+0300/%s</g:sale_price_effective_date>" % sale_end)
        a("      <g:brand>%s</g:brand>" % esc(meta["brand"]))
        a("      <g:gtin>%s</g:gtin>" % gtin13(shop + fid))
        a("      <g:mpn>%s</g:mpn>" % esc(fid))
        a("      <g:condition>new</g:condition>")
        a("      <g:google_product_category>%d</g:google_product_category>" % gcat)
        a("      <g:product_type>%s</g:product_type>" % esc(ptype))
        if color != "-":
            a("      <g:color>%s</g:color>" % esc(color))
        a("      <g:size>%s</g:size>" % esc(size))
        a("      <g:gender>%s</g:gender>" % gender)
        a("      <g:age_group>%s</g:age_group>" % age)
        a("      <g:item_group_id>%s-%s</g:item_group_id>" % (shop.upper()[:3], fid[:6]))
        a("      <g:quantity>%s</g:quantity>" % qty)
        a("      <g:shipping>")
        a("        <g:country>TR</g:country>")
        a("        <g:service>Standart Kargo</g:service>")
        a("        <g:price>%s</g:price>" % ("0.00 TRY" if float(price.split()[0]) > 500 else "49.90 TRY"))
        a("      </g:shipping>")
        a("      <g:custom_label_0>%s</g:custom_label_0>" % esc(meta["brand"]))
        a("      <g:custom_label_1>%s</g:custom_label_1>" % ("indirim" if sale else "tam fiyat"))
        a("      <g:custom_label_2>%s</g:custom_label_2>" % esc(ptype.split(" > ")[0]))
        a("      <g:custom_label_3>%s</g:custom_label_3>" % vintage)
        a("    </item>")
        items.append("\n".join(x))

    head = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0" xmlns:g="http://base.google.com/ns/1.0">',
        '  <channel>',
        '    <title>TR3 Test Feed — Yango Ads / AIR</title>',
        '    <link>https://example.com/tr3-test-feed</link>',
        '    <description>Тестовый фид на %d офферов (5 брендов). Данные фейковые, картинки реальные.</description>' % len(items),
        '    <lastBuildDate>%s</lastBuildDate>' % datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0300"),
    ]
    tail = ['  </channel>', '</rss>', '']
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(head) + "\n" + "\n".join(items) + "\n" + "\n".join(tail))
    print("written: %s (%d offers: %d old + %d new)"
          % (OUT, len(items), stats["old"], stats["new"]))


if __name__ == "__main__":
    build()
