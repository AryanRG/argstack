import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]

class InstallTest(unittest.TestCase):
    def test_repeat_install_and_collision(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp)/'agent'/'skills'
            cmd = [sys.executable, str(ROOT/'install.py'), '--target', str(target)]
            subprocess.run(cmd + ['overnight'], check=True, capture_output=True)
            subprocess.run(cmd + ['overnight'], check=True, capture_output=True)
            self.assertTrue((target/'overnight'/'SKILL.md').samefile(ROOT/'skills/overnight/SKILL.md'))
            (target/'modernize').mkdir()
            (target/'modernize/local.txt').write_text('user-owned')
            result = subprocess.run(cmd + ['bro','modernize'], capture_output=True)
            self.assertNotEqual(result.returncode,0)
            self.assertFalse(os.path.lexists(target/'bro'))
            self.assertEqual((target/'modernize/local.txt').read_text(),'user-owned')
