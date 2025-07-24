import os
import shutil

def move_folder_contents(src_folder, dst_folder):
    # Make sure destination exists
    os.makedirs(dst_folder, exist_ok=True)

    # Loop through all items in the source folder
    for item in os.listdir(src_folder):
        src_path = os.path.join(src_folder, item)
        dst_path = os.path.join(dst_folder, item)

        # Move the item
        shutil.move(src_path, dst_path)
        print(f"Moved: {src_path} → {dst_path}")

# Example usage
move_folder_contents('/home/fmanzoni-lx/Documents/Compal/CelebA-Spoof-Segregado-2/train/spoof_medium_8', '/home/fmanzoni-lx/Documents/Compal/CelebA-Spoof-Segregado-2/train/spoof_medium_9')