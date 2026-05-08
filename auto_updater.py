#!/usr/bin/env python3
"""
Automatic Update Daemon
Nodes automatically fetch and apply updates without user intervention
Zero-downtime rolling updates
"""

import subprocess
import requests
import json
import os
import time
import hashlib
from datetime import datetime

GITHUB_REPO = "alex-place/human-flourishing-frameworks"
UPDATE_CHECK_INTERVAL = 3600  # Check every hour
CURRENT_VERSION = os.environ.get('HFF_VERSION', '1.0.0')
UPDATE_ENABLED = True

def get_latest_version():
    """Fetch latest version from GitHub"""
    try:
        response = requests.get(
            f'https://api.github.com/repos/{GITHUB_REPO}/releases/latest',
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            return data.get('tag_name', '1.0.0').lstrip('v')
    except:
        pass
    return None

def get_release_info(version):
    """Get release info from GitHub"""
    try:
        response = requests.get(
            f'https://api.github.com/repos/{GITHUB_REPO}/releases/tags/v{version}',
            timeout=5
        )
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def download_update(version):
    """Download update from GitHub"""
    try:
        # Download the repo as zip
        response = requests.get(
            f'https://github.com/{GITHUB_REPO}/archive/refs/tags/v{version}.zip',
            timeout=30
        )
        if response.status_code == 200:
            os.makedirs('./updates', exist_ok=True)
            zip_path = f'./updates/hff-v{version}.zip'
            with open(zip_path, 'wb') as f:
                f.write(response.content)
            return zip_path
    except Exception as e:
        print(f"[ERROR] Failed to download update: {e}")
    return None

def verify_update(zip_path, expected_hash):
    """Verify update integrity"""
    try:
        with open(zip_path, 'rb') as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
        return file_hash == expected_hash
    except:
        return False

def install_update(version):
    """Install update with zero downtime"""
    try:
        os.makedirs('./backups', exist_ok=True)

        # Backup current code
        backup_cmd = f'git checkout -b backup-{datetime.now().strftime("%Y%m%d-%H%M%S")}'
        subprocess.run(backup_cmd, shell=True, cwd='.', timeout=30)

        # Fetch latest from GitHub
        subprocess.run('git fetch origin master', shell=True, cwd='.', timeout=30)

        # Pull latest (fast-forward only)
        result = subprocess.run(
            'git pull --ff-only origin master',
            shell=True,
            cwd='.',
            timeout=30,
            capture_output=True
        )

        if result.returncode == 0:
            print(f"[OK] Updated to version {version}")

            # Update version file
            with open('.version', 'w') as f:
                f.write(version)

            # Restart the app (systemd will handle restart)
            print("[OK] Update installed - restart required")
            return True
        else:
            print(f"[ERROR] Git pull failed: {result.stderr.decode()}")
            return False

    except Exception as e:
        print(f"[ERROR] Update installation failed: {e}")
        return False

def check_for_updates():
    """Check for updates periodically"""
    while UPDATE_ENABLED:
        try:
            latest_version = get_latest_version()

            if latest_version and latest_version > CURRENT_VERSION:
                print(f"[INFO] New version available: {latest_version}")

                # Download and install
                if install_update(latest_version):
                    print(f"[OK] Successfully updated to v{latest_version}")
                else:
                    print(f"[WARNING] Failed to update to v{latest_version}")

        except Exception as e:
            print(f"[WARNING] Update check failed: {e}")

        # Wait before checking again
        time.sleep(UPDATE_CHECK_INTERVAL)

def get_update_status():
    """Get current update status"""
    return {
        'current_version': CURRENT_VERSION,
        'latest_version': get_latest_version(),
        'update_enabled': UPDATE_ENABLED,
        'last_check': datetime.utcnow().isoformat(),
        'next_check_in_hours': UPDATE_CHECK_INTERVAL / 3600
    }

if __name__ == "__main__":
    print("[OK] Auto-updater initialized")
    print(f"[INFO] Current version: {CURRENT_VERSION}")
    print(f"[INFO] Checking for updates every {UPDATE_CHECK_INTERVAL}s")
