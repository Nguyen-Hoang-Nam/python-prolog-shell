import re

from components.interpreter import Conjunction, Variable, Term, TRUE, Rule, Disjunction, Negation, Unequal, Equal

# Check normal name or name with space
ATOM_NAME_REGEX = r"^[A-Za-z0-9_]+$|^\'[A-Za-z0-9_][A-Za-z0-9_\-\,.]+\s*[A-Za-z0-9_\-,. ]*\'$"
VARIABLE_REGEX = r"^[A-Z_][A-Za-z0-9_]*$"

class Parser(object):
  def __init__(self, tokens):
    # Store tokens as list 
    # Example: ["functor", "(", "argument1", ",", "argument2", ")"]
    self.tokens = tokens 

    # Store Variable in each query
    self._scope = None
    self.is_disjunction = False

  # Call when use input new query
  def parse_query(self):

    # Create new empty scope to store new Variable
    # Because Variable is local in each scope
    self._scope = {}
    return self.parse_term()
  
  @property
  # Get current token
  def current(self):
    return self.tokens[0]

  # Remove current token
  def pop_current(self):
    return self.tokens.pop(0)

  # Get atom such as functor, argument
  def parse_atom(self):
    name = self.pop_current()

    # Check if current is atom
    # This avoid functor(argument, , argument)
    if re.match(ATOM_NAME_REGEX, name) is None:
      raise Exception("Invalid Atom Name: " + str(name))
    return name

  # Get full Term
  # Return:
  # 1: Conjunction([argument1, argument2, etc])
  # 2: Variable(name)
  # 3: Term(name)
  # 4: Fact -> Term(functor, [argument1, argument2, etc])
  def parse_term(self):

    if self.current == "\\==":
      self.pop_current()

      arguments = []
      arguments.append(self.parse_term())
      self.pop_current()
      arguments.append(self.parse_term())
      return Unequal(arguments)

    if self.current == "==":
      self.pop_current()

      arguments = []
      arguments.append(self.parse_term())
      self.pop_current()
      arguments.append(self.parse_term())
      return Equal(arguments)

    if self.current == "\\+":
      self.pop_current() # Remove "\+"

      arguments = []
      arguments.append(self.parse_term())
      return Negation(arguments)

    # Clause without functor
    # Example: (true, false)
    if self.current == "(":
      self.pop_current() # Remove "("
      arguments = self.parse_arguments() # Start get arguments

      if self.is_disjunction:
        self.is_disjunction = False
        return Disjunction(arguments) # (argument1; argument2)
      else:
        return Conjunction(arguments) # (argument1, argument2, argument3, etc)

    # Get atom
    atom = self.parse_atom()

    # Check variable
    # Example: functor(Variable, argument)
    if re.match(VARIABLE_REGEX, atom) is not None:
      # Check anonymous variable _
      if atom == "_":
        return Variable("_")

      # Get Variable in scope if exist
      variable = self._scope.get(atom)

      # Variable did not assign before
      if variable is None:
        # Add variable to scope
        self._scope[atom] = Variable(atom)
        variable = self._scope[atom]

      return variable

    # If atom is not functor
    # Example: functor(argument1, argument2, etc)
    if self.current != "(":
      return Term(atom)

    # If atom is functor
    # Example: functor(subfunctor(arugment1, argument2), argument3, etc)
    self.pop_current() # Remove "(" after subfunctor
    arguments = self.parse_arguments() # Get all arguments in subfunctor 
    return Term(atom, arguments)

  # Get consecutive arguments
  def parse_arguments(self):
    arguments = []
    is_disjunction = False

    # Keep get argument until close parenthesis
    while self.current != ")":
      # Sometime, arguments is a fact or rule
      # Therefore, we need to parse agrument as term for general case
      arguments.append(self.parse_term())

      # Next to argument must be "," or ")" or ";"
      if self.current not in (",", ")", ";"):
        raise Exception(
          "Expected , or ) or ; in term"
        )

      if self.current == ",":
        # Remove "," then to next argument
        self.pop_current()
      elif self.current == ";":
        is_disjunction = True 
        # Remove ";" then to next argument
        self.pop_current()

    if is_disjunction:
      self.is_disjunction = True 

    # Remove ")"
    self.pop_current()
    return arguments

  # Parse rule and fact from database file
  # Return:
  # 1 Fact: functor(argument1, argument2, etc) 
  # -> head = Term(functor, [argument1, argument2, etc])
  # -> Rule(head, true)
  # 2 Rule: functor1(argument1, argument2) :- functor2(argument3, argument4) 
  # -> head = Term(functor1, [argument1, argument2])
  # -> tail = Term(functor2, [argument3, argument4])
  # -> Rule(head, tail)
  def parse_rule(self):
    is_disjunction = False
    # Create new empty scope to store new Variable
    # Because Variable is local in each scope
    self._scope = {}
    head = self.parse_term()

    # Rule is fact
    # fact(atom1, atom2).
    if self.current == ".":
      self.pop_current() # Remove "."
      # head :- TRUE
      return Rule(head, TRUE())

    # Rule must has :- if Rule is not fact
    # fact1(atom1, atom2) :- fact2(atom3, atom4)
    if self.current != ":-":
      raise Exception(
        "Expected :- in rule"
      )

    # Remove :- 
    self.pop_current()

    arguments = []

    while self.current != ".":
      arguments.append(self.parse_term())

      # Next to argument must be "," or ")"
      if self.current not in (",", ".", ";"):
        raise Exception(
          "Expected , or . or ; in term"
        )
      
      # Remove ","
      if self.current == ",":
        self.pop_current()
      elif self.current == ";":
        is_disjunction = True 
        self.pop_current()

    if is_disjunction:
      self.is_disjunction = True 

    # Remove "."
    self.pop_current()

    # If we only have one argument then Arguments[0] must be Term(functor2, [argument3, argument4])
    # Otherwise, It is Conjunction(Term, Term)
    # Example functor1(argument1, argument2) :- functor2(argument3, argument4), functor3(argument5, argument6)
    tail = arguments[0] if len(arguments) == 1 else Conjunction(arguments)
    return Rule(head, tail)

  