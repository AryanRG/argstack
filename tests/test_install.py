import hashlib
import os
from unittest.mock import patch
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

    def test_external_cache_via_symlinked_path(self):
        sys.path.insert(0, str(ROOT))
        import install
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            real = root/'real'
            real.mkdir()
            alias = root/'alias'
            alias.symlink_to(real, target_is_directory=True)
            source = root/'source.md'
            source.write_text('local test fixture')
            entry = {'source':source.resolve().as_uri(), 'sha256':hashlib.sha256(source.read_bytes()).hexdigest()}
            with patch.dict(os.environ, XDG_CACHE_HOME=str(alias)), patch.dict(install.EXTERNAL, example=entry):
                dest = install.resolve_external('example')
                self.assertEqual(dest, dest.resolve())
                self.assertEqual((dest/'SKILL.md').read_bytes(),source.read_bytes())
