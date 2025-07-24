import os
import cv2

def process_label_file(label_file, mode):
    with open(label_file, 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        img_rel_path, label = line.strip().split()
        label = int(label)  # 0 = live, 1 = spoof

        img_path = os.path.join(root_dir, img_rel_path)
        bb_path = os.path.splitext(img_path)[0] + '_BB.txt'

        if not os.path.isfile(img_path):
            print(f"[ERRO] Imagem não encontrada: {img_path}")
            continue

        if not os.path.isfile(bb_path):
            print(f"[ERRO] Bounding box não encontrada para: {img_path}")
            continue

        # Carrega imagem
        img = cv2.imread(img_path)
        if img is None:
            print(f"[ERRO] Falha ao carregar imagem: {img_path}")
            continue

        real_h, real_w = img.shape[:2]

        # Agora é seguro abrir o arquivo .txt de bbox
        try:
            with open(bb_path, 'r') as bb_file:
                bbox_line = bb_file.readline().strip()
                if not bbox_line:
                    print(f"[ERRO] Bounding box vazia: {bb_path}")
                    continue
                bbox = list(map(float, bbox_line.split()))
        except Exception as e:
            print(f"[ERRO] Problema lendo bbox {bb_path}: {e}")
            continue
        
        if len(bbox) < 4:
            print(f"[ERRO] Bounding box inválida em {bb_path}")
            continue

        # Ajustar a bbox para o tamanho real da imagem
        x1 = int(bbox[0] * (real_w / 224))
        y1 = int(bbox[1] * (real_h / 224))
        w1 = int(bbox[2] * (real_w / 224))
        h1 = int(bbox[3] * (real_h / 224))

        # Corrigir limites
        x1 = max(0, x1)
        y1 = max(0, y1)
        w1 = min(w1, real_w - x1)
        h1 = min(h1, real_h - y1)

        # Crop
        cropped_img = img[y1:y1+h1, x1:x1+w1]

        # Diretório de saída
        out_dir = os.path.join(output_root, mode, 'live' if label == 0 else 'spoof')
        os.makedirs(out_dir, exist_ok=True)

        # Nome do arquivo de saída
        filename = os.path.basename(img_path)
        out_path = os.path.join(out_dir, filename)

        # Salvar imagem cropada
        cv2.imwrite(out_path, cropped_img)
        print(f"[OK] Imagem salva: {out_path}")

# Definir caminhos
root_dir = 'C:/Projects/COMPAL/CelebA'
output_root = 'C:/Projects/COMPAL/CelebA/CelebA_spoof_croped'

# Processar treino e teste
process_label_file('C:/Projects/COMPAL/CelebA/metas/intra_test/train_label.txt', 'train')
process_label_file('C:/Projects/COMPAL/CelebA/metas/intra_test/test_label.txt', 'test')

