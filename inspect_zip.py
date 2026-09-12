#!/usr/bin/env python3
"""
Inspect ZIP archive contents and extract
"""
import zipfile
import os
import sys

def inspect_zip(zip_path):
    """List all files in the ZIP"""
    print(f"\n{'='*70}")
    print(f"INSPECTING: {zip_path}")
    print(f"{'='*70}\n")
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            file_list = zip_ref.namelist()
            print(f"Total files in ZIP: {len(file_list)}\n")
            print("Directory structure:")
            for file in sorted(file_list):
                print(f"  {file}")
        return True
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def extract_zip(zip_path, extract_to='.'):
    """Extract ZIP to directory"""
    print(f"\n{'='*70}")
    print(f"EXTRACTING: {zip_path} -> {extract_to}")
    print(f"{'='*70}\n")
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print(f"✅ Extraction complete\n")
        return True
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def find_files(directory='.', max_depth=4):
    """Recursively find all files"""
    print(f"\n{'='*70}")
    print(f"EXTRACTED STRUCTURE (max depth {max_depth}):")
    print(f"{'='*70}\n")
    
    for root, dirs, files in os.walk(directory):
        # Calculate depth
        depth = root.replace(directory, '').count(os.sep)
        if depth > max_depth:
            continue
        
        # Skip hidden and common unneeded dirs
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules']]
        
        indent = '  ' * depth
        print(f"{indent}{os.path.basename(root)}/")
        
        subindent = '  ' * (depth + 1)
        for file in sorted(files):
            if not file.startswith('.'):
                print(f"{subindent}{file}")

if __name__ == '__main__':
    zip_file = 'swi_v1_part1_source.zip'
    
    # Step 1: Inspect
    if inspect_zip(zip_file):
        # Step 2: Extract
        if extract_zip(zip_file):
            # Step 3: Show structure
            find_files()
            print("\n✅ Complete!\n")
