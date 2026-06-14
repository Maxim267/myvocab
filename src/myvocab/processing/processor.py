import logging
import os
import re
from pathlib import Path

from src.myvocab.parsing.vocabulary import vocabulary as vcb
from src.myvocab.parsing.commands.load_settings import load_settings
from src.myvocab.parsing.commands.write_settings import write_settings
from src.myvocab.parsing.commands.write_all_patches import write_all_patches
from src.myvocab.parsing.commands.write_directories import write_directories
from src.myvocab.parsing.commands.get_singular import get_singular
from src.myvocab.parsing.commands.get_infinit import get_infinit
from src.myvocab.parsing.commands.save_file import save_file
from src.myvocab.parsing.commands.diff_two_files import diff_two_files
from src.myvocab.parsing.commands.get_init_data import get_init_data
from src.myvocab.parsing.commands.get_init_data import get_init_casing_data
from src.myvocab.parsing.commands.skip_current_dir import skip_current_dir
from src.myvocab.parsing.commands.get_casing import get_casing, log_casing
from src.myvocab.utils.walk_handler.handle_error import handle_error
from src.myvocab.utils.str_handler.combine_current_target_words import combine_current_target_words
from src.myvocab.validators import validators as vld
from src.myvocab.exceptions import exceptions as exc
from src.myvocab.constants import constants as cns
from src.myvocab.parsing.infinitive import infinitive as inf
from src.myvocab.translation.translator import translate
from src.myvocab.authentication.auth_yandex.function_iam.fetch_iam_func import fetch_iam_func
from src.myvocab.authentication.auth_yandex.account_iam.fetch_iam_oauth import fetch_iam_oauth
# from src.myvocab.authentication.auth_yandex.exchange_jwt_iam.create_iam_token import create_iam_token

logger = logging.getLogger(__name__)

def add_pair(payload: dict, pairs: dict) -> None:
   """ Store the word pair based on the transformer ID. """

   if payload["pair"] != "":
      if payload["id"] in cns.RANGE_SINGULAR_ID:
         pairs["singular"].add(payload["pair"])
      elif payload["id"] in cns.RANGE_INFINIT_ID:
         pairs["infinit"].add(payload["pair"])
      elif payload["id"] in cns.RANGE_CASING_ID:
         pairs["casing"].add(payload["pair"])

def get_transformer (word: str, vocab: vcb.VocabConfig) -> dict:
   """ Process a word through the first fitted transformer. """

   vdata = get_init_data(word)

   # Singular-transformer
   if vocab.use_lemma_singular:
      # Skip singularizing irregular verbs ending in -s
      if word not in vocab.verbs_ending_s:
         vdata = get_singular(word, vocab)
         if vdata["id"] != cns.UNCHANGED_DATA_ID:
            return vdata

   # Infinite-transformer
   if vocab.use_lemma_infinit:
      vdata = get_infinit(word, vocab)
      if vdata["id"] != cns.UNCHANGED_DATA_ID:
         return vdata

   return vdata

def get_case_transformer(vocab: vcb.VocabConfig, case_word: str, key_word: str, key_old: str = "") -> dict:
   """ Process a word through the casing transformer. """

   mixed_word = case_word

   if key_old != "" and key_old != key_word:
      # The verb form has been changed from V3 or V2 to V1
      if (vocab.use_lemma_infinit and key_old != key_word
              and key_word == vocab.infinit.verbs_v1.get(key_word)):
         mixed_word = combine_current_target_words(case_word, key_word)
      # The noun form has been changed to the singular
      elif (vocab.use_lemma_singular and key_old != key_word
              and key_word == vocab.singular.irregular_plural_nouns.get(key_old)):
         mixed_word = combine_current_target_words(case_word, key_word)

   vdata = get_init_data(key_word)

   # Casing-transformer
   if vocab.use_lemma_casing:
      vdata = get_casing(vocab, mixed_word, key_word)
      if vdata["id"] != cns.UNCHANGED_DATA_ID:
         return vdata

   return vdata

def remove_translation_marks(items: list) -> list:
   return_items = list(items)
   for index, item in enumerate(items):
      if find_list := re.findall(f'{cns.TAG_TRANSLATE}(.+)', item):
         return_items[index] = find_list[0]
   return return_items

def render_vocab(base_path: Path):
   """ Generate a vocabulary from the base directory.

   Any text outside the <<word>> and <</word>> tag-only strings is treated as raw file lines.
   Text enclosed in <<word>> and <</word>> tag-only strings is interpreted as a list of isolated English words,
   which can optionally be converted to their singular or infinitive forms and translated.
   Set options in the auto-generated base_directory/dir_unique_id/settings.txt.
   This directory contains all program output data.
   """

   # Create a new empty vocabulary
   vocab = vcb.VocabConfig(base_path)
   # Load settings from an existing file, otherwise persist defaults
   load_settings(vocab)

   # Add transformers
   if vocab.use_lemma_singular:
      vocab.set_singular(True)
   if vocab.use_lemma_infinit:
      vocab.set_infinitive(True)
   if vocab.use_lemma_casing:
      vocab.set_casing(True)

   # Get the list of verbs ending in -s
   verbs_s = set()
   if vocab.use_lemma_singular:
      # Get a list of irregular verbs ending in -s from the project files
      verbs_s.update(inf.InfinitAttrib.infinit_attrib_verbs_ending_s())
      if vocab.use_lemma_infinit:
         # and merge them with those stored in the Documents directory
         verbs_s.update(vocab.infinit.verbs_ending_s())
   vocab.verbs_ending_s = verbs_s

   logger.debug(vocab)

   # Persist settings to a file
   write_settings(vocab)

   write_all_patches(vocab)
   write_directories(vocab)

   parsed_pairs = {
      "singular": set(),
      "infinit": set(),
      "casing": set()
   }

   lines_list = list()
   lines_set = set()

   # Caching transformations for reuse
   transform_dict = dict()
   # Caching casing for reuse
   casing_dict = dict()
   # Caching translations for reuse
   translated_words = dict()

   trn_tag = ""
   if vocab.use_word_translate:
      # Tag for translation
      trn_tag = cns.TAG_TRANSLATE
      logger.info("Translation direction: " +
                  f"`{vocab.source_language}` to `{vocab.target_language}` " +
                  f"(`{vocab.source_language_code}` -> `{vocab.target_language_code}`)")

   logger.info("Populating a new vocabulary with isolated words and phrases ...")
   offset = len(vocab.base_directory.parts) - 1
   # If the PyInstaller executable sets the base directory to '.'
   if offset < 0:
      offset = 0

   # Show the `activity indicator`
   print("Parsing files: ", end="", flush=True)

   flag_next_file = False

   # Path.walk traverses the directory tree, starting from the base
   for dirpath, dirs, files in Path.walk(vocab.base_directory, on_error = handle_error):

      # The path is starting from the base directory.
      dirpath_parts = Path(*dirpath.parts[offset::])

      # Check if the current directory should be ignored
      if skip_current_dir(vocab, dirpath, dirpath_parts):
         continue

      for filename in files:

         # Text files only
         if not filename.endswith(".txt"):
            continue

         try:
            # Ignore files prefixed with '!' if 'use_dir_with_leading_exclamation_mark' flag is unset
            join_path = Path.joinpath(dirpath_parts, filename)
            vld.validate_directory_with_leading_exclamation_mark(join_path, vocab.use_dir_with_leading_exclamation_mark)
         except exc.VocabError:
            continue

         filepath = Path.joinpath(dirpath, filename)
         # Keep the `activity indicator` visible
         print(".", end="", flush=True)

         file_lines = list()
         file_list = list()
         file_set = set()
         # First words of sentences that are capitalized, but allow for lowercase as well
         first_words = set()

         # Read the current file
         with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

            # Extract the first words of sentences that are capitalized, but allow for lowercase as well
            if vocab.use_lemma_casing and (vocab.use_lemma_infinit or vocab.use_lemma_singular):
               firsts = set()
               firsts.update(re.findall(r'[.!?…—]["“”„]*[ \n]["“”„]*([A-Z][a-z0-9-]+)', content, re.MULTILINE))
               # Extract all words from a text
               alls = set()
               alls.update(re.findall(r'\b[a-zA-Z0-9-]+\b', content, re.MULTILINE))
               # Extract words that allow lowercase
               for word in firsts:
                  cur_word = word.lower()
                  # If the text contains the word in lowercase
                  if cur_word in alls:
                     first_words.add(word)
               # Remove processed words from the "firsts" set
               for word in first_words:
                  firsts.remove(word)

               # Transform the remaining words and check if they can be added to the 'first_words' set.
               logger.debug("Start transforming the words and adding some of them to the case set.")
               for word in firsts:
                  if word[0].isupper():
                     trans_data = get_transformer(word, vocab)
                     if trans_data["word"] != word.lower():
                        case_data = get_case_transformer(vocab, word, trans_data["word"], word.lower)
                        # Add the capitalized word to the set if a matching lowercase version is present
                        if case_data["word"].lower() in alls:
                           first_words.add(word)
               logger.debug("Finish transforming the words and adding some of them to the case set.")

            # Read lines from a file
            file_lines = re.findall(r'[^\n]+', content)

         t_word = False
         if not vocab.use_order_text:

            file_delimiter = str(Path.joinpath(dirpath_parts, filename)).ljust(80, '-')
            if flag_next_file:
               file_list.append(f"\n{file_delimiter}")
            else:
               flag_next_file = True
               file_list.append(f"{file_delimiter}")

         for file_line in file_lines:
            if file_line == cns.TAG_WORD:
               t_word = True
               continue
            elif file_line == cns.TAG_END_WORD:
               t_word = False
               continue

            if t_word:
               file_line_words = re.findall(r'\b[a-zA-Z0-9-]+\b', file_line)
               # Word list processing without any Transformer models
               if not (vocab.use_lemma_infinit or  vocab.use_lemma_singular or vocab.use_lemma_casing):
                  # Word list processing with using Casing
                  if vocab.use_lemma_casing:
                     cur_list = list()
                     for f_word in file_line_words:

                        # Convert the word to lowercase
                        if f_word in first_words:
                           f_word = f_word.lower()

                        if casing_word := casing_dict.get(f_word):
                           val = casing_word
                        else:
                           case_data = get_case_transformer(vocab, f_word, f_word.lower())

                           # Convert the word to lowercase
                           if case_data["word"] in first_words:
                              case_data["word"] = case_data["word"].lower()

                           add_pair(case_data, parsed_pairs)
                           casing_dict[f_word] = case_data["word"]
                           val = case_data["word"]
                        cur_list.append(val)
                     file_line_words = cur_list

                  # The words have been processed
                  if vocab.use_order_text and not vocab.use_word_translate:
                     file_set.update(file_line_words)
                  elif vocab.use_order_text:
                     for file_line_word in file_line_words:
                        file_set.add(trn_tag + file_line_word)
                  else:
                     for file_line_word in file_line_words:
                        if file_line_word not in file_set:
                           file_list.append(trn_tag + file_line_word)
                           file_set.add(file_line_word)
               else:
                  # Word processing using Transformers
                  for fl_word in file_line_words:

                     # Convert the word to lowercase
                     if fl_word in first_words:
                        fl_word = fl_word.lower()

                     lower_word = fl_word.lower()
                     # Exclude numbers
                     if re.match(r'\b[0-9]+\b', fl_word):
                        continue

                     # If the current word has already been processed
                     been_val = ""
                     if (vocab.use_lemma_casing
                             and (been_val := casing_dict.get(fl_word))):
                        pass
                     if been_val == "":
                        if ((vocab.use_lemma_infinit or vocab.use_lemma_singular)
                                and (been_val := transform_dict.get(lower_word))):
                           pass
                     if been_val is not None and been_val != "":
                        if vocab.use_order_text:
                           file_set.add(trn_tag +  been_val)
                        else:
                           if been_val not in file_set:
                              file_list.append(trn_tag + been_val)
                              file_set.add(been_val)
                        continue

                     # if the word contains a hyphen
                     is_multi = False
                     multi_words = None
                     # list of values for a given key in vocab.casing.mixed_casing dictionary
                     casing_mixed_list = None

                     # Skip hyphenated compound processing?
                     is_skip = vocab.use_lemma_infinit and lower_word in vocab.infinit.only_ending_ed
                     if not is_skip:
                        is_skip = vocab.use_lemma_singular and lower_word in vocab.singular.only_ending_s
                     if not is_skip:
                        is_skip = vocab.use_lemma_casing and (casing_mixed_list := vocab.casing.mixed_casing.get(lower_word)) and lower_word in [item.lower() for item in casing_mixed_list]
                     if not is_skip:
                        multi_words = re.split(r'-', fl_word)
                        if len(multi_words) > 1:
                           for m_word in multi_words:
                              if m_word != "":
                                 # Enable hyphenated compound processing
                                 is_multi = True
                                 break
                     # Hyphenated compound
                     if is_multi:
                        lower_phrase = ""
                        case_phrase = ""
                        source_phrase = ""
                        transform_data = get_init_data()
                        case_data = get_init_data()
                        trns_data_id = cns.UNCHANGED_DATA_ID

                        for multi_word in multi_words:

                           # Convert the word to lowercase
                           if multi_word in first_words:
                              multi_word = multi_word.lower()

                           lower_multi_word = multi_word.lower()
                           if multi_word != "":
                              if lower_phrase != "":
                                 lower_phrase += "-"
                              if case_phrase != "":
                                 case_phrase += "-"
                                 source_phrase += "-"

                              # Proceed with the transform using infinite or singular
                              if trans_val := transform_dict.get(lower_multi_word):
                                 lower_phrase = lower_phrase + trans_val
                              else:
                                 transform_data = get_transformer(lower_multi_word, vocab)
                                 transform_dict[lower_multi_word] = transform_data["word"]
                                 lower_phrase = lower_phrase + transform_data["word"]
                                 trans_val = transform_data["word"]
                                 if transform_data["id"] != cns.UNCHANGED_DATA_ID:
                                    trns_data_id = transform_data["id"]
                              # Proceed with the casing
                              if vocab.use_lemma_casing:
                                 if casing_word := casing_dict.get(trans_val):
                                    case_phrase = case_phrase + casing_word
                                    source_phrase = source_phrase + multi_word[:len(casing_word)]
                                 else:
                                    case_data = get_case_transformer(vocab, multi_word, trans_val, lower_multi_word)

                                    # Convert the word to lowercase
                                    if case_data["word"] in first_words:
                                       case_data["word"] = case_data["word"].lower()

                                    casing_dict[multi_word] = case_data["word"]
                                    case_phrase = case_phrase + case_data["word"]
                                    source_phrase = source_phrase + multi_word[:len(case_data["word"])]
                                    if case_data["id"] != cns.UNCHANGED_DATA_ID:
                                       trns_data_id = case_data["id"]
                        # The hyphenated phrase has been processed
                        if lower_phrase != "":
                           transform_dict[lower_word] = lower_phrase
                           # A specific casing rule was applied
                           if vocab.use_lemma_casing and trns_data_id in cns.RANGE_CASING_ID:
                              casing_dict[fl_word] = case_phrase
                              case_data["id"] = cns.RANGE_CASING_MAX_ID
                              case_data["pair"] = "" if fl_word == case_phrase else f"{fl_word} - {case_phrase}"
                              add_pair(case_data, parsed_pairs)

                              # Log a specific rule
                              hyphen_word = case_phrase
                              log_casing(get_init_casing_data(), f"{source_phrase} -> {case_phrase}")
                           # A specific transform rule was applied
                           else:
                              # Log a specific rule
                              hyphen_word = lower_phrase
                              if lower_phrase != lower_word:
                                 if vocab.use_lemma_infinit and trns_data_id in cns.RANGE_INFINIT_ID:
                                    transform_data["id"] = cns.RANGE_INFINIT_MAX_ID
                                 else:
                                    transform_data["id"] = cns.RANGE_SINGULAR_MAX_ID
                                 case_data["pair"] = "" if lower_word == lower_phrase else f"{lower_word} - {lower_phrase}"
                                 add_pair(transform_data, parsed_pairs)
                           # The word has been processed
                           if vocab.use_order_text:
                              file_set.add(trn_tag + hyphen_word)
                           else:
                              if hyphen_word not in file_set:
                                 file_list.append(trn_tag + hyphen_word)
                                 file_set.add(hyphen_word)
                     else:
                        sng_word = ""
                        # A populated list serves as a flag to apply 'Before' casing
                        if casing_mixed_list is not None and casing_mixed_list:
                           case_data = get_case_transformer(vocab, fl_word, lower_word)

                           # Convert the word to lowercase
                           if case_data["word"] in first_words:
                              case_data["word"] = case_data["word"].lower()

                           if case_data["id"] != cns.UNCHANGED_DATA_ID:
                              add_pair(case_data, parsed_pairs)
                              casing_dict[fl_word] = case_data["word"]
                              sng_word = case_data["word"]
                        # 'Before' casing did not work. Proceed with the transform using infinite or singular
                        if sng_word == "":
                           transform_data = get_transformer(lower_word, vocab)
                           transform_dict[lower_word] = transform_data["word"]
                           add_pair(transform_data, parsed_pairs)
                           sng_word = transform_data["word"]
                           # Proceed with the 'After' casing
                           if vocab.use_lemma_casing:
                              case_data = get_case_transformer(vocab, fl_word, sng_word, lower_word)

                              # Convert the word to lowercase
                              if case_data["word"] in first_words:
                                 case_data["word"] = case_data["word"].lower()

                              add_pair(case_data, parsed_pairs)
                              casing_dict[fl_word] = case_data["word"]
                              sng_word = case_data["word"]

                        # The word has been processed
                        if vocab.use_order_text:
                           file_set.add(trn_tag + sng_word)
                        else:
                           if sng_word not in file_set:
                              file_list.append(trn_tag + sng_word)
                              file_set.add(sng_word)
            else:
               file_line = file_line.strip()
               if file_line != '':
                  if vocab.use_order_text:
                     file_set.add(file_line)
                  else:
                     if file_line not in file_set:
                        file_list.append(file_line)
                        file_set.add(file_line)

         if vocab.use_order_text:
            lines_set.update(file_set)
         else:
            lines_list.extend(file_list)

   if vocab.use_order_text:
      all_list = list(lines_set)
   else:
      all_list = list(lines_list)

   # Restore word wrap after using the activity indicator
   print("")

   if vocab.use_word_translate:

      auth = os.getenv('AUTH')
      logger.info(f"auth: {auth}")

      iam_token = None
      transl_words = None

      if auth == 'account_iam':
         # To get an IAM token with a Yandex account
         vdata = fetch_iam_oauth()
         if vdata.get("ok") and (iam_token := vdata.get("iamToken")):
            transl_words = None if vocab.use_order_text else translated_words
         else:
            all_list = remove_translation_marks(all_list)
            logger.error("Failed to fetch IAM token while preparing to translate.")
      elif auth == 'exchange_jwt_iam':
         # To get an IAM token with an Authorized keys.
         try:
            iam_token = create_iam_token()
            transl_words = None if vocab.use_order_text else translated_words
         except Exception as e:
            all_list = remove_translation_marks(all_list)
            logger.error(f"Failed to fetch IAM token while preparing to translate: {e}")
      else:
         # To get an IAM token from the function code in Yandex Cloud Functions
         vdata = fetch_iam_func()
         if iam_token := vdata.get("access_token"):
            transl_words = None if vocab.use_order_text else translated_words
         else:
            all_list = remove_translation_marks(all_list)
            logger.error("Failed to fetch IAM token while preparing to translate.")

      if iam_token is not None and iam_token != "":
         all_list = translate(
            iam = iam_token,
            words = all_list,
            target_language_code = vocab.target_language_code,
            result_directory = vocab.result_file.parent,
            translated_words = transl_words)
   else:
      # Delete both the sent and received API translation files
      translate_path = Path.joinpath(vocab.result_directory, cns.TRANSLATE_FOLDER)
      if translate_path.exists() and translate_path.is_dir():
         # Loop through and delete files only
         for file_path in translate_path.iterdir():
            if file_path.is_file():
               file_path.unlink()

   # Vocabulary
   if not vocab.result_file.is_file():
      vocab.result_file.parent.mkdir(exist_ok = True, parents = True)
   # Write the vocabulary to a file
   save_file(vocab.result_file, all_list, vocab.use_order_text)
   logger.info(f"The resulting vocabulary has been created: \n{vocab.result_file.resolve()}")

   # Singularization
   if vocab.use_lemma_singular:
      # Write all pairs of original plural words and their singularized versions to the `singular.parsed_pairs_path` directory.
      save_file(vocab.singular.parsed_pairs_path, list(parsed_pairs["singular"]), vocab.use_order_text)

      # This allows the user to potentially analyze the applied transformations.
      # Some or all transformations validated by the user may be copied to the `singular.reviewed_pairs_path` directory.

      # Get the remaining unverified transformation.
      unreviewed_pairs = diff_two_files(vocab.singular.parsed_pairs_path, vocab.singular.reviewed_pairs_path)
      # Write the remaining unverified transformation to the `singular.unreviewed_pairs_path` directory.
      save_file(vocab.singular.unreviewed_pairs_path, unreviewed_pairs, vocab.use_order_text)
   else:
      # Save empty files
      if vocab.singular is None:
         vocab.set_singular(False)
      save_file(vocab.singular.parsed_pairs_path, list(), False)
      save_file(vocab.singular.unreviewed_pairs_path, list(), False)

   # Infinitive
   if vocab.use_lemma_infinit:
      # Write all pairs of original words and their base forms to the infinit.`infinit.parsed_pairs_path` directory.
      save_file(vocab.infinit.parsed_pairs_path, list(parsed_pairs["infinit"]), vocab.use_order_text)

      # This allows the user to potentially analyze the applied transformations.
      # Some or all transformations validated by the user may be copied to the `infinit.reviewed_pairs_path` directory.

      # Get the remaining unverified transformation.
      unreviewed_pairs = diff_two_files(vocab.infinit.parsed_pairs_path, vocab.infinit.reviewed_pairs_path)
      # Write the remaining unverified transformation to the `infinit.unreviewed_pairs_path` directory.
      save_file(vocab.infinit.unreviewed_pairs_path, unreviewed_pairs, vocab.use_order_text)
   else:
      # Save empty files
      if vocab.infinit is None:
         vocab.set_infinitive(False)
      save_file(vocab.infinit.parsed_pairs_path, list(), False)
      save_file(vocab.infinit.unreviewed_pairs_path, list(), False)

   # Casing
   if vocab.use_lemma_casing:
      # Write all pairs of original words and their casing forms to the casing.`casing.parsed_pairs_path` directory.
      save_file(vocab.casing.parsed_pairs_path, list(parsed_pairs["casing"]), vocab.use_order_text)

      # This allows the user to potentially analyze the applied transformations.
      # Some or all transformations validated by the user may be copied to the `casing.reviewed_pairs_path` directory.

      # Get the remaining unverified transformation.
      unreviewed_pairs = diff_two_files(vocab.casing.parsed_pairs_path, vocab.casing.reviewed_pairs_path)
      # Write the remaining unverified transformation to the `casing.unreviewed_pairs_path` directory.
      save_file(vocab.casing.unreviewed_pairs_path, unreviewed_pairs, vocab.use_order_text)
   else:
      # Save empty files
      if vocab.casing is None:
         vocab.set_casing(False)
      save_file(vocab.casing.parsed_pairs_path, list(), False)
      save_file(vocab.casing.unreviewed_pairs_path, list(), False)