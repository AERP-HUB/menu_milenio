#!/usr/bin/env python3
"""Genera las versiones WebP y AVIF (completa y de 480 px) de cada .jpg de la carpeta img/.

Uso:   pip install pillow          (Pillow >= 11.3 incluye AVIF; si no, solo se crea WebP)
       python3 optimizar-imagenes.py img/

Por cada img/foto.jpg crea:  foto.webp, foto-480.webp, foto.avif, foto-480.avif
index.html ya está preparado: usa <picture> con AVIF -> WebP -> JPG, y si algún archivo
no existe cae solo al siguiente formato, así que puedes subir los archivos poco a poco.
"""
import sys, pathlib
from PIL import Image, features

folder = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'img')
AVIF = features.check('avif')
if not AVIF:
    print('Aviso: tu Pillow no soporta AVIF; solo se generará WebP.')
BIG, SMALL = 1200, 480
tot_in = tot_out = 0
for src in sorted(list(folder.glob('*.jpg')) + list(folder.glob('*.jpeg'))):
    im = Image.open(src).convert('RGB')
    for width, suf in ((BIG, ''), (SMALL, '-480')):
        r = im.copy()
        if r.width > width:
            r = r.resize((width, round(r.height * width / r.width)), Image.LANCZOS)
        base = src.with_suffix('').as_posix() + suf
        r.save(base + '.webp', 'WEBP', quality=78, method=6); tot_out += pathlib.Path(base + '.webp').stat().st_size
        if AVIF:
            r.save(base + '.avif', 'AVIF', quality=55); tot_out += pathlib.Path(base + '.avif').stat().st_size
    tot_in += src.stat().st_size
    print('OK', src.name)
print(f'JPG originales: {tot_in/1024:.0f} KB · versiones modernas generadas: {tot_out/1024:.0f} KB')
