% FACTS
parent('Queen Elizabeth II', 'Prince Charles').
parent('Queen Elizabeth II', 'Princess Anne').
parent('Queen Elizabeth II', 'Prince Andrew').
parent('Queen Elizabeth II', 'Prince Edward').
parent('Prince Phillip', 'Prince Charles').
parent('Prince Phillip', 'Princess Anne').
parent('Prince Phillip', 'Prince Andrew'). 
parent('Prince Phillip', 'Prince Edward').
parent('Princess Diana', 'Prince William').
parent('Princess Diana', 'Prince Harry').
parent('Prince Charles', 'Prince William').
parent('Prince Charles', 'Prince Harry').
parent('Captain Mark Phillips', 'Peter Phillips').
parent('Captain Mark Phillips', 'Zara Phillips').
parent('Princess Anne', 'Peter Phillips').
parent('Princess Anne', 'Zara Phillips').
parent('Sarah Ferguson', 'Princess Beatrice').
parent('Sarah Ferguson', 'Princess Eugenie').
parent('Prince Andrew', 'Princess Beatrice').
parent('Prince Andrew', 'Princess Eugenie').
parent('Sophie Rhys-jones', 'James, Viscount Severn').
parent('Sophie Rhys-jones', 'Lady Louise Mountbatten-Windsor').
parent('Prince Edward', 'James, Viscount Severn').
parent('Prince Edward', 'Lady Louise Mountbatten-Windsor').
parent('Prince William', 'Prince George').
parent('Prince William', 'Princess Charlotte').
parent('Kate Middleton', 'Prince George').
parent('Kate Middleton', 'Princess Charlotte').
parent('Autumn Kelly', 'Savannah Phillips').
parent('Autumn Kelly', 'Isla Phillips').
parent('Peter Phillips', 'Savannah Phillips').
parent('Peter Phillips', 'Isla Phillips').
parent('Zara Phillips', 'Mia Grace Tindall').
parent('Mike Tindall', 'Mia Grace Tindall').

married('Queen Elizabeth II', 'Prince Phillip').
married('Prince Phillip', 'Queen Elizabeth II').
married('Prince Charles', 'Camilla Parker Bowles').
married('Camilla Parker Bowles', 'Prince Charles').
married('Princess Anne', 'Timothy Laurence').
married('Timothy Laurence', 'Princess Anne').
married('Sophie Rhys-jones', 'Prince Edward').
married('Prince Edward', 'Sophie Rhys-jones').
married('Prince William', 'Kate Middleton').
married('Kate Middleton', 'Prince William').
married('Autumn Kelly', 'Peter Phillips').
married('Peter Phillips', 'Autumn Kelly').

divorced('Princess Diana', 'Prince Charles').
divorced('Prince Charlse', 'Princess Diana').
divorced('Captain Mark Phillips', 'Princess Anne').
divorced('Princess Anne', 'Captain Mark Phillips').
divorced('Sarah Ferguson', 'Prince Andrew').
divorced('Prince Andrew', 'Sarah Ferguson').

male('Prince Phillip').
male('Prince Charles').
male('Captain Mark Phillips').
male('Timothy Laurence').
male('Prince Andrew').
male('Prince Edward').
male('Prince William').
male('Prince Harry').
male('Peter Phillips').
male('Mike Tindall').
male('James, Viscount Severn').
male('Prince George').

female('Queen Elizabeth II').
female('Princess Diana').
female('Camilla Parker Bowles').
female('Princess Anne').
female('Sarah Ferguson').
female('Sophie Rhys-jones').
female('Kate Middleton').
female('Autumn Kelly').
female('Zara Phillips').
female('Princess Beatrice').
female('Princess Eugenie').
female('Lady Louise Mountbatten-Windsor').
female('Princess Charlotte').
female('Savannah Phillips').
female('Isla Phillips').
female('Mia Grace Tindall').

% RULES
husband(Person, Wife) :- male(Person), married(Person, Wife).

wife(Person, Husband) :- female(Person), married(Person, Husband).

father(Parent, Child) :- male(Parent), parent(Parent, Child).

mother(Parent, Child) :- female(Parent), parent(Parent, Child).

child(Child, Parent) :- parent(Parent, Child).

son(Child, Parent) :- male(Child), parent(Parent, Child).

daughter(Child, Parent) :- female(Child), parent(Parent, Child).

grandparent(GP, GC) :- parent(GP, Z), parent(Z, GC).

grandmother(GM, GC) :- mother(GM, Z), parent(Z, GC).

grandfather(GF, GC) :- father(GF, Z), parent(Z, GC).

grandchild(GC, GP) :- child(GC, Z), child(Z, GP).

grandson(GS, GP) :- son(GS, Z), child(Z, GP).

granddaughter(GD, GP) :- daughter(GD, Z), child(Z, GP).

sibling(Person1, Person2) :- child(Person1, Z), child(Person2, Z), \== Person1, Person2.

brother(Person, Sibling) :- male(Person), sibling(Person, Sibling).

sister(Person, Sibling) :- female(Person), sibling(Person, Sibling).

aunt(Person, NieceNephew) :- ((sister(Person, Z), parent(Z, NieceNephew), \+ parent(Person, NieceNephew)); (brother(Y, Z), parent(Z, NieceNephew), \+ parent(Y, NieceNephew), wife(Person, Y))).

uncle(Person, NieceNephew) :- ((brother(Person, Z), parent(Z, NieceNephew), \+ parent(Person, NieceNephew)); (sister(Y, Z), parent(Z, NieceNephew), \+ parent(Y, NieceNephew), husband(Person, Y))).

niece(Person, AuntUncle) :- daughter(Person, Z), (sibling(Z, AuntUncle); (married(AuntUncle, Y), sibling(Y, Z)))..

nephew(Person, AuntUncle) :- son(Person, Z), (sibling(Z, AuntUncle); (married(AuntUncle, Y), sibling(Y, Z))).

