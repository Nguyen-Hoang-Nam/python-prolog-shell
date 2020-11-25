% chu de: company
% facts
male('Tobey Maguire').
male('Mr. Ditkovitch').
male('Joker').
male('Spiderman').
male('Jona Jameson').
male('Bully Maguire').
male('Kyle Craven').
male('Drew Scanlon').
male('Erlich Bachman').
male('Norman Osborn').
male('Uncle Ben').
male('Bruce Wayne').
male('Alfred Pennyworth').
female('Chuck Norris').
female('Gimme Rent').
female('Doge').
female('Mary Jane').
female('May Parker').
female('Karen').
female('Gwen Stacy').
female('Goblin Junior').

position('Tobey Maguire', 'CEO').
position('Mr. Ditkovitch', 'CFO').
position('Joker', 'Sales manager').
position('Spiderman', 'CTO').
position('Jona Jameson', 'Product manager').
position('Bully Maguire', 'Lead').
position('Kyle Craven', 'Back-end dev').
position('Drew Scanlon', 'Back-end tester').
position('Erlich Bachman', 'Intern').
position('Norman Osborn', 'Product designer').
position('Uncle Ben', 'CMO').
position('Bruce Wayne', 'Graphic design').
position('Alfred Pennyworth', 'Marketing writer').
position('Chuck Norris', 'CRO').
position('Gimme Rent', 'Accountant').
position('Doge', 'Back-end dev').
position('Mary Jane', 'Sales').
position('May Parker', 'Front-end dev').
position('Karen', 'Front-end tester').
position('Gwen Stacy', 'QA engineer').
position('Goblin Junior', 'Director of marketing').

rich('Tobey Maguire').
rich('Jona Jameson').
rich('Bully Maguire').
rich('Erlich Bachman').
rich('Norman Osborn').
rich('Bruce Wayne').
rich('Gimme Rent').
rich('Doge').
rich('Gwen Stacy').
rich('Goblin Junior').

domain('Finance').
domain('Risk').
domain('Technology').
domain('Marketing').

manage('Tobey Maguire', 'Mr. Ditkovitch').
manage('Tobey Maguire', 'Chuck Norris').
manage('Tobey Maguire', 'Spiderman').
manage('Tobey Maguire', 'Uncle Ben').
manage('Mr. Ditkovitch', 'Gimme Rent').
manage('Chuck Norris', 'Joker').
manage('Joker', 'Mary Jane').
manage('Spiderman', 'Jona Jameson').
manage('Jona Jameson', 'Bully Maguire').
manage('Jona Jameson', 'Norman Osborn').
manage('Jona Jameson', 'Gwen Stacy').
manage('Bully Maguire', 'Doge').
manage('Bully Maguire', 'Kyle Craven').
manage('Bully Maguire', 'Drew Scanlon').
manage('Bully Maguire', 'Erlich Bachman').
manage('Bully Maguire', 'May Parker').
manage('Bully Maguire', 'Karen').
manage('Uncle Ben', 'Goblin Junior').
manage('Goblin Junior', 'Bruce Wayne').
manage('Goblin Junior', 'Alfred Pennyworth').

friend('Tobey Maguire', 'Bully Maguire').
friend('Bully Maguire', 'Tobey Maguire').
friend('Spiderman', 'Uncle Ben').
friend('Uncle Ben', 'Spiderman').
friend('Chuck Norris', 'Karen').
friend('Karen', 'Chuck Norris').

domain_position('Finance', 'CFO').
domain_position('Risk', 'CRO').
domain_position('Technology', 'CTO').
domain_position('Marketing', 'CMO').
domain_position('Finance', 'Accountant').
domain_position('Risk', 'Sales Manager').
domain_position('Risk', 'Sales').
domain_position('Technology', 'Product manager').
domain_position('Technology', 'Lead').
domain_position('Technology', 'Back-end dev').
domain_position('Technology', 'Back-end tester').
domain_position('Technology', 'Intern').
domain_position('Technology', 'Front-end dev').
domain_position('Technology', 'Front-end tester').
domain_position('Technology', 'Product designer').
domain_position('Technology', 'QA engineer').
domain_position('Marketing', 'Director of marketing').
domain_position('Marketing', 'Graphic design').
domain_position('Marketing', 'Marketing writer').

employee(Person) :- position(Person, _), \+ position(Person, 'CEO').

chief_in_domain(Person, Domain) :- ((== Domain, 'Finance', position(Person, 'CFO')); (== Domain, 'Risk', position(Person, 'CRO')); (== Domain, 'Technology', position(Person, 'CTO')); (== Domain, 'Marketing', position(Person, 'CMO'))).

male_chief_in_domain(Person, Domain) :- male(Person), chief_in_domain(Person, Domain).

female_chief_in_domain(Person, Domain) :- female(Person), chief_in_domain(Person, Domain).

is_chief(Person) :- (position(Person, 'CEO'); position(Person, 'CFO'); position(Person, 'CRO'); position(Person, 'CTO'); position(Person, 'CMO')).

domain_has_manager(Domain, Person) :- ((== Domain, 'Risk', position(Person, 'Sales manager')); (== Domain, 'Technology', position(Person, 'Product manager'))).

domain_has_director(Domain, Person) :- == Domain, 'Marketing', position(Person, 'Director of marketing').

male_in_position(Person, Position) :- male(Person), position(Person, Position).

female_in_position(Person, Position) :- female(Person), position(Person, Position).

in_domain(Person, Domain) :- domain_position(Domain, Z), position(Person, Z).

friend_with_chief(Person, Chief) :- friend(Person, Chief), is_chief(Chief).

friend_with_rich(Person1, Person2) :- friend(Person1, Person2), rich(Person2).

friends_different_domain(Person1, Person2) :- friend(Person1, Person2), in_domain(Person1, Z), in_domain(Person2, X), \== Z, X.

male_in_domain(Person, Domain) :- male(Person), domain_position(Domain, Z), position(Person, Z).

female_in_domain(Person, Domain) :- female(Person), domain_position(Domain, Z), position(Person, Z).

male_manager(Person) :- male(Person), (domain_has_manager('Risk', Person); domain_has_manager('Technology', Person)).

female_manager(Person) :- female(Person), (domain_has_manager('Risk', Person); domain_has_manager('Technology', Person)).

male_director(Person) :- male(Person), domain_has_director('Marketing', Person).

female_director(Person) :- female(Person), domain_has_director('Marketing', Person).

same_domain(Person1, Person2) :- \== Person1, Person2, in_domain(Person1, Z), in_domain(Person2, Z).

same_manager(Person1, Person2) :- manage(Z, Person1), manage(Z, Person2), \== Person1, Person2.

ceo(Person) :- position(Person, 'CEO').

male_ceo(Person) :- male(Person), position(Person, 'CEO').

female_ceo(Person) :- female(Person), position(Person, 'CEO').

developer(Person) :- (position(Person, 'Back-end dev'); position(Person, 'Front-end dev'); position(Person, 'Intern')).

male_developer(Person) :- male(Person), (position(Person, 'Back-end dev'); position(Person, 'Front-end dev'); position(Person, 'Intern')).

female_developer(Person) :- female(Person), (position(Person, 'Back-end dev'); position(Person, 'Front-end dev'); position(Person, 'Intern')).

intern(Person) :- position(Person, 'Intern').

male_intern(Person) :- male(Person), position(Person, 'Intern').

female_intern(Person) :- female(Person), position(Person, 'Intern').

leader(Person) :- position(Person, 'Lead').

male_leader(Person) :- male(Person), position(Person, 'Lead').

female_leader(Person) :- female(Person), position(Person, 'Lead').

same_position(Person1, Person2) :- position(Person1, Z), position(Person2, Z), \== Person1, Person2.

both_chiefs(Person1, Person2) :- is_chief(Person1), is_chief(Person2), \== Person1, Person2.

male_chief(Person) :- male(Person), is_chief(Person).

female_chief(Person) :- female(Person), is_chief(Person).

rich_developer(Person) :- developer(Person), rich(Person).

rich_intern(Person) :- intern(Person), rich(Person).

%rich_manager(Person) :- rich(Person), (domain_has_manager(_, Person)).

rich_male_in_domain(Person, Domain) :- rich(Person), male_in_domain(Person, Domain).

rich_female_in_domain(Person, Domain) :- rich(Person), female_in_domain(Person, Domain).

rich_male(Person) :- rich(Person), male(Person).

rich_female(Person) :- rich(Person), female(Person).
