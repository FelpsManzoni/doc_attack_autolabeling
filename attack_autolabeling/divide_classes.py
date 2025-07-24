import os
import json
import shutil
import pandas as pd
from collections import defaultdict
from tqdm import tqdm

# === CONFIGURAÇÕES ===
original_base_dir = "C:/Projects/COMPAL/CelebA/Data"  # <-- AJUSTE AQUI
output_dir = "CelebA-Spoof-Segregado"
train_json = "C:/Projects/COMPAL/CelebA/metas/protocol1/train_label.json"
test_json = "C:/Projects/COMPAL/CelebA/metas/protocol1/test_label.json"

# Para armazenar estatísticas
stats = []

def process_partition(json_path, partition_name):
    with open(json_path, "r") as f:
        data = json.load(f)

    spoof_count = defaultdict(int)
    live_count = 0

    for path, meta in tqdm(data.items(), desc=f"Processando {partition_name}"):
        src_path = os.path.join(original_base_dir, os.path.relpath(path, "Data"))
        if meta[43] == 1 and 'spoof' in path:
            spoof_medium = meta[40]
            dst_dir = os.path.join(output_dir, partition_name, f"spoof_medium_{spoof_medium}")
            spoof_count[spoof_medium] += 1
        elif meta[43] == 0 and 'live' in path:
            dst_dir = os.path.join(output_dir, partition_name, "live")
            live_count += 1
        else:
            continue

        os.makedirs(dst_dir, exist_ok=True)
        dst_path = os.path.join(dst_dir, os.path.basename(path))
        try:
            shutil.copy2(src_path, dst_path)
        except FileNotFoundError:
            print(f"[!] Arquivo não encontrado: {src_path}")

    # Exibir contagens
    print(f"\n📊 Distribuição em {partition_name}:")
    print(f"  Live: {live_count}")
    for k in sorted(spoof_count):
        print(f"  Spoof tipo {k}: {spoof_count[k]}")

    # Salvar no stats
    stats.append({
        'partition': partition_name,
        'live': live_count,
        **{f'spoof_{k}': spoof_count[k] for k in sorted(spoof_count)}
    })

# Executar nos dois conjuntos
process_partition(train_json, "train")
process_partition(test_json, "test")

# Salvar estatísticas como CSV
df_stats = pd.DataFrame(stats)
df_stats.to_csv(os.path.join(output_dir, "stats.csv"), index=False)

print("\n✅ Organização e contagem concluídas. Estatísticas salvas em stats.csv.")

