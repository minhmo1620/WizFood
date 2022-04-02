KB_HEADER = '''
%  Tell prolog that known/3 will be added later by asserta
:- dynamic known/3.
:- discontiguous ask/2.
:- discontiguous numberask/2.
:- discontiguous menuask/3.  
'''            

BASE_KB = [
    {'name': 'nasic_lemak',
    'preference': 'asian',
    'ingredients': ['rice', 'sambal', 'coconutmilk'],
    'calories': '644'},
    {'name': 'fried_rice', 'ingredients': ['rice'], 'fry': 'yes', 'calories': '800'},
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
    'ingredients': ['rice'],
    'meat': 'yes',
    'heavy_portion': 'yes',
    'calories': '2000'},
    {'name': 'baguette',
    'preference': 'western',
    'ingredients': ['bread'],
    'origin': 'france',
    'calories': '130'}
]

CALORIES_RULES = '''
abs(X, Y) :- Y is sign(X) * X.
calories(X, Y, Z) :- abs(X-Y, Z).
recommend(X) :- bagof(Y, food(Y), Z), expected_calories(M), min_difference(Z, M, X).

addElement(X, [], [X]). 
addElement(X, [Y | Rest], [X,Y | Rest]) :- X @< Y, !.
addElement(X, [Y | Rest1], [Y | Rest2]) :- addElement(X, Rest1, Rest2).

diff(Base, L, Z):- my_dict(Dc), R=Dc.L, calories(R, Base, Z).

min_difference([L|Ls], Base, X) :-
	diff(Base, L, Z),
    min_difference(Ls, Z, L, [L], Base, X).

min_difference([], Min, X0, X, Base, X).

min_difference([L|Ls], Min, X0, X1, Base, X) :-
	diff(Base, L, Z),
    Z = Min,
    addElement(L, X1, A),
    min_difference(Ls, Min, L, A, Base, X).

min_difference([L|Ls], Min, X0, A, Base, X) :-
	diff(Base, L, Z),
    Z > Min,
    min_difference(Ls, Min, X0, A, Base, X).

min_difference([L|Ls], Min, X0, A, Base, X) :-
	diff(Base, L, Z),
    Z < Min,
    min_difference(Ls, Min, L, [L], Base, X).
'''

RULES = """
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
