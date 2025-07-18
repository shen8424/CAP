import json
import os
import re
import time
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

_pattern = re.compile(r'[^a-zA-Z0-9]')

def process_candidates(candidates):
    """Optimized candidate key processing"""
    keys = list(candidates.keys())
    sorted_keys = sorted(keys, key=lambda x: -len(x))
    reserved = []

    reserved_set = set()
    for key in sorted_keys:
        if not any(key in rk for rk in reserved_set):
            reserved.append(key)
            reserved_set.add(key)
    return reserved

def normalize(s):
    """Normalize string: remove all non-alphanumeric characters and convert to lowercase"""
    return _pattern.sub('', s).lower()

def get_subfolders_dict(parent_path):
    """Efficiently get subfolder information"""
    subfolders = []
    for entry in os.listdir(parent_path):
        entry_path = os.path.join(parent_path, entry)
        if os.path.isdir(entry_path):
            subfolders.append((entry, entry_path))
    return {name: path for name, path in subfolders}

def process_item(item, json_b, normalized_subfolders):
    """Parallel processing of a single JSON A entry"""
    text = item.get('text', '')
    
    candidates_b = {}
    for key, value in json_b.items():
        if len(key) <= 3:
            continue
        if key in text:
            candidates_b[key] = value
    
    reserved_b = process_candidates(candidates_b)
    
    extra_info = {k: f"{k} {candidates_b[k]}" for k in reserved_b}
    item['cap_texts'] = extra_info
    
    extra_imgs = {}
    for key in extra_info:
        normalized_key = normalize(key)
        if normalized_key in normalized_subfolders:
            path = normalized_subfolders[normalized_key][1]
            extra_imgs[key] = path
    item['cap_images'] = extra_imgs
    
    return item

def main(args):
    print("Starting the program...")
    start_time = time.time()
    
    print("Loading JSON A from", args.path_A)
    with open(args.path_A, 'r', encoding='utf-8') as f:
        json_a = json.load(f)
    
    print("Loading JSON B from", args.path_B)
    with open(args.path_B, 'r', encoding='utf-8') as f:
        json_b = json.load(f)
    
    print("Processing subfolders in", args.folder_path)
    subfolder_dict = get_subfolders_dict(args.folder_path)
    normalized_subfolders = {
        normalize(name): (name, path) 
        for name, path in subfolder_dict.items()
    }
    
    print("Processing items in parallel...")
    processed_items = []
    futures = []
    with ThreadPoolExecutor() as executor:
        for item in json_a:
            future = executor.submit(process_item, item, json_b, normalized_subfolders)
            futures.append(future)
        
        with tqdm(total=len(futures), desc="Processing items") as pbar:
            for future in as_completed(futures):
                result = future.result()
                processed_items.append(result)
                pbar.update(1)
    
    print(f"Saving results to {args.output_path}")
    with open(args.output_path, 'w', encoding='utf-8') as f:
        json.dump(processed_items, f, indent=4, ensure_ascii=False)
    
    end_time = time.time()
    print(f"Program completed in {end_time - start_time:.2f} seconds.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process JSON data with folder mapping')
    parser.add_argument('--path_A', type=str, default = "./train.json",
                        help='Path to Your Json')
    parser.add_argument('--path_B', type=str, default = "./cap_text_info.json",
                        help='Path to JSON CAP Texts')
    parser.add_argument('--folder_path', type=str, default = "./people_imgs",
                        help='Path to the folder containing CAP Images')
    parser.add_argument('--output_path', type=str, default = "./train_cap.json",
                        help='Path to save the output JSON file')
    
    args = parser.parse_args()
    main(args)
