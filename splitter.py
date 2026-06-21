# splitter.py
import json
import os

from cursor import load_cursor, save_cursor, reset_cursor
from scanned_ips import load_scanned_ips, add_scanned_ips, is_scanned, scanned_count

INPUT_FILE = "output/clean_ips.txt"
OUTPUT_FILE = "output/current_part.txt"

def load_config():
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def write_lines(path, lines):
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

def count_lines(path):
    total = 0
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    total += 1
    except:
        return 0
    return total

def read_chunk(path, start, size):
    chunk = []
    idx = 0
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if idx < start:
                    idx += 1
                    continue
                chunk.append(line)
                if len(chunk) >= size:
                    break
                idx += 1
    except:
        return []
    return chunk

def split_file(infile=INPUT_FILE):
    cfg = load_config()
    batch_size = cfg.get("batch_size", 20000)
    total = count_lines(infile)
    
    if total <= 0:
        write_lines(OUTPUT_FILE, [])
        reset_cursor()
        print("NO CLEAN IPS")
        return OUTPUT_FILE
    
    scanned = load_scanned_ips()
    total_scanned = len(scanned)
    print(f"TOTAL CLEAN IPS={total}, SCANNED={total_scanned}")
    
    if total_scanned >= total:
        print("ALL IPS SCANNED - RESETTING SCANNED LIST")
        save_scanned_ips(set())
        scanned = set()
        reset_cursor()
    
    cursor = load_cursor()
    
    if cursor < 0:
        cursor = 0
    
    if cursor >= total:
        cursor = 0
        save_cursor(0)
    
    chunk = []
    found_new = 0
    idx = 0
    
    try:
        with open(infile, "r", encoding="utf-8") as f:
            for line in f:
                ip = line.strip()
                if not ip:
                    continue
                
                if ip in scanned:
                    idx += 1
                    continue
                
                if idx < cursor:
                    idx += 1
                    continue
                
                chunk.append(ip)
                found_new += 1
                
                if len(chunk) >= batch_size:
                    break
                
                idx += 1
    except:
        pass
    
    if not chunk:
        print("NO NEW IPS FOUND - SCANNING FROM BEGINNING")
        cursor = 0
        save_cursor(0)
        try:
            with open(infile, "r", encoding="utf-8") as f:
                for line in f:
                    ip = line.strip()
                    if not ip:
                        continue
                    chunk.append(ip)
                    if len(chunk) >= batch_size:
                        break
        except:
            pass
    
    next_cursor = cursor + len(chunk)
    
    if next_cursor >= total:
        next_cursor = total
        save_cursor(next_cursor)
        print("REACHED END OF LIST - WILL CONTINUE FROM BEGINNING NEXT CYCLE")
    else:
        save_cursor(next_cursor)
    
    write_lines(OUTPUT_FILE, chunk)
    
    percent = round((next_cursor / total) * 100, 2) if total > 0 else 0
    print(f"TOTAL={total} CURSOR={cursor} END={next_cursor} PART={len(chunk)} NEW_IPS={found_new} PROGRESS={percent}%")
    
    return OUTPUT_FILE

if __name__ == "__main__":
    split_file()
