from pathlib import Path
from src.myvocab.parsing.singularization import singularization as sng
from src.myvocab.parsing.infinitive import infinitive as inf
from src.myvocab.validators import validators as vld
from src.myvocab.utils.logging_handler.set_file_handler import set_file_handler

class VocabConfig:
    """ Vocabulary configuration

    The Vocabulary configuration is a structure designed to automatically generate and store
    a set of attributes used for parsing text files, starting at the base directory.
    """

    __singular: sng.SingularAttrib = None
    __infinit: inf.InfinitAttrib = None
    __verbs_ending_s = set()

    def __init__(self, base_path: Path):
        """ Initialize the `Vocabulary configuration`.
        Args:
            base_path (Path): Base directory.
        """
        try:
            vld.validate_base_directory(base_path)
            self.__base_directory = base_path
            set_file_handler(self.log_file)
        except Exception:
            current_directory = Path.cwd()
            set_file_handler(Path.joinpath(current_directory, self.__LOG_FILE_NAME))
            raise

    __DIR_NAME: str = "Myvocab"
    __UNIQUE_ID: str = "58b254sv"
    __DIR_UNIQUE_ID: str = f"{__DIR_NAME}_{__UNIQUE_ID}"
    __SETTINGS_FILE_NAME: str = "settings.txt"
    __ALL_PATCHES_FILE_NAME: str = "view_all_used_paths.txt"
    __LOG_FILE_NAME: str = "app.log"

    __result_file_name: str = "vocabulary.txt"
    __directories_file_name: str = "directories.txt"

    # Flag to enable singular transformation
    use_lemma_singular: bool = True
    # Flag to enable infinitive transformation
    use_lemma_infinit: bool = True
    # Flag to enable translation
    use_word_translate: bool = False
    # Flag to enable ordering in the result vocabulary file
    use_order_text: bool = True
    # Flag to enable processing files and folders starting with "!"
    use_folder_with_leading_exclamation_mark: bool = False

    @property
    def dir_unique_id(self):
        """ Get the unique result directory name. """
        return self.__DIR_UNIQUE_ID

    @property
    def base_directory(self):
        """ Get the path to the parsing base directory. """
        return self.__base_directory

    @property
    def result_directory(self):
        """ Get the path to the result directory. """
        return Path.joinpath(self.base_directory, self.dir_unique_id)

    @property
    def log_file(self):
        """ Get the path to the log file. """
        return Path.joinpath(self.result_directory, self.__LOG_FILE_NAME)

    @property
    def result_file(self):
        """ Get the path to the result vocabulary file. """
        return Path.joinpath(self.result_directory, self.__result_file_name)

    @result_file.setter
    def result_file(self, result_file_name: str):
        """ Set the name of the result vocabulary file. """
        self.__result_file_name = result_file_name

    @property
    def directories_file(self):
        """ Get the path to the file representing the full directory tree during file parsing. """
        return Path.joinpath(self.result_directory, self.__directories_file_name)

    @directories_file.setter
    def directories_file(self, directories_file_name):
        """ Set the name of the file representing the full directory tree during file parsing. """
        self.__directories_file_name = directories_file_name

    @property
    def settings_file(self):
        """ Get the path to the settings file. """
        return Path.joinpath(self.result_directory, self.__SETTINGS_FILE_NAME)

    @property
    def all_patches_file(self):
        """ Get the path to the file that contains all used paths. """
        return Path.joinpath(self.result_directory, self.__ALL_PATCHES_FILE_NAME)

    @property
    def singular(self):
        """ Get the Singular transformation configuration. """
        return self.__singular

    def set_singular(self) -> None:
        """ Create a singular-transformer. """
        self.__singular = sng.SingularAttrib(self.dir_unique_id)

    @property
    def infinit(self):
        """ Get the Infinitive transformation configuration. """
        return self.__infinit

    def set_infinitive(self) -> None:
        """ Create an infinitive-transformer. """
        self.__infinit = inf.InfinitAttrib(self.dir_unique_id)

    @property
    def verbs_ending_s(self) -> set:
        """ Get verbs ending in -s. """
        return self.__verbs_ending_s

    @verbs_ending_s.setter
    def verbs_ending_s(self, value: set):
        """ Set verbs ending in -s. """
        self.__verbs_ending_s = value

    def __str__(self) -> str:
        """ Return the string representation of the object. """
        cur_str = (
        f"\n{'-'*40}\n"
        f"{__class__}\n"
        f"# VOCABULARY\n"
        f"dir_unique_id = {self.dir_unique_id}\n"
        f"base_directory = {self.base_directory}\n"
        f"result_directory = {self.result_directory}\n"
        f"result_file = {self.result_file}\n"
        f"directories_file = {self.directories_file}\n"
        f"settings_file = {self.settings_file}\n"
        f"all_patches_file = {self.all_patches_file}\n"
        f"log_file = {self.log_file}\n"
        f"use_lemma_singular = {self.use_lemma_singular}\n"
        f"use_lemma_infinit = {self.use_lemma_infinit}\n"
        f"use_word_translate = {self.use_word_translate}\n"
        f"use_order_text = {self.use_order_text}\n"
        f"use_folder_with_leading_exclamation_mark = {self.use_folder_with_leading_exclamation_mark}\n"
        f"{"" if self.singular is None else f"{self.singular}"}"
        f"{"" if self.infinit is None else f"{self.infinit}"}"
        f"{'-'*40}\n"
        )
        return cur_str

    def str_path(self) -> str:
        """ Return the content of all used directories as a string. """
        cur_str = (
        f"# VOCABULARY\n"
        f"{self.result_file}\n"
        f"{self.directories_file}\n"
        f"{self.settings_file}\n"
        f"{self.all_patches_file}\n"
        f"{self.log_file}\n"
        f"{"" if self.singular is None else f"{self.singular.str_path()}"}"
        f"{"" if self.infinit is None else f"{self.infinit.str_path()}"}"
        )
        return cur_str