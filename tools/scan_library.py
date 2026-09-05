#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
from core.library import scan_library
def main():
 parser=argparse.ArgumentParser(description='Read-only AudioHardcore music library scanner');parser.add_argument('path');parser.add_argument('--no-hash',action='store_true');parser.add_argument('--output',type=Path);args=parser.parse_args();payload=[r.to_dict() for r in scan_library(args.path,compute_hash=not args.no_hash)];text=json.dumps(payload,indent=2,ensure_ascii=False)
 if args.output:args.output.write_text(text,encoding='utf-8');print(f'Wrote {len(payload)} records to {args.output}')
 else:print(text)
if __name__=='__main__':main()
