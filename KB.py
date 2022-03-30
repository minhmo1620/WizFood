KB_headers = '''
%  Tell prolog that known/3 will be added later by asserta
:- dynamic known/3.
:- discontiguous ask/2.
:- discontiguous numberask/2.
:- discontiguous menuask/3.  
'''            

question = {
    'preference': 'What is your preference food?',
    'expected_calories': 'How many calories do you want to eat today?',
    'origin': 'Which country do you to have food today?',
    'spicy': 'Do you want spicy food',
    'noodle': 'Do you want some noodle?',
    'use_rice': 'Do you want rice?',
    'has_sambal': 'Do you want samble?',
    'contain_coconutmilk': 'Do you want food that contains coconutmilk?',
    'fry': 'Do you want fried food?',
    'soup': 'Do you want soup?',
    'contain_meat': 'Do you want meat in your meal?',
    'heavy_portion': 'Do you want heavy portion food?',
    'use_bread': 'Do you want to have bread?'
}
food_data = [
    {'name': 'nasic_lemak',
    'preference': 'asian',
    'use_rice': 'yes',
    'has_sambal': 'yes',
    'contain_coconutmilk': 'yes',
    'calories': '644'},
    {'name': 'fried_rice', 'use_rice': 'yes', 'fry': 'yes', 'calories': '800'},
    {'name': 'dandan_noodle',
    'preference': 'asian',
    'soup': 'no',
    'origin': 'china',
    'calories': '378'},
    {'name': 'pho',
    'preference': 'asian',
    'soup': 'yes',
    'origin': 'vietnam',
    'calories': '400'},
    {'name': 'kebab',
    'preference': 'eastern',
    'contain_meat': 'yes',
    'use_rice': 'yes',
    'heavy_portion': 'yes',
    'calories': '2000'},
    {'name': 'baguette',
    'preference': 'western',
    'use_bread': 'yes',
    'origin': 'france',
    'calories': '130'}
]

calories_rules = '''
abs(X, Y) :- Y is sign(X) * X.
calories(X, Y, Z) :- abs(X-Y, Z).

recommend(X) :- bagof(Y, food(Y), Z), expected_calories(M), min_difference(Z, M, X).

diff(Base, L, Z):- my_dict(Dc), R=Dc.L, calories(R, Base, Z).

min_difference([L|Ls], Base, X) :- diff(Base, L, Z), min_difference(Ls, Z, L, Base, X).

min_difference([], Min, X, Base, X).
min_difference([L|Ls], Min, X0, Base, X) :- diff(Base, L, Z), Z >= Min, min_difference(Ls, Min, X0, Base, X).

min_difference([L|Ls], Min, X0, Base, X) :- diff(Base, L, Z), Z < Min, min_difference(Ls, Min, L, Base, X).
'''

askable_dict = {
    "expected_calories": {
        "type": "numberask",
        "question" : "How many calories do you want today?"
    },
    "preference": {
        "type": "menuask",
        "question": "",
        "choices": ["asian", "western", "eastern"]
    },
    "origin": {
        "type": "menuask",
        "question": "",
        "choices": ["vietnam", "france", "china"]
    },
    "spicy": {
        "type": "ask",
        "question": ""
    },
    "noodle": {
        "type": "ask",
        "question": ""
    },
    "use_rice": {
        "type": "ask",
        "question": ""
    },
    "has_sambal": {
        "type": "ask",
        "question": ""
    },
    "contain_coconutmilk": {
        "type": "ask",
        "question": ""
    },
    "fry": {
        "type": "ask",
        "question": ""
    },
    "soup": {
        "type": "ask",
        "question": ""
    },
    "spicy": {
        "type": "ask",
        "question": ""
    },
    "contain_meat": {
        "type": "ask",
        "question": ""
    },
    "heavy_portion": {
        "type": "ask",
        "question": ""
    },
    "use_bread": {
        "type": "ask",
        "question": ""
    },
}

rules = """
% Remember what I've been told is correct
ask(Attr, Val) :- known(yes, Attr, Val), !.
menuask(Attr, Val, _) :- known(yes, Attr, Val), !.
numberask(Attr, Val) :- known(yes, Attr, Val), !.

% Remember what I've been told is wrong
ask(Attr, Val) :- known(_, Attr, Val), !, fail.
menuask(Attr, Val, _) :- known(_, Attr, Val), !, fail.
numberask(Attr, Val) :- known(_, Attr, Val), !, fail.

% Remember when I've been told an attribute has a different value
ask(Attr, Val) :- known(yes, Attr, V), V \== Val, !, fail.
numberask(Attr, Val) :- known(yes, Attr, V), V \== Val, !, fail.
menuask(Attr, Val, _) :- known(yes, Attr, V), V \== Val, !, fail.

multivalued(ingredient).
multivalued(preference).
multivalued(origin).

ask(A, V):-
    known(yes, A, V), % succeed if true
    !.	% stop looking

ask(A, V):-
    known(_, A, V), % fail if false
    !, fail.

numberask(A, V):-
    known(yes, A, V), % succeed if true
    !.	% stop looking

numberask(A, V):-
    known(_, A, V), % fail if false
    !, fail.

% If not multivalued, and already known, don't ask again for a different value.
ask(A, V):-
    \+multivalued(A),
    known(yes, A, V2),
    V \== V2,
    !.

ask(A, V):-
    read_py_ask(A,V,Y), % get the answer
    asserta(known(Y, A, V)), % remember it
    write_py(known(Y, A, V)),
    Y == yes.	% succeed or fail

numberask(Attr, Val) :- 
    read_py_numberask(Attr, Val),
    asserta(known(yes, Attr, Val)),
    write_py(known(yes, Attr, Val)).

menuask(Attr, Val, List) :- 
    read_py_menuask(Attr, Ans, List),
    check_val(Ans, Attr, Val, List),
    asserta(known(yes, Attr, Ans)),
    write_py(known(yes, Attr, Ans)),
    Ans == Val.
    
check_val(Ans, _, _, List) :- 
    member(Ans, List), 
    !.
check_val(Ans, Attr, Val, List) :- 
    read_py_menuask(Attr, Ans, List),
    menuask(Attr, Val, List).
"""

