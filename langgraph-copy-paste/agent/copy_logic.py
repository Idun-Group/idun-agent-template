import re
import shutil
from pathlib import Path


def copy_requested_file(user_text: str, source_dir: Path, target_dir: Path) -> str:
    match = re.search(r"copy\s+(.+)$", user_text.strip(), re.IGNORECASE)
    if not match:
        return "Invalid command. Use: copy <filename>"

    filename = match.group(1).strip()
    if not filename or ".." in filename or Path(filename).is_absolute():
        return "Invalid filename."

    source_dir = source_dir.resolve()
    target_dir = target_dir.resolve()
    source_path = (source_dir / filename).resolve()
    target_path = (target_dir / filename).resolve()

    try:
        source_path.relative_to(source_dir)
        target_path.relative_to(target_dir)
    except ValueError:
        return "Access denied: path out of scope."

    if not source_path.exists():
        return f"Source file not found: {filename}"

    target_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_path, target_path)
    return f"Success: '{filename}' copied from source_docs to target_docs."
