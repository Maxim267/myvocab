from pathlib import Path
import logging

from src.myvocab.parsing.casing.data import path_file
from src.myvocab.parsing.commands.get_file_unique_lines import get_file_unique_lines
from src.myvocab.parsing.commands.save_file import save_file
from src.myvocab.parsing.commands.save_file_merge import save_file_merge

logger = logging.getLogger(__name__)


class CasingAttrib:
    """ Casing transformation configuration

    The `Casing transformation configuration` is a structure designed to automatically generate and store
    a set of attributes used when converting words to their respective letter cases.

    Args:
        dir_unique_id (str): Unique base directory.
        is_init (bool, optional): Whether to initialize the `Casing transformation configuration`.
    """

    __mixed_casing: dict = None

    def __init__(self, dir_unique_id: str, is_init: bool = True):
        """ Initialize the `Casing transformation configuration`.
        Args:
            dir_unique_id (str): Unique base directory.
            is_init (bool, optional): Whether to initialize the `Casing transformation configuration`.
        """
        self.__dir_unique_id = dir_unique_id
        if is_init:
            self.initialize()

    # Casing
    __home = Path.home()
    __documents_path: Path = Path.joinpath(__home, "Documents")

    @property
    def casing_path(self):
        """ Get /Documents/Casing directory. """
        if self.__documents_path.exists() and self.__documents_path.is_dir():
            return Path.joinpath(self.__documents_path, self.__dir_unique_id, "Casing")
        else:
            return Path.joinpath(self.__home, self.__dir_unique_id, "Casing")

    # casing in
    @property
    def casing_in_path(self):
        """ Get /Documents/Casing/in directory. """
        return Path.joinpath(self.casing_path, "in")

    @property
    def mixed_casing_path(self):
        """ Get /Documents/Casing/in/mixed_casing.txt directory. """
        return Path.joinpath(self.casing_in_path, "mixed_casing.txt")

    @property
    def reviewed_pairs_path(self):
        """ Get /Documents/Casing/in/reviewed_pairs.txt directory. """
        return Path.joinpath(self.casing_in_path, "reviewed_pairs.txt")

    # casing out
    @property
    def casing_out_path(self):
        """ Get /Documents/Casing/out directory. """
        return Path.joinpath(self.casing_path, "out")

    @property
    def parsed_pairs_path(self):
        """ Get /Documents/Casing/out/parsed_pairs.txt directory. """
        return Path.joinpath(self.casing_out_path, "parsed_pairs.txt")

    @property
    def unreviewed_pairs_path(self):
        """ Get /Documents/Casing/out/unreviewed_pairs.txt directory. """
        return Path.joinpath(self.casing_out_path, "unreviewed_pairs.txt")

    # Initial data
    __data_path: Path = Path(path_file.__file__).parent
    __data_mixed_casing_path: Path = Path.joinpath(__data_path, "mixed_casing.txt")
    __data_reviewed_pairs_path: Path = Path.joinpath(__data_path, "reviewed_pairs.txt")

    @property
    def mixed_casing(self) -> dict:
        """ Get case variations of a word. """
        if self.__mixed_casing is None:
            self.__mixed_casing = dict()
            mixed = get_file_unique_lines(self.mixed_casing_path)
            for item in mixed:
                if cur_list := self.__mixed_casing.get(item.lower()):
                    cur_list.append(item)
                else:
                    l_list = list()
                    l_list.append(item)
                    self.__mixed_casing[item.lower()] = l_list
        return self.__mixed_casing

    def __str__(self):
        """ Return the string representation of the object. """
        cur_set = (
            f"\n  {__class__}\n"
            f"  # ALLOGRAPHICATION\n"
            f"  mixed_casing_path = {self.mixed_casing_path}\n"
            f"  reviewed_pairs_path = {self.reviewed_pairs_path}\n"
            f"  parsed_pairs_path = {self.parsed_pairs_path}\n"
            f"  unreviewed_pairs_path = {self.unreviewed_pairs_path}\n")
        return cur_set

    def str_path(self) -> str:
        """ Return the content of all used directories as a string. """
        cur_set = (
            f"# ALLOGRAPHICATION\n"
            f"{str(self.mixed_casing_path.resolve())}\n"
            f"{str(self.reviewed_pairs_path.resolve())}\n"
            f"{str(self.parsed_pairs_path.resolve())}\n"
            f"{str(self.unreviewed_pairs_path.resolve())}\n"
        )
        return cur_set

    def initialize(self):
        """ Initialize the object's attributes and set up its initial state.

        Runs only if initial data is missing from the /Document directory.
        """
        if not self.mixed_casing_path.is_file():
            cur_set = get_file_unique_lines(self.__data_mixed_casing_path)
            save_file(self.mixed_casing_path, list(cur_set), True)
        else:
            save_file_merge(self.mixed_casing_path, self.__data_mixed_casing_path, False)

        if not self.reviewed_pairs_path.is_file():
            cur_set = get_file_unique_lines(self.__data_reviewed_pairs_path)
            save_file(self.reviewed_pairs_path, list(cur_set), True)
        else:
            save_file_merge(self.reviewed_pairs_path, self.__data_reviewed_pairs_path, False)
