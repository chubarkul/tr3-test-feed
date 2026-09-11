#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Сборка тестового Google Merchant XML-фида (RSS 2.0, namespace g:)
по картинкам из папок tr 3/{defacto,fresh_scarf,manuka,sporthink}.

Все данные (цены, URL, GTIN, наличие) — ФЕЙКОВЫЕ, только для тестовой кампании.
Тайтлы/категории/цвета соответствуют тому, что реально нарисовано на картинке.

Меняется одна строка — IMAGE_BASE — и фид пересобирается под другой хостинг картинок.
"""
import html
import os
import random
from datetime import datetime, timedelta

# Куда залиты картинки. Внутри должен лежать defacto/, manuka/, fresh_scarf/, sporthink/
IMAGE_BASE = "https://raw.githubusercontent.com/chubarkul/tr3-test-feed/main/images"

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "feed_tr3_test.xml")

random.seed(20260911)  # воспроизводимые «фейковые» цены

SHOPS = {
    "manuka": dict(brand="Manuka", domain="manuka.com.tr", path="urun"),
    "defacto": dict(brand="DeFacto", domain="defacto.com.tr", path="p"),
    "fresh_scarf": dict(brand="Fresh Scarf", domain="freshscarf.com", path="products"),
    "sporthink": dict(brand="Sporthink", domain="sporthink.com", path="p"),
}

# (file_id, title, google_category_id, product_type, color, size, gender, age_group, price_range)
ITEMS = {
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
 ("16905","Deri Dokulu Omuz Çantası - Siyah",6551,"Kadın > Aksesuar > Çanta","Siyah","Std","female","adult",(1490,2690)),
 ("17111","Kruvaze Geniş Yakalı Uzun Kaban - Kahve",1604,"Kadın > Dış Giyim > Kaban","Kahve","L","female","adult",(4990,7990)),
 ("17294","Fiyonk Detaylı Puf Çanta - Haki",6551,"Kadın > Aksesuar > Çanta","Haki","Std","female","adult",(1690,2590)),
 ("17580","Bomber Kesim Ceket - Açık Haki",1604,"Kadın > Dış Giyim > Ceket","Açık Haki","M","female","adult",(2290,3490)),
 ("17655","Altın Kaplama Burgu Yüzük",200,"Kadın > Aksesuar > Takı","Altın","16","female","adult",(690,1290)),
 ("18247","Keten Dokulu Blazer Ceket - Siyah",1604,"Kadın > Dış Giyim > Ceket","Siyah","S","female","adult",(2690,3990)),
 ("18449","Fitilli Dizüstü Çorap - Gri",213,"Kadın > Giyim > Çorap","Gri","Std","female","adult",(290,490)),
 ("18460","Fitilli Kalın Çorap - Antrasit",213,"Kadın > Giyim > Çorap","Antrasit","Std","female","adult",(290,490)),
 ("18658","Fiyonk Detaylı Mini Çanta - Lacivert",6551,"Kadın > Aksesuar > Çanta","Lacivert","Std","female","adult",(1390,2190)),
 ("8593","Keten Dokulu Bol Paça Pantolon - Bej",204,"Kadın > Giyim > Pantolon","Bej","M","female","adult",(1490,2190)),
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
 ("G2630AXBR103","Çiçek Desenli Pamuklu Boxer - Ekru",213,"Erkek > İç Giyim > Boxer","Ekru","L","male","adult",(149,299)),
 ("G5917AXGN10","Pure Korean Anti Aging Yüz Maskesi 27 ml",2915,"Kozmetik > Cilt Bakımı > Maske","-","27 ml","unisex","adult",(59,129)),
 ("G6814A826SMBG399","Kız Çocuk Geniş Paça Jean Pantolon - Camel",5424,"Çocuk > Kız Çocuk > Jean","Camel","8-9 Yaş","female","kids",(399,699)),
 ("G9536A8NM55","Kız Çocuk Düz Paça Jean Pantolon - Mavi",5424,"Çocuk > Kız Çocuk > Jean","Mavi","9-10 Yaş","female","kids",(449,749)),
 ("G9704AXNSKR1","Kare Çerçeveli Güneş Gözlüğü - Kahve",178,"Aksesuar > Güneş Gözlüğü","Kahve","Std","unisex","adult",(399,699)),
 ("H0858AXER238","Normal Bel A Kesim Midi Etek - Ekru",1581,"Kadın > Giyim > Etek","Ekru","M","female","adult",(549,899)),
 ("H2754AXBR190","Fermuar Detaylı El Çantası - Bordo",6551,"Kadın > Aksesuar > Çanta","Bordo","Std","female","adult",(599,1099)),
 ("H2920A8BK81","Erkek Çocuk Basketbol Şortu - Siyah",5424,"Çocuk > Erkek Çocuk > Şort","Siyah","11-12 Yaş","male","kids",(249,449)),
 ("H4379AXBK27","Halka Detaylı Omuz Çantası - Siyah",6551,"Kadın > Aksesuar > Çanta","Siyah","Std","female","adult",(649,1149)),
 ("H5282AX26SPBE281","Kolsuz V Yaka Mini Elbise - Mavi",2271,"Kadın > Giyim > Elbise","Mavi","S","female","adult",(599,999)),
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
 ("43725558120583","Keten Dokulu Pamuklu Şal 190 cm - Bordo",167,"Kadın > Tesettür > Şal","Bordo","190 cm","female","adult",(319,569)),
 ("43725569228935","Desenli Viskon Şal 72x194 cm - Haki",167,"Kadın > Tesettür > Şal","Haki","72x194 cm","female","adult",(379,679)),
 ("43725586071687","Yumuşak Dokulu Düz Şal 190 cm - Vizon",167,"Kadın > Tesettür > Şal","Vizon","190 cm","female","adult",(299,549)),
 ("43725595803783","İç Göstermez Terletmeyen Şal 95x95 cm - Siyah",167,"Kadın > Tesettür > Şal","Siyah","95x95 cm","female","adult",(389,689)),
 ("43725633060999","Desenli Terletmeyen Şal 95x95 cm - Bej",167,"Kadın > Tesettür > Şal","Bej","95x95 cm","female","adult",(389,689)),
 ("43725638697095","Bambu Karışımlı Kolay Şekil Alan Şal - Antrasit",167,"Kadın > Tesettür > Şal","Antrasit","70x180 cm","female","adult",(429,749)),
 ("43725672317063","İpek Karışımlı Desenli Şal - Mürdüm",167,"Kadın > Tesettür > Şal","Mürdüm","90x90 cm","female","adult",(499,899)),
 ("43779845652615","Çiçek Desenli Hafif Şal 93x93 cm - Ekru",167,"Kadın > Tesettür > Şal","Ekru","93x93 cm","female","adult",(359,629)),
 ("43808094748807","Düz Renk Viskon Şal - Yağ Yeşili",167,"Kadın > Tesettür > Şal","Yağ Yeşili","70x190 cm","female","adult",(289,529)),
 ("44563089129607","Desenli Uzun Viskon Şal 193 cm - Haki",167,"Kadın > Tesettür > Şal","Haki","193 cm","female","adult",(349,619)),
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
 ("4067903166871","Erkek Trekking Ayakkabısı - Kahve",187,"Erkek > Ayakkabı > Outdoor","Kahve","43","male","adult",(3199,5299)),
 ("4067981522682","Erkek Futbol Forma Takımı - Lacivert",5697,"Erkek > Spor Giyim > Forma","Lacivert","M","male","adult",(1499,2499)),
 ("4067983745577","Çocuk Koşu Ayakkabısı - Beyaz / Siyah",187,"Çocuk > Ayakkabı > Koşu","Beyaz","34","unisex","kids",(1399,2299)),
 ("4068805166402","Antrenman Sırt Çantası - Bordo",100,"Spor > Aksesuar > Sırt Çantası","Bordo","Std","unisex","adult",(899,1599)),
 ("4069162805263","Erkek Koşu Ayakkabısı - Siyah",187,"Erkek > Ayakkabı > Koşu","Siyah","45","male","adult",(2599,4299)),
 ("5401246303521","Kadın Baskılı Tişört - Ekru",212,"Kadın > Spor Giyim > Tişört","Ekru","S","female","adult",(599,1099)),
 ("5715830354562","Erkek Kısa Kollu Gömlek - Mavi",212,"Erkek > Giyim > Gömlek","Mavi","L","male","adult",(999,1699)),
 ("8421225615725","Çocuk Sandalet - Lila",1933,"Çocuk > Ayakkabı > Sandalet","Lila","30","female","kids",(649,1099)),
 ("8682902954265","Kadın Jogger Eşofman Altı - Zümrüt",5697,"Kadın > Spor Giyim > Eşofman Altı","Zümrüt","M","female","adult",(1099,1899)),
 ("8683906668226","Erkek Outdoor Bot - Siyah",187,"Erkek > Ayakkabı > Bot","Siyah","43","male","adult",(2999,4899)),
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


def money(lo, hi):
    return round(random.uniform(lo, hi) / 10) * 10 - 0.01


def build():
    items = []
    idx = 0
    for shop, rows in ITEMS.items():
        meta = SHOPS[shop]
        for (fid, title, gcat, ptype, color, size, gender, age, prange) in rows:
            idx += 1
            price = money(*prange)
            has_sale = idx % 3 == 0
            sale = round(price * random.uniform(0.6, 0.85) / 10) * 10 - 0.01
            # наличие: ~85% in stock, остальное — out of stock / preorder
            avail = "in stock"
            if idx % 13 == 0:
                avail = "out of stock"
            elif idx % 17 == 0:
                avail = "preorder"
            link = "https://www.{d}/{p}/{s}-{i}".format(
                d=meta["domain"], p=meta["path"], s=slug(title), i=fid)
            img = "{b}/{f}/{i}.jpg".format(b=IMAGE_BASE, f=shop, i=fid)
            sale_end = (datetime(2026, 9, 11) + timedelta(days=30)).strftime("%Y-%m-%dT23:59:59+0300")

            x = []
            a = x.append
            a("    <item>")
            a("      <g:id>%s-%s</g:id>" % (shop.upper()[:3], fid))
            a("      <title>%s</title>" % esc(title))
            a("      <description>%s. %s koleksiyonundan, test amaçlı oluşturulmuş ürün kaydı.</description>"
              % (esc(title), esc(meta["brand"])))
            a("      <link>%s</link>" % esc(link))
            a("      <g:image_link>%s</g:image_link>" % esc(img))
            a("      <g:availability>%s</g:availability>" % avail)
            a("      <g:price>%.2f TRY</g:price>" % price)
            if has_sale:
                a("      <g:sale_price>%.2f TRY</g:sale_price>" % sale)
                a("      <g:sale_price_effective_date>2026-09-11T00:00:00+0300/%s</g:sale_price_effective_date>" % sale_end)
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
            a("      <g:quantity>%d</g:quantity>" % (0 if avail == "out of stock" else random.randint(3, 250)))
            a("      <g:shipping>")
            a("        <g:country>TR</g:country>")
            a("        <g:service>Standart Kargo</g:service>")
            a("        <g:price>%s</g:price>" % ("0.00 TRY" if price > 500 else "49.90 TRY"))
            a("      </g:shipping>")
            a("      <g:custom_label_0>%s</g:custom_label_0>" % esc(meta["brand"]))
            a("      <g:custom_label_1>%s</g:custom_label_1>" % ("indirim" if has_sale else "tam fiyat"))
            a("      <g:custom_label_2>%s</g:custom_label_2>" % esc(ptype.split(" > ")[0]))
            a("    </item>")
            items.append("\n".join(x))

    head = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0" xmlns:g="http://base.google.com/ns/1.0">',
        '  <channel>',
        '    <title>TR3 Test Feed — Yango Ads / AIR</title>',
        '    <link>https://example.com/tr3-test-feed</link>',
        '    <description>Тестовый фид на 80 офферов (4 бренда x 20). Данные фейковые, картинки реальные.</description>',
        '    <lastBuildDate>%s</lastBuildDate>' % datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0300"),
    ]
    tail = ['  </channel>', '</rss>', '']
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(head) + "\n" + "\n".join(items) + "\n" + "\n".join(tail))
    print("written: %s (%d offers)" % (OUT, len(items)))


if __name__ == "__main__":
    build()
