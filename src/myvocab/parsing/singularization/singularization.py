from pathlib import Path
from src.myvocab.parsing.singularization.data import path_file
from src.myvocab.parsing.commands.get_file_unique_lines import get_file_unique_lines
from src.myvocab.parsing.commands.save_file import save_file
from src.myvocab.parsing.commands.get_v_tuple import get_v2

class SingularAttrib:
    """ Singular transformation configuration.

    The `Singular transformation configuration` is a structure designed to automatically generate and store
    a set of attributes used for converting words from plural to singular form.
    """

    __singular_ending_non_s: set = None
    __only_ending_s: set = None
    __irregular_plural_nouns: dict = None
    __reviewed_pairs: dict = None

    def __init__(self, dir_unique_id: str):
        """ Initialize the `Singular transformation configuration`.
        Args:
            dir_unique_id (str): Unique base directory.
        """
        self.__dir_unique_id = dir_unique_id
        self.initialize()

    # Singularization 
    __home = Path.home()
    __documents_path: Path = Path.joinpath(__home, "Documents")
    @property
    def singularization_path(self):
        """ Get /Documents/Singularization directory. """
        if self.__documents_path.exists() and self.__documents_path.is_dir():
            return Path.joinpath(self.__documents_path, self.__dir_unique_id, "Singularization")
        else:
            return Path.joinpath(self.__home, self.__dir_unique_id, "Singularization")

    # Singularization in
    @property
    def singularization_in_path(self):
        """ Get /Documents/Singularization/in directory. """
        return Path.joinpath(self.singularization_path, "in")

    @property
    def only_ending_s_path(self):
        """ Get /Documents/Singularization/in/only_ending_s.txt directory. """
        return Path.joinpath(self.singularization_in_path, "only_ending_s.txt")

    @property
    def singular_ending_non_s_path(self):
        """ Get /Documents/Singularization/in/singular_ending_non_s.txt directory. """
        return Path.joinpath(self.singularization_in_path, "singular_ending_non_s.txt")

    @property
    def irregular_plural_nouns_path(self):
        """ Get /Documents/Singularization/in/irregular_plural_nouns.txt directory. """
        return Path.joinpath(self.singularization_in_path, "irregular_plural_nouns.txt")

    @property
    def reviewed_pairs_path(self):
        """ Get /Documents/Singularization/in/reviewed_pairs.txt directory. """
        return Path.joinpath(self.singularization_in_path, "reviewed_pairs.txt")

    # Singularization out
    @property
    def singularization_out_path(self):
        """ Get /Documents/Singularization/out directory. """
        return Path.joinpath(self.singularization_path, "out")

    @property
    def parsed_pairs_path(self):
        """ Get /Documents/Singularization/out/parsed_pairs.txt directory. """
        return Path.joinpath(self.singularization_out_path, "parsed_pairs.txt")

    @property
    def unreviewed_pairs_path(self):
        """ Get /Documents/Singularization/out/unreviewed_pairs.txt directory. """
        return Path.joinpath(self.singularization_out_path, "unreviewed_pairs.txt")

    # Initial data
    __data_path: Path = Path(path_file.__file__).parent
    __data_only_ending_s_path: Path = Path.joinpath(__data_path, "only_ending_s.txt")
    __data_singular_ending_non_s_path: Path = Path.joinpath(__data_path, "singular_ending_non_s.txt")
    __data_irregular_plural_nouns_path: Path = Path.joinpath(__data_path, "irregular_plural_nouns.txt")
    __data_reviewed_pairs_path: Path = Path.joinpath(__data_path, "reviewed_pairs.txt")

    # Singularization lists in
    @property
    def only_ending_s(self) -> set:
        """ Get words with invariable -s endings to skip processing and prevent orthographic errors.

        All words with 'invariable -s endings', not just nouns, should be added to this set to skip processing for them.
        For example, the 'invariable -s endings' rule correctly excludes the adverb 'across' from processing.
        """
        if self.__only_ending_s is None:
            self.__only_ending_s = get_file_unique_lines(self.only_ending_s_path)
        return self.__only_ending_s

    @property
    def singular_ending_non_s(self) -> set:
        """ Get singular nouns not ending in -s.

        First, populate this set with all singular nouns ending in '-fe'.
        Other cases of singular nouns not ending in -s (e.g., those ending in -f, -ch, -sh, -x, -z) are optional
        and intended for informational purposes only, rather than for controlling processing logic.
        """
        if self.__singular_ending_non_s is None:
            self.__singular_ending_non_s = get_file_unique_lines(self.singular_ending_non_s_path)
        return self.__singular_ending_non_s

    @property
    def irregular_plural_nouns(self) -> dict:
        """ Get a map of irregular nouns from plural to singular.

        This map is optional and contains irregular noun mappings for specific cases.
        For instance, the irregular nouns mapping correctly handles the plural 'feet' by converting it to the singular 'foot'.
        """
        if self.__irregular_plural_nouns is None:
            self.__irregular_plural_nouns = get_v2(self.irregular_plural_nouns_path)
        return self.__irregular_plural_nouns

    def __str__(self) -> str:
        """ Return the string representation of the object. """
        cur_str = (
        f"\n  {__class__}\n"
        f"  # SINGULARIZATION\n"
        f"  only_ending_s_path = {self.only_ending_s_path}\n"
        f"  singular_ending_non_s_path = {self.singular_ending_non_s_path}\n"
        f"  irregular_plural_nouns_path = {self.irregular_plural_nouns_path}\n"
        f"  reviewed_pairs_path = {self.reviewed_pairs_path}\n"
        f"  parsed_pairs_path = {self.parsed_pairs_path}\n"
        f"  unreviewed_pairs_path = {self.unreviewed_pairs_path}\n")
        return cur_str

    def str_path(self) -> str:
        """ Return the content of all used directories as a string. """
        cur_str = (
        f"# SINGULARIZATION\n"
        f"{str(self.only_ending_s_path.resolve())}\n"
        f"{str(self.singular_ending_non_s_path.resolve())}\n"
        f"{str(self.irregular_plural_nouns_path.resolve())}\n"
        f"{str(self.reviewed_pairs_path.resolve())}\n"
        f"{str(self.parsed_pairs_path.resolve())}\n"
        f"{str(self.unreviewed_pairs_path.resolve())}\n"
        )
        return cur_str

    def initialize(self):
        """ Initialize the object's attributes and set up its initial state.

        Runs only if initial data is missing from the /Document directory.
        """
        if not self.singular_ending_non_s_path.is_file():
            cur_set = get_file_unique_lines(self.__data_singular_ending_non_s_path)
            save_file(self.singular_ending_non_s_path, list(cur_set), True)

        if not self.only_ending_s_path.is_file():
            cur_set = get_file_unique_lines(self.__data_only_ending_s_path)
            save_file(self.only_ending_s_path, list(cur_set), True)

        if not self.irregular_plural_nouns_path.is_file():
            cur_set = get_file_unique_lines(self.__data_irregular_plural_nouns_path)
            save_file(self.irregular_plural_nouns_path, list(cur_set), True)

        if not self.reviewed_pairs_path.is_file():
            cur_set = get_file_unique_lines(self.__data_reviewed_pairs_path)
            save_file(self.reviewed_pairs_path, list(cur_set), True)