import logging
from enum import Flag, auto
from src.myvocab.parsing.vocabulary import vocabulary as vcb
from src.myvocab.parsing.commands.transformer.get_init_data import get_init_data
from src.myvocab.parsing.commands.transformer.get_singular import get_singular_dict, get_singular_form
from src.myvocab.parsing.commands.transformer.get_infinit import get_infinit_dict, get_infinit_form
from src.myvocab.parsing.commands.transformer.get_casing import get_casing_dict, get_casing_form
from src.myvocab.constants import constants as cns

logger = logging.getLogger(__name__)


class Transformer(Flag):
    """ Applied transformer types """
    SINGULAR = auto()
    INFINITE = auto()
    CASING = auto()


def add_pair(pairs: dict, payload: dict) -> None:
    """ Store the word pair based on the transformer ID. """

    if payload["pair"] != "":
        if payload["id"] in cns.RANGE_SINGULAR_ID:
            pairs[Transformer.SINGULAR].add(payload["pair"])
        elif payload["id"] in cns.RANGE_INFINIT_ID:
            pairs[Transformer.INFINITE].add(payload["pair"])
        elif payload["id"] in cns.RANGE_CASING_ID:
            pairs[Transformer.CASING].add(payload["pair"])


def add_transformer(trns_list: Transformer, trns_name: Transformer) -> Transformer:
    """ Add a transformer to the list of transformers """
    if trns_list is None:
        trns_list = trns_name
    else:
        trns_list = trns_list | trns_name
    return trns_list


def get_transformer(vocab: vcb.VocabConfig, word: str, pairs: dict, transformers: Transformer = None) -> dict:
    """ Process a word through a transformer. """

    vdata = get_init_data(word)

    # Search for the input word in the dictionary
    if (vocab.use_lemma_casing
            and (transformers is None or Transformer.CASING in transformers)):
        vdata = get_casing_dict(vocab, vdata, word)
        add_pair(pairs, vdata)
    if vdata["id"] == cns.UNCHANGED_DATA_ID:
        if (vocab.use_lemma_singular
                and (transformers is None or Transformer.SINGULAR in transformers)):
            vdata = get_singular_dict(vocab, vdata)
            add_pair(pairs, vdata)
    if vdata["id"] == cns.UNCHANGED_DATA_ID:
        if (vocab.use_lemma_infinit
                and (transformers is None or Transformer.INFINITE in transformers)):
            vdata = get_infinit_dict(vocab, vdata)
            add_pair(pairs, vdata)

    # Singular-transformer
    if vdata["id"] == cns.UNCHANGED_DATA_ID:
        if (vocab.use_lemma_singular
                and (transformers is None or Transformer.SINGULAR in transformers)):
            # Skip singularizing irregular verbs ending in -s
            if word not in vocab.verbs_ending_s:
                vdata = get_singular_form(vocab, vdata)
                add_pair(pairs, vdata)
    # Infinite-transformer
    if vdata["id"] == cns.UNCHANGED_DATA_ID:
        if (vocab.use_lemma_infinit
                and (transformers is None or Transformer.INFINITE in transformers)):
            vdata = get_infinit_form(vocab, vdata)
            add_pair(pairs, vdata)
    # Casing-transformer
    if vdata["id"] not in cns.RANGE_CASING_ID:
        if (vocab.use_lemma_casing
                and (transformers is None or Transformer.CASING in transformers)):
            vdata = get_casing_form(vocab, vdata, word)
            add_pair(pairs, vdata)

    return vdata
