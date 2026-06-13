def join_current_target_words(current_word: str, target_word: str) -> str:
   """
   Join the current word with a target word by retaining the prefix of the current word
   for all case-insensitively matching characters, followed by appending the remaining suffix of the target word.
   """
   length = 0
   # Join the current word with a target word by retaining the prefix of the current word
   for curr, targ in zip(current_word, target_word):
      if curr.casefold() != targ.casefold():
         break
      # The counter is incremented while joining the current word with the target word
      length += 1
   # Append the remaining suffix of the target word
   return current_word[:length] + target_word[length:]