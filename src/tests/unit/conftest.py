# conftest.py
import os
import pytest

OUTPUT_DIR = "src/output"

@pytest.fixture(autouse=True)
def cleanup_output_files():
    yield  # let the test run
    for filename in os.listdir(OUTPUT_DIR):
        if not filename.endswith(".txt"):
            filepath = os.path.join(OUTPUT_DIR, filename)
            if os.path.isfile(filepath):
                os.remove(filepath)
