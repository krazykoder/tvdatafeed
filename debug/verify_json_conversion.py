#!/usr/bin/env python3
"""
Verify converted JSON files and extract key financial data
"""
import json
import sys
import os
from pathlib import Path

def verify_json_file(json_file):
    """Verify and analyze a converted JSON file"""
    
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        print(f"[*] {os.path.basename(json_file)}")
        
        # Check structure
        if 'metadata' not in data or 'frames' not in data:
            print("    ✗ Invalid structure (missing metadata or frames)")
            return False
        
        metadata = data['metadata']
        frames = data['frames']
        
        print(f"    ✓ Valid JSON structure")
        print(f"    ✓ Source: {metadata.get('source_file')}")
        print(f"    ✓ Total frames: {metadata.get('total_objects')}")
        print(f"    ✓ Frames extracted: {len(frames)}")
        
        # Analyze frame contents
        session_id = None
        financial_data_count = 0
        
        for i, frame in enumerate(frames):
            if isinstance(frame, dict):
                # Check for session ID
                if 'session_id' in frame and session_id is None:
                    session_id = frame['session_id']
                
                # Check for financial data
                if 'p' in frame and isinstance(frame['p'], list) and len(frame['p']) > 1:
                    if isinstance(frame['p'][1], dict) and 'v' in frame['p'][1]:
                        v = frame['p'][1]['v']
                        if isinstance(v, dict):
                            # Check for financial fields
                            if any(k in v for k in ['revenues_fq_h', 'earnings_fq_h', 'revenues_fy_h', 'earnings_fy_h']):
                                financial_data_count += 1
        
        if session_id:
            print(f"    ✓ Session ID: {session_id}")
        
        if financial_data_count > 0:
            print(f"    ✓ Financial data frames: {financial_data_count}")
        
        print(f"    ✓ File size: {os.path.getsize(json_file):,} bytes")
        
        return True
    
    except json.JSONDecodeError as e:
        print(f"    ✗ Invalid JSON: {e}")
        return False
    except Exception as e:
        print(f"    ✗ Error: {e}")
        return False

def verify_all_json_files(directory=None, pattern='*.json'):
    """Verify all JSON files in a directory"""
    
    if directory is None:
        directory = os.path.dirname(__file__)
    
    # Find all .json files
    json_files = sorted(Path(directory).glob(pattern))
    
    if not json_files:
        print(f"No {pattern} files found in {directory}")
        return 0
    
    print(f"\n{'='*80}")
    print(f"Verifying Converted JSON Files")
    print(f"{'='*80}\n")
    
    valid = 0
    invalid = 0
    
    for json_file in json_files:
        # Skip non-converted files (those without _NASDAQ in name)
        if '_NASDAQ' not in str(json_file):
            continue
        
        if verify_json_file(str(json_file)):
            valid += 1
        else:
            invalid += 1
        print()
    
    print(f"{'='*80}")
    print(f"Results: {valid} valid, {invalid} invalid")
    print(f"{'='*80}\n")
    
    return valid

if __name__ == '__main__':
    # Get directory from command line or use current directory
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        directory = os.path.dirname(__file__)
    
    valid = verify_all_json_files(directory)
    sys.exit(0 if valid > 0 else 1)
