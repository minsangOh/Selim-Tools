import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import uuid


ROOT = Path(__file__).resolve().parents[1]
CHILD = '''
import sys
from single_instance import acquire
ok = acquire(sys.argv[1])
print(int(ok), flush=True)
if ok and len(sys.argv) > 2:
    sys.stdin.readline()
'''


@unittest.skipUnless(os.name == "nt", "Windows mutex")
class SingleInstanceTests(unittest.TestCase):
    def setUp(self):
        self.key = "test." + uuid.uuid4().hex
        self.env = {**os.environ, "PYTHONPATH": str(ROOT)}

    def start(self, key=None, cwd=None):
        proc = subprocess.Popen(
            [sys.executable, "-u", "-c", CHILD, key or self.key, "hold"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, env=self.env, cwd=cwd,
        )
        self.addCleanup(self.stop, proc)
        return proc

    @staticmethod
    def stop(proc):
        if proc.poll() is None:
            proc.kill()
        proc.communicate(timeout=10)

    def probe(self):
        result = subprocess.run(
            [sys.executable, "-c", CHILD, self.key],
            capture_output=True, text=True, env=self.env, timeout=10,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout.strip()

    def test_duplicate_and_normal_restart(self):
        first = self.start()
        self.assertEqual(first.stdout.readline().strip(), "1")
        self.assertEqual(self.probe(), "0")
        first.communicate("\n", timeout=10)
        self.assertEqual(first.returncode, 0)
        self.assertEqual(self.probe(), "1")

    def test_restart_after_forced_exit(self):
        first = self.start()
        self.assertEqual(first.stdout.readline().strip(), "1")
        first.kill()
        first.communicate(timeout=10)
        self.assertEqual(self.probe(), "1")

    def test_different_apps_can_run_together(self):
        first = self.start()
        self.assertEqual(first.stdout.readline().strip(), "1")
        other = self.start(self.key + ".other")
        self.assertEqual(other.stdout.readline().strip(), "1")

    def test_simultaneous_launch_has_one_winner(self):
        children = [self.start() for _ in range(8)]
        outcomes = [p.stdout.readline().strip() for p in children]
        self.assertEqual(outcomes.count("1"), 1, outcomes)
        self.assertEqual(outcomes.count("0"), 7, outcomes)

    def test_different_copy_and_working_directory(self):
        first = self.start()
        self.assertEqual(first.stdout.readline().strip(), "1")
        with tempfile.TemporaryDirectory() as folder:
            Path(folder, "single_instance.py").write_bytes((ROOT / "single_instance.py").read_bytes())
            second = self.start(cwd=folder)
            self.assertEqual(second.stdout.readline().strip(), "0")
            second.communicate(timeout=10)


if __name__ == "__main__":
    unittest.main()
