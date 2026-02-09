def get_yes_no_input(prompt_message: str, default: str = "yes") -> bool:
    """ Prompts the user for Yes/No input with a default value.

    The default value is used if the user just presses Enter.
    Valid inputs are "yes" ("y") and "no" ("n"), case-insensitive.
    Args:
        prompt_message (str): The question to ask the user.
        default (str, optional): The default choice ("yes" or "no"). Defaults to "yes".
    Returns:
        bool: True if the final answer is "yes", False if "no".
    """

    # Determine the hint message and valid empty responses
    if default == "yes":
        hint = "[Y/n]"
        valid_empty_response = "yes"
    elif default == "no":
        hint = "[y/N]"
        valid_empty_response = "no"
    else:
        # If no valid default is specified, make both required
        hint = "[y/n]"
        valid_empty_response = None
        default = None

    while True:
        user_input = input(f"{prompt_message} {hint}: ").lower().strip()

        if user_input == "":
            if valid_empty_response is not None:
                return valid_empty_response == "yes"
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")
                continue

        if user_input in ["yes", "y"]:
            return True
        elif user_input in ["no", "n"]:
            return False
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")