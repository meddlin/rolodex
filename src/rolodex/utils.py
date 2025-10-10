import os
import tempfile
import subprocess

def launch_editor_with_text(initial_text: str) -> str:
    _EDITOR_ = os.environ.get("EDITOR", "vim")

    with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as tf:
        tf.write(initial_text.encode("utf-8"))
        tf.flush()
        temp_name = tf.name

    subprocess.call([_EDITOR_, temp_name])

    with open(temp_name, "r") as tf:
        updated_text = tf.read()

    os.unlink(temp_name)  # cleanup temp file
    return updated_text