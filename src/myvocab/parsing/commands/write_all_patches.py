from src.myvocab.parsing.vocabulary import vocabulary as vcb

def write_all_patches(vocab: vcb.VocabConfig) -> None:
    """ Write all applied patches to a file.

    Save patches to 'vocab.all_patches_file'.

    Args:
        vocab (VocabConfig): 'Vocabulary configuration' object
    """

    if not vocab.all_patches_file.parent.exists():
        vocab.all_patches_file.parent.mkdir(exist_ok = True, parents = True)

    with open(vocab.all_patches_file, "w", encoding='utf-8') as file:
        file.write(vocab.str_path())