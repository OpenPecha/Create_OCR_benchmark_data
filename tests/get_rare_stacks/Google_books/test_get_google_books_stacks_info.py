from pathlib import Path 

from create_benchmark_data.get_rare_stacks import get_google_books_stacks_info

def test_crop_image():
    DATA_DIR = Path(__file__).parent / "data"
    
    output_file = DATA_DIR / "stack_info.json"
    get_google_books_stacks_info(DATA_DIR, output_file)
    assert output_file.exists() == True

    expected_stacks_info = DATA_DIR / "expected_stack_info.json"
    assert output_file.read_text() == expected_stacks_info.read_text()

    output_file.unlink()
    
