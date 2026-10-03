# -*- coding: utf-8 -*-
"""Bouwt dist/ uit site.zip.

Vanaf 02-10-2026 is site.zip de bron: een volledige kopie van de live site.
De eerdere generator staat in de git-geschiedenis.
Bijwerken: nieuwe site.zip uploaden en committen; Cloudflare draait
`python3 build.py` en publiceert dist/.
"""
import shutil
import zipfile

shutil.rmtree("dist", ignore_errors=True)
zipfile.ZipFile("site.zip").extractall("dist")
print("dist opgebouwd uit site.zip")
