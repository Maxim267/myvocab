from pathlib import Path

def save_file(file_path: Path, items: list, is_sorted: bool) -> None:
    """ Write a list to a file.

        Args:
            file_path (Path): Path to the file
            items (list): Items to save
            is_sorted (bool): Sorting option
    """

    if not file_path.parent.exists():
        file_path.parent.mkdir(exist_ok = True, parents = True)

    with open(file_path, "w", encoding='utf-8') as file:
        if is_sorted:
            file.writelines(f"{word}\n" for word in sorted(items))
        else:
            file.writelines(f"{word}\n" for word in items)