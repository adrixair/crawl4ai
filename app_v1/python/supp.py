#!/usr/bin/env python3
"""
Copie tous les .ppt / .pptx du dossier PRO3584 (et sous-dossiers)
vers ~/Documents/PRO3584_PowerPoints, sans écraser les doublons.
"""

from pathlib import Path
import shutil
import os

# 1) Chemins source et destination
# NB : le dossier MoodleUSP est dans iCloud Drive ▸ « Documents »
SOURCE = Path("/Users/adrien/Library/Mobile Documents/com~apple~CloudDocs/"
              "Documents/MoodleUSP/PRO3584 - Projeto, Processo e Gestão da Inovação (2025)")

DEST = Path.home() / "Documents" / "PRO3584_PowerPoints"

# Vérifications préalables
print(f"SOURCE = {SOURCE}")
if not SOURCE.exists():
    raise FileNotFoundError(f"❌ Dossier source introuvable : {SOURCE}")
print("✅ Dossier source OK")


print(f"DEST   = {DEST}")

# -- Diagnostic rapide : combien de PPT trouvés ? --
all_ppts = [p for p in SOURCE.rglob('*') if p.suffix.lower() in ('.ppt', '.pptx')]
print(f"👉 {len(all_ppts)} fichier(s) .ppt/.pptx repéré(s) (liste tronquée) :")
for p in all_ppts[:10]:
    print("   •", p.relative_to(SOURCE))
if not all_ppts:
    print("   ⚠️  Aucune présentation repérée — vérifie que les fichiers sont bien téléchargés dans iCloud ou que le chemin SOURCE est correct.")

# 2) Crée le dossier de destination s'il n'existe pas
DEST.mkdir(parents=True, exist_ok=True)

# 3) Parcourt récursivement et copie les .ppt / .pptx
count_new = 0
count_skip = 0
for ext in ("*.ppt", "*.pptx"):
    for ppt in SOURCE.rglob(ext):
        target = DEST / ppt.name
        if target.exists():          # équiv. du `cp -n` → on saute les doublons
            print(f"↪︎ déjà présent, on ignore : {ppt.name}")
            count_skip += 1
            continue
        shutil.copy2(ppt, target)    # copy2 garde les métadonnées
        print(f"✔︎ Copié : {ppt.relative_to(SOURCE)} → {target}")
        count_new += 1

print(f"\n✅ Terminé : {count_new} nouveau(x) fichier(s) copié(s), {count_skip} ignoré(s).")
print("   Tout est maintenant dans :", DEST)