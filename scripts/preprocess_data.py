import pandas as pd
import numpy as np
import os

def clean_tello_data(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    print(f"Loading {input_file}...")
    df = pd.read_csv(input_file)

    # 1. Remove initialization NaNs (where Gazebo wasn't active yet)
    initial_rows = len(df)
    df_clean = df.dropna(subset=['gz_x', 'gz_y', 'gz_z']).copy()
    
    # 2. Reset time to start from 0.0s
    df_clean['time'] = df_clean['time'] - df_clean['time'].iloc[0]
    
    # 3. Center coordinates so flight starts at (0,0,0)
    # This helps the Neural ODE learn physics instead of absolute offsets
    for col in ['gz_x', 'gz_y', 'gz_z', 'twin_x', 'twin_y', 'twin_z']:
        df_clean[col] = df_clean[col] - df_clean[col].iloc[0]

    # 4. Save the result
    df_clean.to_csv(output_file, index=False)
    
    print(f"DONE!")
    print(f"Original rows: {initial_rows}")
    print(f"Cleaned rows:  {len(df_clean)}")
    print(f"Saved to: {output_file}")

if __name__ == "__main__":
    # Ensure the data directory exists
    if not os.path.exists('data'):
        os.makedirs('data')
        
    clean_tello_data('twin_compare_15_secned_.csv', 'data/cleaned_tello_data.csv')
