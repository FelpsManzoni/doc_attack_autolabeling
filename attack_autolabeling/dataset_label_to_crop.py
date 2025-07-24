import os
import pandas as pd
import shutil
from tqdm import tqdm
import glob
from pathlib import Path

# === CONFIGURAÇÃO ===
csv_path = Path("C:/Projects/COMPAL/train_labels.csv")  # ou "test_labels.csv"
crop_root = Path("C:/Projects/COMPAL/CelebA/CelebA_spoof_croped")
output_root = "croped_filtered"

# === PROCESSAMENTO ===
df = pd.read_csv(csv_path)

for _, row in tqdm(df.iterrows(), total=len(df), desc="Copiando imagens"):
    image_path = row['image_path']       # ex: train/spoof_medium_0/494410.png
    label = row['label']                 # ex: spoof_medium_0 ou live
    img_name = os.path.basename(image_path)
    part = image_path.split("\\")[0]      # train ou test

    # Buscar imagem em crop_root/[train|test]/**/[img_name]
    search_pattern = os.path.join(crop_root, part, "**", img_name)
    matches = glob.glob(search_pattern, recursive=True)

    if not matches:
        print(f"[!] Imagem não encontrada: {search_pattern}")
        continue

    src = matches[0]
    dst_dir = os.path.join(output_root, part, label)
    dst = os.path.join(dst_dir, img_name)

    os.makedirs(dst_dir, exist_ok=True)
    shutil.copy2(src, dst)

