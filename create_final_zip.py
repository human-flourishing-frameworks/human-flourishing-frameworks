#!/usr/bin/env python3
"""
Create comprehensive zip file with all framework materials
"""

import zipfile
import os
from pathlib import Path

def create_zip():
    """Create final deliverable zip file"""

    base_dir = Path("/tmp/quantum-compliance-poc")
    zip_path = Path("/tmp/quantum-compliance-framework-complete.zip")

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Walk through all files in the directory
        for root, dirs, files in os.walk(base_dir):
            # Skip __pycache__ and other non-essential directories
            dirs[:] = [d for d in dirs if d not in ['__pycache__', '.pytest_cache', '.git']]

            for file in files:
                # Skip .pyc files
                if file.endswith('.pyc'):
                    continue

                file_path = Path(root) / file
                arcname = file_path.relative_to("/tmp")

                zf.write(file_path, arcname)
                print(f"Added: {arcname}")

    size_mb = zip_path.stat().st_size / (1024 * 1024)
    print(f"\n✓ Created: {zip_path}")
    print(f"  Size: {size_mb:.2f} MB")

    # List contents
    print(f"\n  Contents:")
    with zipfile.ZipFile(zip_path, 'r') as zf:
        for info in zf.filelist:
            if not info.is_dir():
                print(f"    - {info.filename} ({info.file_size} bytes)")


if __name__ == "__main__":
    create_zip()
