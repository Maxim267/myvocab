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
from src.myvocab.parsing.commands.skip_current_dir import skip_current_dir
from src.myvocab.utils.walk_handler.handle_error import handle_error
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

def set_transformer (word: str, vocab: vcb.VocabConfig) -> dict:
   """ Process a word through the first fitted transformer. """

   vdata = get_init_data(word)

   # Singular-transformer
   if vocab.use_lemma_singular:
      # Skip singularizing verbs ending in -s
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
      vocab.set_singular()
   if vocab.use_lemma_infinit:
      vocab.set_infinitive()

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
      "infinit": set()
   }

   lines_list = list()
   lines_set = set()

   # Caching transformations for reuse
   transform_dict = dict()
   # Caching translations for reuse
   translated_words = dict()

   trn_tag = ""
   if vocab.use_word_translate:
      # Tag for translation
      trn_tag = cns.TAG_TRANSLATE

   logger.info("Populating a new vocabulary with isolated words and phrases ...")
   offset = len(vocab.base_directory.parts) - 1

   # Show the `activity indicator`
   print(f"Parsing files: ", end="", flush=True)

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
            # Ignore files prefixed with '!' if 'use_folder_with_leading_exclamation_mark' flag is unset
            join_path = Path.joinpath(dirpath_parts, filename)
            vld.validate_directory_with_leading_exclamation_mark(join_path, vocab.use_folder_with_leading_exclamation_mark)
         except exc.VocabError:
            continue

         filepath = Path.joinpath(dirpath, filename)

         # Keep the `activity indicator` visible
         print(f".", end="", flush=True)

         file_lines = list()
         file_list = list()
         file_set = set()

         # Read the current file
         with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            # Read lines from a file
            file_lines = re.findall(r'[^\n]+', content)

         t_word = False
         if not vocab.use_order_text:

            cur_str = str(Path.joinpath(dirpath_parts, filename)).ljust(80, '-')
            if flag_next_file:
               file_list.append(f"\n{cur_str}")
            else:
               flag_next_file = True
               file_list.append(f"{cur_str}")

         for file_line in file_lines:
            if file_line == cns.TAG_WORD:
               t_word = True
               continue
            elif file_line == cns.TAG_END_WORD:
               t_word = False
               continue

            if t_word:
               file_line_words = re.findall(r'\b[a-zA-Z0-9-]+\b', file_line.lower())

               # Word list processing without using Transformers
               if not (vocab.use_lemma_infinit or  vocab.use_lemma_singular):

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
                  for word in file_line_words:
                     # Exclude numbers
                     if re.match(r'\b[0-9]+\b', word):
                           continue
                     # If the current word has already been processed
                     if val := transform_dict.get(word):
                        if vocab.use_order_text:
                           file_set.add(trn_tag + val)
                        else:
                           if val not in file_set:
                              file_list.append(trn_tag + val)
                              file_set.add(val)
                        continue

                     # if the word contains a hyphen
                     is_multi = False
                     multi_words = re.split(r'-', word)
                     if len(multi_words) > 1:
                        for m_word in multi_words:
                           if m_word != "":
                              is_multi = True
                              break
                     # Hyphenated compound
                     if is_multi:
                        phrase = ""
                        # data_list = list()
                        for m_word in multi_words:
                           if m_word != "":
                              if phrase != "":
                                 phrase += "-"
                              # Hyphenated word ending in -s or -ed (e.g., passers-by; strong-willed)
                              transform_data = set_transformer(m_word, vocab)
                              # data_list.append(transform_data)
                              phrase = phrase + transform_data["word"]
                        if phrase != "":
                           transform_dict[word] = phrase
                           # Keep the resulting Hyphenated compounds and their parsing pair
                           init_data = get_init_data(trn_tag + phrase)
                           if phrase != word:
                              init_data["pair"] = word + " - " + phrase
                           add_pair(init_data, parsed_pairs)
                           if vocab.use_order_text:
                              file_set.add(trn_tag + phrase)
                           else:
                              if phrase not in file_set:
                                 file_list.append(trn_tag + phrase)
                                 file_set.add(phrase)
                     else:
                        transform_data = set_transformer(word, vocab)
                        transform_word = transform_data["word"]
                        transform_dict[word] = transform_word
                        transform_data["word"] = trn_tag + transform_word
                        add_pair(transform_data, parsed_pairs)
                        if vocab.use_order_text:
                           file_set.add(trn_tag + transform_word)
                        else:
                           if transform_word not in file_set:
                              file_list.append(trn_tag + transform_word)
                              file_set.add(transform_word)
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

      if auth == 'account_iam':
         # To get an IAM token with a Yandex account
         vdata = fetch_iam_oauth()
         if vdata.get("ok") and vdata.get("iamToken"):
            translated = None if vocab.use_order_text else translated_words
            all_list = translate(vdata.get("iamToken"), all_list, vocab.result_file.parent, translated)
         else:
            logger.error(f"Failed to retrieve the Translate API token.")

      elif auth == 'exchange_jwt_iam':
         # To get an IAM token with an Authorized keys.
         try:
            iam_token = create_iam_token()
            translated = None if vocab.use_order_text else translated_words
            all_list = translate(iam_token, all_list, vocab.result_file.paren, translated)
         except Exception as e:
            logger.error(f"Failed to retrieve the Translate API token: {e}")

      else:
         # To get an IAM token from the function code in Yandex Cloud Functions
         vdata = fetch_iam_func()
         if vdata.get("access_token"):
            translated = None if vocab.use_order_text else translated_words
            all_list = translate(vdata.get("access_token"), all_list, vocab.result_file.parent, translated)
         else:
            logger.error(f"Failed to retrieve the Translate API token.")

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