import os
import shutil

# Diretório base
base_dir = "/home/fmanzoni-lx/Documents/Compal/CelebA-Spoof-Segregado-2"

# Diretórios spoof
subdirs = ["spoof_print_1", "spoof_paper_cut_2", "spoof_replay_3"]

# Caminho completo dos diretórios
test_dir = os.path.join(base_dir, "test")
train_dir = os.path.join(base_dir, "train")

# Flag para saber se houve conflito (evita exclusão do test nesse caso)
conflict_found = False

for spoof in subdirs:
    test_spoof_dir = os.path.join(test_dir, spoof)
    train_spoof_dir = os.path.join(train_dir, spoof)

    os.makedirs(train_spoof_dir, exist_ok=True)

    for filename in os.listdir(test_spoof_dir):
        src_file = os.path.join(test_spoof_dir, filename)
        dst_file = os.path.join(train_spoof_dir, filename)

        if not os.path.exists(dst_file):
            shutil.move(src_file, dst_file)
        else:
            conflict_found = True
            print(f"Aviso: Arquivo {filename} já existe em {train_spoof_dir}, não foi movido.")

# Remove o diretório test se não houve conflitos
if not conflict_found:
    shutil.rmtree(test_dir)
    print("Todos os arquivos movidos com sucesso. Diretório 'test' removido.")
else:
    print("Arquivos foram movidos, mas o diretório 'test' não foi removido devido a conflitos.")

