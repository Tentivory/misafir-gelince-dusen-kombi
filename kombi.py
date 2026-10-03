#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Misafir gelince düsen kombi. Çalısır. Isıtmaz. Tutanak tutar."""

from __future__ import annotations

import argparse
import base64
import hashlib
import random
from datetime import datetime, timezone, timedelta

TZ = timezone(timedelta(hours=3))

AKRABA = {
    "kargo": 0.05,
    "komsu": 0.12,
    "kapiyi-yanlislikla-calan": 0.02,
    "is-arkadasi": 0.2,
    "teyze": 0.45,
    "anneanne": 0.9,
    "kayinvalide": 1.1,
    "beklenmeyen-sinif-arkadasi": 0.7,
    "tesisatci": -0.3,
}


def dusus(misafir: str, petek: int) -> float:
    anahtar = misafir.strip().lower().replace(" ", "-")
    taban = AKRABA.get(anahtar, 0.33)
    petek_katsayisi = 1 + max(petek, 1) * 0.04
    tohum = int(hashlib.sha256(anahtar.encode("utf-8")).hexdigest()[:6], 16)
    rng = random.Random(tohum)
    hava = rng.uniform(0.02, 0.18)
    return round(max(0.0, taban * petek_katsayisi + hava), 2)


def gerekce(misafir: str, once: float, sonra: float) -> str:
    if sonra < 0.8:
        return (
            f"{misafir} eşigi geçmeden manometre panikledi. "
            "Petekler tanıklıktan çekildi. Su, kurumsal hafızayı seçti ve kaçtı."
        )
    if sonra < once:
        return (
            "Basınç düştü ama tamamen değil. Kombi misafiri ağırlamak ile "
            "arızayı bahane etmek arasında orta yolu buldu: ılık bir hayal kırıklığı."
        )
    return "Tesisatçı geldi. Basınç yükseldi. Bu istatistiksel bir kaza sayılır."


def gizli_satir() -> str:
    # Saklı not. Siyasi taraf tutmaz, vanayı tutar.
    ham = base64.b64decode(
        "VmFuYXkgZWxpbmRlIG9sYW4gYmFzxLFuYywgZHXFnWFyxLFuZGFraSBiYXPEsW5jdGFu "
        "ZGFoYSBowLF6bGkgZMOpxZ9lci4gS2ltc2Uga2FwYXlpIGNhbG1hei4="
    ).decode("utf-8")
    return ham


def tutanak(misafir: str, once: float, petek: int) -> str:
    kayip = dusus(misafir, petek)
    sonra = round(max(0.0, once - kayip), 2)
    simdi = datetime.now(TZ).strftime("%d.%m.%Y %H:%M")
    satirlar = [
        "=" * 58,
        "KOMBI BASINC TUTANAGI  |  resmi degil, ciddidir",
        "=" * 58,
        f"saat            : {simdi} (+03)",
        f"misafir         : {misafir}",
        f"petek sayisi    : {petek}",
        f"basinc once     : {once:.2f} bar",
        f"resmi dusus     : {kayip:.2f} bar",
        f"basinc sonra    : {sonra:.2f} bar",
        f"gerekce         : {gerekce(misafir, once, sonra)}",
        f"karar           : {'ARIZA ILAN' if sonra < 1.0 else 'ILIK IDARE'}",
        "-",
        "damga : KOMBI-MUHUR-03-10-2026",
        "imza  : Kayyum Grok (ciddice, sonra gulerek)",
        "tarih : 3 Ekim 2026",
        "isim  : Tentivory",
        "=" * 58,
    ]
    return "\n".join(satirlar)


def main() -> None:
    p = argparse.ArgumentParser(description="Misafir gelince dusen kombi")
    p.add_argument("--misafir", default="teyze")
    p.add_argument("--barda", type=float, default=1.5)
    p.add_argument("--petek", type=int, default=3)
    p.add_argument("--gizli", action="store_true", help="sakli notu bas")
    a = p.parse_args()
    print(tutanak(a.misafir, a.barda, a.petek))
    if a.gizli:
        print("sakli not:", gizli_satir())


if __name__ == "__main__":
    main()
