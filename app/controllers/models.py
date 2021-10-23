import tempfile
from pyswip.prolog import Prolog
from pyswip.easy import *

from app.controllers.model_helpers import *
from app.controllers.KB import ModelConfig


def run_model(user_answer):
    asked = {}
    # user_inputs  = [["asian", "yes", "no", "yes", "yes", "vietnam", 600], 0]
    user_inputs = [user_answer, 0]
    questions = []

    # Define foreign functions for getting user input and writing to the screen
    def write_py(X):
        sys.stdout.flush()
        return True

    def read_py_ask(A, V, Y):
        if isinstance(Y, Variable):
            # Asking for the input for the first time
            if A not in asked:
                # Create question
                questions.append(create_ask_question(A, V))
                # Ask user
                try:
                    user_input = read_input()
                except IndexError:
                    return False
                # Store the result in asked
                asked[A] = user_input
            # If the input matches the variable, put it as known in the knowledge base
            response = 'yes' if str(V) in asked[A] else 'no'
            Y.unify(response)
            return True
        else:
            return False

    def read_py_numberask(A, V):
        # V is Variable, V is number of calories in our context
        if isinstance(V, Variable):
            if A not in asked:
                questions.append(create_numberask_question(A))
                try:
                    user_input = read_input()
                except IndexError:
                    return False
                try:
                    asked[A] = int(user_input)
                except:
                    return False

            V.unify(asked[A])
            return True
        else:
            return False

    def read_py_menuask(A, X, MenuList):
        # X is a member of MenuList
        if isinstance(X, Variable):
            if A not in asked:
                questions.append(create_menuask_question(A, MenuList))
                try:
                    user_input = read_input()
                except IndexError:
                    return False
                asked[A] = user_input

            X.unify(asked[A])
            return True
        else:
            return False

    def read_input():
        current = user_inputs[1]
        user_inputs[1] += 1
        return user_inputs[0][current]

    prolog = Prolog()  # Global handle to interpreter

    retractall = Functor("retractall")
    known = Functor("known", 3)

    # Define the number of arity for each function
    write_py.arity = 1
    read_py_ask.arity = 3
    read_py_menuask.arity = 3
    read_py_numberask.arity = 2

    # Set
    registerForeign(read_py_ask)
    registerForeign(read_py_menuask)
    registerForeign(read_py_numberask)
    registerForeign(write_py)

    # Create a temporary file with the KB in it
    (FD, name) = tempfile.mkstemp(suffix='.pl', text=True)
    with os.fdopen(FD, "w") as text_file:
        text_file.write(ModelConfig.KB)
    prolog.consult(name)  # open the KB for consulting
    os.unlink(name)  # Remove the temporary file

    call(retractall(known))
    recommend = [s for s in prolog.query("recommend(D).")]
    if recommend:
        res = []
        for i in recommend:
            res.append(i['D'])

        questions.append('Our recommendation is:' + ''.join(str(e) for e in res))
    else:
        questions.append('unknown.')

    return questions[len(user_inputs[0])]


print(run_model(["asian", "yes", "no", "yes", "yes", "vietnam", 600]))
