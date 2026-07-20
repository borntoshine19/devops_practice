import os
import shutil
from datetime import datetime

source_dir = "/home/sasha/dev"
backup_dir = "/home/sasha/dev/backups"

if not os.path.exists(backup_dir):
	os.makedirs(backup_dir)

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
backup_path = os.path.join(backup_dir, f"backup_{timestamp}")

shutil.copytree(source_dir, backup_path, ignore=shutil.ignore_patterns('venv', 'backups', '.git'))

import time
days_to_keep = 7
now = time.time()

for f in os.listdir(backup_dir):
	f_path = os.path.join(backup_dir, f)

	if os.stat(f_path).st_mtime < now - (days_to_keep * 86400):
		if os.path.isdir(f_path):
			shutil.rmtree(f_path)

print(f"Succesful backup in {backup_path}")
