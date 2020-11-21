import re

from components.interpreter import Conjunction, Variable, Term, TRUE, Rule

ATOM_NAME_REGEX = r"^[A-Za-z0-9_]+$|^\'[A-Za-z0-9_\-,]+\s.[A-Za-z0-9_\-, ]+\'$"
VARIABLE_REGEX = r"^[A-Z_][A-Za-z0-9_]*$"

class Parser(object):
  def __init__(self, tokens):
    self.tokens = tokens 
    self._scope = None

  def parse_query(self):
    self._scope = {}
    return self.parse_term()
  
  @property
  def current(self):
    return self.tokens[0]

  def pop_current(self):
    return self.tokens.pop(0)

  def parse_atom(self):
    name = self.pop_current()
    if re.match(ATOM_NAME_REGEX, name) is None:
      raise Exception("Invalid Atom Name: " + str(name))
    return name

  def parse_term(self):
    # Start list of arguments
    # Example: "(", "atom1", ",", "atom2", ")"
    if self.current == "(":
      self.pop_current()
      arguments = self.parse_arguments()
      return Conjunction(arguments)

    atom = self.parse_atom()

    # Check variable
    # Example: "Variable", ",", "atom 2"
    if re.match(VARIABLE_REGEX, atom) is not None:
      # Check anonymous variable _
      if atom == "_":
        return Variable("_")

      variable = self._scope.get(atom)

      if variable is None:
        self._scope[atom] = Variable(atom)
        variable = self._scope[atom]

      return variable

    # If atom is not functor
    # Example: "atom", ",", "atom 1"
    if self.current != "(":
      return Term(atom)

    # If atom is functor
    # Example: "functor", "(", "atom 1", ",", "atom 2"
    self.pop_current()
    arguments = self.parse_arguments() # Get atom 1, atom 2, etc
    return Term(atom, arguments)

  def parse_arguments(self):
    arguments = []

    # Keep get argument until close parenthesis
    while self.current != ")":
      # Sometime, arguments is a fact or rule
      # Therefore, we need to parse agrument as parse term
      arguments.append(self.parse_term())

      # Next to argument must be "," or ")"
      if self.current not in (",", ")"):
        raise Exception(
          "Expected , or ) in term"
        )

      # Remove "," then to next argument
      if self.current == ",":
        self.pop_current()

    # Remove ")"
    self.pop_current()
    return arguments


  def parse_rule(self):
    self._scope = {}
    head = self.parse_term()

    # Rule is fact
    # fact(atom1, atom2).
    if self.current == ".":
      self.pop_current()
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

      if self.current not in (",", "."):
        raise Exception(
          "Expected , or . in term"
        )
      
      # Remove ","
      if self.current == ",":
        self.pop_current()

    # Remove "."
    self.pop_current()

    tail = arguments[0] if arguments == 1 else Conjunction(arguments)
    return Rule(head, tail)

  