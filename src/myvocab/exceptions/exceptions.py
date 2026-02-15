class VocabError(Exception):
    """The base Vocab error."""

class DirectoryIsMountError(VocabError):
    """Raised when a directory is the root of a mounted filesystem."""
    def __init__(self, directory, message="Directory is the root of a mounted filesystem:"):
        self.directory = directory
        self.message = message   
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} '{self.directory}'"

class DirectoryIsSystemRootError(VocabError):
    """Raised when a directory is the System Root."""
    def __init__(self, directory, message="Directory is the System root:"):
        self.directory = directory
        self.message = message   
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} '{self.directory}'"

class DirectoryExclamationMarkError(VocabError):
    """Raised when a directory has the leading exclamation mark."""
    def __init__(self, directory, message="Directory has the leading exclamation mark:"):
        self.directory = directory
        self.message = message   
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} '{self.directory}'"

class DirectoryNotExistError(VocabError):
    """Raised when a directory is not exist."""
    def __init__(self, directory, message="Directory does not exist:"):
        self.directory = directory
        self.message = message   
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} '{self.directory}'"
    
class DirectoryIsNotFileError(VocabError):
    """Raised when a directory is not a file."""
    def __init__(self, directory, message="Directory is not a file:"):
        self.directory = directory
        self.message = message   
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} '{self.directory}'"

class DirectoryIsNotFolderError(VocabError):
    """Raised when a directory is not a folder."""
    def __init__(self, directory, message="The path is not a folder:"):
        self.directory = directory
        self.message = message   
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} '{self.directory}'"

class FileNameIsNotFileError(VocabError):
    """Raised when a filename is invalid."""
    def __init__(self, directory, message="Invalid filename:"):
        self.directory = directory
        self.message = message   
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} '{self.directory}'"

class NonBooleanValueError(VocabError):
    """Raised when a value is not of type boolean."""
    def __init__(self, directory, message="The value is not of type boolean:"):
        self.directory = directory
        self.message = message   
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} '{self.directory}'"

class IndexOutOfRangeError(VocabError):
    """Raised when an index out of range."""
    def __init__(self, directory, message="The index out of range:"):
        self.directory = directory
        self.message = message   
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} '{self.directory}'"

class IdentifierOutOfRangeError(VocabError):
    """Raised when an identifier out of range."""
    def __init__(self, identifier: int, out_range: range, message: str ="The identifier out of range:"):
        self.identifier = identifier
        self.range = out_range
        self.message = message   
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} {self.identifier} not in {self.range}"

class FileIsNotFoundError(VocabError):
    """Raised when a file is not found."""
    def __init__(self, file, message="The file is not found:"):
        self.file = file
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} '{self.file}'"

class FileIsEmptyError(VocabError):
    """Raised when a file is empty."""
    def __init__(self, file, message="The file is empty:"):
        self.file = file
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} '{self.file}'"

class VariableIsNotFoundError(VocabError):
    """Raised when a variable is not found."""
    def __init__(self, variable, message="The variable is not found:"):
        self.variable = variable
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} '{self.variable}'"

class ChunkSizeSmallError(VocabError):
    """Raised when a chunk size is too small."""

    def __init__(self, size, expected_size, message="The chunk size is too small:"):
        self.size = size
        self.expected_size = expected_size
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} {self.size} (expected {self.expected_size})"