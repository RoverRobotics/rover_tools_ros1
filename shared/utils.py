
def user_says_yes(question:str):
    user_input = None
    while user_input != 'y' and user_input != 'n':
        user_input = input(question + " (y/n):")

    if user_input == 'y':
        return True
    else:
        return False