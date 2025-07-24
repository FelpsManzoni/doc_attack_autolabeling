import pandas as pd
import os
 
def split_csv_into_four(input_csv, output_dir='splits'):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
 
    # Load the CSV
    df = pd.read_csv(input_csv)
 
    # Calculate the size of each split
    total_rows = len(df)
    split_size = total_rows // 4
 
    # Split and save
    for i in range(4):
        start_idx = i * split_size
        end_idx = (i + 1) * split_size if i < 3 else total_rows  # last chunk gets the remainder
        split_df = df.iloc[start_idx:end_idx]
        split_df.to_csv(os.path.join(output_dir, f'split_{i + 1}.csv'), index=False)
 
    print(f"CSV file split into 4 parts in folder: {output_dir}")
 
# Example usage
split_csv_into_four('C:/Projects/COMPAL/train_labels.csv')