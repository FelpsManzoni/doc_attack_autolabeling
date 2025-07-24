import os
import pandas as pd

base_dir = "C:/Projects/COMPAL/CelebA-Spoof-Segregado/"
partitions = ["train", "test"]

entries = []

for part in partitions:
    part_dir = os.path.join(base_dir, part)
    for label_dir in os.listdir(part_dir):
        label_path = os.path.join(part_dir, label_dir)
        if not os.path.isdir(label_path):
            print(label_path)
            continue
        for img_name in os.listdir(label_path):
            if img_name.lower().endswith(('.jpg', '.png', '.jpeg')):
                relative_path = os.path.join(part, label_dir, img_name)
                entries.append({
                    "image_path": relative_path,
                    "label": label_dir
                })

# Criar DataFrame e separar por partição
df = pd.DataFrame(entries)
df_train = df[df["image_path"].str.startswith("train")]
df_test = df[df["image_path"].str.startswith("test")]

# Salvar CSVs
df_train.to_csv("train_labels.csv", index=False)
df_test.to_csv("test_labels.csv", index=False)

print("✅ CSVs gerados: train_labels.csv e test_labels.csv")

