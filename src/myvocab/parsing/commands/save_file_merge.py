from pathlib import Path
from src.myvocab.parsing.commands.get_file_unique_lines import get_file_unique_lines
from src.myvocab.parsing.commands.get_list_diff import get_list_diff
from src.myvocab.parsing.commands.save_file import save_file

def save_file_merge(path1: Path, path2: Path):
    """ Merge files, remove duplicates, and sort each file's lines separately. """

    cur_list1 = list(get_file_unique_lines(path1))
    cur_list2 = list(get_file_unique_lines(path2))
    cur_list1 = get_list_diff(cur_list1, cur_list2)
    cur_list1.sort()
    cur_list2.sort()
    cur_list1.extend(cur_list2)
    save_file(path1, cur_list1, False)