import os
import random
import shutil

def downsample_dataset(
    input_root, output_root, fraction=0.2, max_per_class=None, seed=42
):
    random.seed(seed)

    # Walk through train and test directories
    for split in ['train', 'test']:
        input_split = os.path.join(input_root, split)
        output_split = os.path.join(output_root, split)
        os.makedirs(output_split, exist_ok=True)

        for class_name in os.listdir(input_split):
            class_input_path = os.path.join(input_split, class_name)
            class_output_path = os.path.join(output_split, class_name)
            os.makedirs(class_output_path, exist_ok=True)

            if not os.path.isdir(class_input_path):
                continue

            all_files = [
                f for f in os.listdir(class_input_path)
                if os.path.isfile(os.path.join(class_input_path, f))
            ]
            total = len(all_files)

            if max_per_class:
                num_to_keep = min(max_per_class, total)
            else:
                num_to_keep = int(total * fraction)

            selected_files = random.sample(all_files, num_to_keep)

            for filename in selected_files:
                src = os.path.join(class_input_path, filename)
                dst = os.path.join(class_output_path, filename)
                shutil.copy2(src, dst)

            print(f"{split}/{class_name}: kept {num_to_keep}/{total} images")

# Example usage
downsample_dataset(
    input_root='/home/fmanzoni-lx/Documents/Compal/CelebA-Spoof-Segregado-2',
    output_root='/home/fmanzoni-lx/Documents/Compal/CelebA-Spoof-Segregado-downsample',
    fraction=0.2  # Keep 20% of each class
    # or use: max_per_class=500 to limit by count
)