from app.controllers.KB import ModelConfig


def validate_input(A, user_input):
    """
    Validate the input from users
    Input: A - name of askable
           user_input - str: the input from users
    Output:
    - True/False: whether the input is valid or not
    - user_input list after process
    - error: return the error of the input
    """
    # Slit all values by comma and strip white spaces
    inputs = [x.strip() for x in user_input.split(',') if x.strip()]

    # Get all possible values for askable(A) - this is a dict
    possible_values = ModelConfig.askables_values[str(A)]

    # list containing answers of users based on the number they chose
    res = []

    # We allow askable symptoms to have multiple input
    if str(A) != 'symptoms':
        if len(inputs) != 1:
            return False, [], 'Please choose ONE number'

    # Check the inputs
    for i in inputs:
        try:
            # whether i is integer and i in the possile_values
            if int(i) in possible_values:

                # Add to the result list the value based on the key - int(i)
                res.append(possible_values[int(i)])
            else:
                # Choose out of range number
                if int(i) > len(possible_values):
                    error = 'Please choose integer in range 1-' + str(len(possible_values))
                else:
                    # All other errors will be invalid input
                    error = 'Invalid input'
                return False, [], error
        except:
            # Error: Wrong type
            error = 'Please choose integer in range 1-' + str(len(possible_values))
            return False, [], error

    return True, res, None


def create_ask_question(A, V):
    """
    Create question to ask users includes
    - questions for askables
    - options with numbered list
    - error for previous input
    """
    if str(A) == 'ingredient':
        askable_question = 'Do you want ' + str(V) + ' ?'
    else:
        askable_question = str(ModelConfig.question[str(A)])
    return askable_question + '\n' + 'Your answer is: '


def create_numberask_question(A):
    """
    Create questions to ask for number
    """
    return ModelConfig.question[str(A)] + '\n' + 'Your answer is: ' if str(A) in ModelConfig.question else str(A)


def create_menuask_question(A, menu):
    """
    Create questions to have menuasks
    """
    menuask_question = ModelConfig.question[str(A)]
    menu_list = 'Please choose your preference: ' + ', '.join(map(str, menu))

    return menuask_question + '\n' + menu_list + '\n' + 'Your answer is: '
