from pathlib import Path
import logging
from src.myvocab.parsing.infinitive.data import path_file
from src.myvocab.parsing.commands.get_file_unique_lines import get_file_unique_lines
from src.myvocab.parsing.commands.save_file import save_file
from src.myvocab.parsing.commands.get_v_tuple import get_v3
from src.myvocab.parsing.commands.get_v_tuple import get_v2
from src.myvocab.parsing.commands.get_v_tuple import get_v1
from src.myvocab.parsing.commands.get_verbs_s import get_verbs_s

logger = logging.getLogger(__name__)

class InfinitAttrib:
    """ Infinitive transformation configuration

    The `Infinitive transformation configuration` is a structure designed to automatically generate and store
    a set of attributes used when converting verbs to their base forms.
    """

    __v3: dict = None
    __v2: dict = None
    __v1: dict = None
    __only_ending_ed: set = None
    __verbs_ending_e: set = None
    __verbs_ending_non_ed: set = None

    def __init__(self, dir_unique_id: str):
        """ Initialize the `Infinitive transformation configuration`.
        Args:
            dir_unique_id (str): Unique base directory.
        """
        self.__dir_unique_id = dir_unique_id
        self.initialize()

    @classmethod
    def infinit_attrib_verbs_ending_s(cls) -> set:
        """ Get irregular verbs ending in -s from the internal project data. """
        data_path: Path = Path(path_file.__file__).parent
        data_irregular_verbs_path: Path = Path.joinpath(data_path, "irregular_verbs.txt")
        cur_set = set()
        try:
            verbs = get_v1(data_irregular_verbs_path)
            cur_set.update(get_verbs_s(verbs))
            verbs = get_v2(data_irregular_verbs_path)
            cur_set.update(get_verbs_s(verbs))
            verbs = get_v3(data_irregular_verbs_path)
            cur_set.update(get_verbs_s(verbs))
        except Exception as e:
            logger.warning(f"Error while searching verbs ending -s: {e}")
            if not isinstance(cur_set, set):
                cur_set = set()

        return cur_set

    def verbs_ending_s(self):
        """ Get irregular verbs ending in -s from the external /Documents directory. """
        cur_set = set()
        try:
            verbs = get_v1(self.irregular_verbs_path)
            cur_set.update(get_verbs_s(verbs))
            verbs = get_v2(self.irregular_verbs_path)
            cur_set.update(get_verbs_s(verbs))
            verbs = get_v3(self.irregular_verbs_path)
            cur_set.update(get_verbs_s(verbs))
        except Exception as e:
            logger.warning(f"Error while searching verbs ending -s: {e}")
            if not isinstance(cur_set, set):
                cur_set = set()

        return cur_set

    # Infinitive
    __home = Path.home()
    __documents_path: Path = Path.joinpath(__home, "Documents")

    @property
    def infinitive_path(self):
        """ Get /Documents/Infinitive directory. """
        if self.__documents_path.exists() and self.__documents_path.is_dir():
            return Path.joinpath(self.__documents_path, self.__dir_unique_id, "Infinitive")
        else:
            return Path.joinpath(self.__home, self.__dir_unique_id, "Infinitive")

    # infinitive in
    @property
    def infinitive_in_path(self):
        """ Get /Documents/Infinitive/in directory. """
        return Path.joinpath(self.infinitive_path, "in")

    @property
    def irregular_verbs_path(self):
        """ Get /Documents/Infinitive/in/irregular_verbs.txt directory. """
        return Path.joinpath(self.infinitive_in_path, "irregular_verbs.txt")

    @property
    def only_ending_ed_path(self):
        """ Get /Documents/Infinitive/in/only_ending_ed.txt directory. """
        return Path.joinpath(self.infinitive_in_path, "only_ending_ed.txt")

    @property
    def verbs_ending_e_path(self):
        """ Get /Documents/Infinitive/in/verbs_ending_e.txt directory. """
        return Path.joinpath(self.infinitive_in_path, "verbs_ending_e.txt")

    @property
    def verbs_ending_non_ed_path(self):
        """ Get /Documents/Infinitive/in/verbs_ending_non_ed.txt directory. """
        return Path.joinpath(self.infinitive_in_path, "verbs_ending_non_ed.txt")

    @property
    def reviewed_pairs_path(self):
        """ Get /Documents/Infinitive/in/reviewed_pairs.txt directory. """
        return Path.joinpath(self.infinitive_in_path, "reviewed_pairs.txt")

    # infinitive out
    @property
    def infinitive_out_path(self):
        """ Get /Documents/Infinitive/out directory. """
        return Path.joinpath(self.infinitive_path, "out")

    @property
    def parsed_pairs_path(self):
        """ Get /Documents/Infinitive/out/parsed_pairs.txt directory. """
        return Path.joinpath(self.infinitive_out_path, "parsed_pairs.txt")

    @property
    def unreviewed_pairs_path(self):
        """ Get /Documents/Infinitive/out/unreviewed_pairs.txt directory. """
        return Path.joinpath(self.infinitive_out_path, "unreviewed_pairs.txt")

    # Initial data
    __data_path: Path = Path(path_file.__file__).parent
    __data_irregular_verbs_path: Path = Path.joinpath(__data_path, "irregular_verbs.txt")
    __data_only_ending_ed_path: Path = Path.joinpath(__data_path, "only_ending_ed.txt")
    __data_verbs_ending_e_path: Path = Path.joinpath(__data_path, "verbs_ending_e.txt")
    __data_verbs_ending_non_ed_path: Path = Path.joinpath(__data_path, "verbs_ending_non_ed.txt")
    __data_reviewed_pairs_path: Path = Path.joinpath(__data_path, "reviewed_pairs.txt")

    @property
    def only_ending_ed(self) -> set:
        """ Get words with invariable -ed endings to skip processing and prevent orthographic errors.

        All words with 'invariable -ed endings', not just verbs, should be added to this set to skip processing for them.
        For example, the 'invariable -ed endings' rule correctly excludes the noun 'bed' from processing.
        """
        if self.__only_ending_ed is None:
            self.__only_ending_ed = get_file_unique_lines(self.only_ending_ed_path)
        return self.__only_ending_ed

    @property
    def verbs_ending_e(self) -> set:
        """ Get the base form of the verbs ending in -e.

        The base form of the verbs ending in -e should be added to this set.
        For instance, the 'ending -e' rule correctly handles the verb 'freed', turning it into 'free'.
        """
        if self.__verbs_ending_e is None:
            self.__verbs_ending_e = get_file_unique_lines(self.verbs_ending_e_path)
        return self.__verbs_ending_e

    @property
    def verbs_ending_non_ed(self) -> set:
        """ Get the base form of the verbs `not ending in -ed` to halt processing and prevent errors in downstream logic.

        The base form of the verbs, without the -ed ending, should be added to this set solely to prevent incorrect processing by subsequent rules.
        For instance, the word 'willed' is caught to prevent the '2 consonants + ed' rule from applying and turning 'willed' into 'wil'.
        The 'not ending in -ed' rule correctly handles the verb 'willed', turning it into 'will'.
        """
        if self.__verbs_ending_non_ed is None:
            self.__verbs_ending_non_ed = get_file_unique_lines(self.verbs_ending_non_ed_path)
        return self.__verbs_ending_non_ed

    @property
    def verbs_v3(self) -> dict:
        """ Get the map of irregular verbs mapping V3 to V1. """
        if self.__v3 is None:
            self.__v3 = get_v3(self.irregular_verbs_path)
        return self.__v3

    @property
    def verbs_v2(self) -> dict:
        """ Get the map of irregular verbs mapping V2 to V1. """
        if self.__v2 is None:
            self.__v2 = get_v2(self.irregular_verbs_path)
        return self.__v2

    @property
    def verbs_v1(self) -> dict:
        """ Get the map of irregular verbs mapping V1 to V1. """
        if self.__v1 is None:
            self.__v1 = get_v1(self.irregular_verbs_path)
        return self.__v1

    def __str__(self):
        """ Return the string representation of the object. """
        cur_set = (
        f"\n  {__class__}\n"
        f"  # INFINITIVIZATION\n"
        f"  irregular_verbs_path = {self.irregular_verbs_path}\n"
        f"  only_ending_ed_path = {self.only_ending_ed_path}\n"
        f"  verbs_ending_e_path = {self.verbs_ending_e_path}\n"
        f"  verbs_ending_non_ed_path = {self.verbs_ending_non_ed_path}\n"
        f"  reviewed_pairs_path = {self.reviewed_pairs_path}\n"
        f"  parsed_pairs_path = {self.parsed_pairs_path}\n"
        f"  unreviewed_pairs_path = {self.unreviewed_pairs_path}\n")
        return cur_set
    
    def str_path(self) -> str:
        """ Return the content of all used directories as a string. """
        cur_set = (
        f"# INFINITIVIZATION\n"
        f"{str(self.irregular_verbs_path.resolve())}\n"
        f"{str(self.only_ending_ed_path.resolve())}\n"
        f"{str(self.verbs_ending_e_path.resolve())}\n"
        f"{str(self.verbs_ending_non_ed_path.resolve())}\n"
        f"{str(self.reviewed_pairs_path.resolve())}\n"
        f"{str(self.parsed_pairs_path.resolve())}\n"
        f"{str(self.unreviewed_pairs_path.resolve())}\n"
        )
        return cur_set

    def initialize(self):
        """ Initialize the object's attributes and set up its initial state.

        Runs only if initial data is missing from the /Document directory.
        """
        if not self.irregular_verbs_path.is_file():
            cur_set = get_file_unique_lines(self.__data_irregular_verbs_path)
            save_file(self.irregular_verbs_path, list(cur_set), True)

        if not self.reviewed_pairs_path.is_file():
            cur_set = get_file_unique_lines(self.__data_reviewed_pairs_path)
            save_file(self.reviewed_pairs_path, list(cur_set), True)

        if not self.only_ending_ed_path.is_file():
            cur_set = get_file_unique_lines(self.__data_only_ending_ed_path)
            save_file(self.only_ending_ed_path, list(cur_set), True)

        if not self.verbs_ending_e_path.is_file():
            cur_set = get_file_unique_lines(self.__data_verbs_ending_e_path)
            save_file(self.verbs_ending_e_path, list(cur_set), True)

        if not self.verbs_ending_non_ed_path.is_file():
            cur_set = get_file_unique_lines(self.__data_verbs_ending_non_ed_path)
            save_file(self.verbs_ending_non_ed_path, list(cur_set), True)