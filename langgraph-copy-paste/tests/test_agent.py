import tempfile
import unittest
from pathlib import Path


class CopyFileTests(unittest.TestCase):
    def test_copy_requested_file_into_target_directory(self):
        from agent.copy_logic import copy_requested_file

        with tempfile.TemporaryDirectory() as temp_dir:
            base_dir = Path(temp_dir)
            source_dir = base_dir / "source_docs"
            target_dir = base_dir / "target_docs"
            source_dir.mkdir()
            target_dir.mkdir()

            source_file = source_dir / "test.txt"
            source_file.write_text("hello copy agent", encoding="utf-8")

            result = copy_requested_file("copy test.txt", source_dir, target_dir)

            self.assertEqual(
                result,
                "Success: 'test.txt' copied from source_docs to target_docs.",
            )
            self.assertEqual(
                (target_dir / "test.txt").read_text(encoding="utf-8"),
                "hello copy agent",
            )


if __name__ == "__main__":
    unittest.main()
