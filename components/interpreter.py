from functools import reduce

class Term(object):
  """All Prolog data structure are called Term
  
  Compound term consists of a functor followed by a sequence 
  of one or more arguments
  """

  def __init__(self, functor, arguments=None):
    # Check if compound term does not contain arguments
    # It is TRUE
    if not arguments:
      arguments = []

    self.functor = functor
    self.arguments = arguments

  def match_variable_bindings(self, other_term):
    
    if isinstance(other_term, Variable):
      return other_term.match_variable_bindings(self)

    if isinstance(other_term, Term):

      if self.functor != other_term.functor or len(self.arguments) != len(other_term.arguments):
        return None

      #[argument1, argument2], [argument3, argument4] 
      # -> [(argument1, argument3), (argument2, argument4)]
      zipped_argument_list = list(
        zip(self.arguments, other_term.arguments)
      )

      # Compare each argument of rule with exact argument of goal
      # [{Variable1: argument1}, {Variable2: argument2}] 
      matched_argument_var_binding = [
        arguments[0].match_variable_bindings(arguments[1])
        for arguments in zipped_argument_list
      ]

      # Convert list of dictinaries to dictionaries and check if exist conflict
      return reduce(
        Database.merge_bindings, [{}] + matched_argument_var_binding
      )

  def subtitute_variable_bindings(self, variable_bindings):
    return Term(
      self.functor,
      [
        argument.subtitute_variable_bindings(variable_bindings)
        for argument in self.arguments
      ]
    )

  def query(self, database):
    yield from database.query(self)

  # Return variable's name when print variable object
  def __str__(self):
    return (
      str(self.functor)
      if len(self.arguments) == 0
      else str(self.functor)
      + " ( "
      + ", ".join(str(argument) for argument in self.arguments)
      + " ) "
    )

  # Return self when debug variable object
  def __repr__(self):
    return str(self)

class TRUE(Term):
  def __init__(self, functor="True", arguments=None):
    if not arguments:
      arguments = []
    super().__init__(functor, arguments)

  def subtitute_variable_bindings(self, variable_bindings):
    return self 

  def query(self, database):
    yield self

class Variable(object):
  # A Variable is a type of Term. Variables start with an uppercase letter

  def __init__(self, name):
    self.name = name 

  def match_variable_bindings(self, other_term):
    bindings = {}

    if self != other_term:
      # __str__(self) -> self.name
      # -> bindings[self.name]
      bindings[self] = other_term

    return bindings

  def subtitute_variable_bindings(self, variable_bindings):
    # __str__(self) -> self.name
    # Get value of Variable
    bound_variable_value = variable_bindings.get(self)

    if bound_variable_value:
      return bound_variable_value.subtitute_variable_bindings(
        variable_bindings
      )

    return self 

  # Return variable's name when print variable object
  def __str__(self):
    return str(self.name)

  # Return self when debug variable object
  def __repr__(self):
    return str(self)

class Rule(object):
  # Store left and right side of Rules
  # Example: functor1(argument1, argument2) :- functor2(argument3, argument4)
  # -> head: Term(functor1, [argument1, argument2])
  # -> tail: Term(functor2, [argument3, arugment4])
  
  def __init__(self, head, tail):
    self.head = head 
    self.tail = tail 

  # Return variable's name when print variable object
  def __str__(self):
    return str(self.head) + ":- " + str(self.tail)

  # Return self when debug variable object
  def __repr__(self):
    return str(self)

class Unequal(Term):
  def __init__(self, arguments):
    # Super allows Conjunction to access methods of the Term class
    super().__init__("\\==", arguments)

  def subtitute_variable_bindings(self, variable_bindings):
    return Unequal(
      [
        self.arguments[0].subtitute_variable_bindings(variable_bindings),
        self.arguments[1].subtitute_variable_bindings(variable_bindings)
      ]
    )

  # Not can only have one argument
  def __str__(self):
    return "\== " + str(self.arguments[0]) + " " + str(self.arguments[1])

  def __repr__(self):
    return str(self)

class Negation(Term):
  def __init__(self, arguments):
    # Super allows Conjunction to access methods of the Term class
    super().__init__("~", arguments)

  def subtitute_variable_bindings(self, variable_bindings):
    return Negation(
      [
        self.arguments[0].subtitute_variable_bindings(variable_bindings)
      ]
    )

  # Not can only have one argument
  def __str__(self):
    return "~ " + str(self.arguments[0])

  def __repr__(self):
    return str(self)

class Disjunction(Term):
  # Logical disjunction is an or operation on two logical values
  # Inheritance of Term class
  # Example: argument1; argument2 -> or(argument1, argument2)

  def __init__(self, arguments):
    # Super allows Conjunction to access methods of the Term class
    super().__init__(";", arguments)
    self.check_true = False

  def query(self, database):

    # Go through each argument of Conjunction
    def find_solution(argument_index, variable_bindings):
      if argument_index >= len(self.arguments):
        yield self.subtitute_variable_bindings(variable_bindings)
      else:
        current_term = self.arguments[argument_index]
        empty = True

        for item in database.query(
          current_term.subtitute_variable_bindings(
            variable_bindings
          )
        ):
          empty = False
          self.check_true = True
          combined_variable_bindings = Database.merge_bindings(
            current_term.match_variable_bindings(item),
            variable_bindings,
          )

          if combined_variable_bindings is None:
            yield from find_solution(
              argument_index + 1, combined_variable_bindings
            )

        if (empty and argument_index + 1 < len(self.arguments)) or self.check_true:
          yield from find_solution(
            argument_index + 1, {}
          ) 
    yield from find_solution(0, {})

  def subtitute_variable_bindings(self, variable_bindings):
    return Disjunction(
      [
        argument.subtitute_variable_bindings(variable_bindings)
        for argument in self.arguments 
      ]
    )

  def __str__(self):
    return "; ".join(str(argument) for argument in self.arguments)

  def __repr__(self):
    return str(self)

class Conjunction(Term):
  # Logical conjunction is an And operation on two logical values
  # Inheritance of Term class
  # Example: argument1, argument2 -> and(argument1, argument2)

  def __init__(self, arguments):
    # Super allows Conjunction to access methods of the Term class
    super().__init__(",", arguments)

  def query(self, database):

    # Go through each argument of Conjunction
    def find_solution(argument_index, variable_bindings):
      if argument_index >= len(self.arguments):
        yield self.subtitute_variable_bindings(variable_bindings)
      else:
        current_term = self.arguments[argument_index]

        for item in database.query(
          current_term.subtitute_variable_bindings(
            variable_bindings
          )
        ):

          combined_variable_bindings = Database.merge_bindings(
            current_term.match_variable_bindings(item),
            variable_bindings,
          )

          if combined_variable_bindings is not None:

            yield from find_solution(
              argument_index + 1, combined_variable_bindings
            )
    yield from find_solution(0, {})

  def subtitute_variable_bindings(self, variable_bindings):
    return Conjunction(
      [
        argument.subtitute_variable_bindings(variable_bindings)
        for argument in self.arguments 
      ]
    )

  def __str__(self):
    return ", ".join(str(argument) for argument in self.arguments)

  def __repr__(self):
    return str(self)

class Database(object):
  def __init__(self, rules):
    self.rules = rules 

  def query(self, goal):

    if goal.functor == "," or goal.functor == ";":

      for matching_item in goal.query(self):
        matching_tail_var_bindings = goal.match_variable_bindings(matching_item)

        yield goal.subtitute_variable_bindings(
          matching_tail_var_bindings
        )
    elif goal.functor == "~":
      matching_query_terms = [item for item in self.query(goal.arguments[0])]
      
      if len(matching_query_terms) == 0:
        yield goal.subtitute_variable_bindings({})
    
    elif goal.functor == "\\==":
      if goal.arguments[0].functor != goal.arguments[1].functor:
        yield goal.subtitute_variable_bindings({})

    else:
      for index, rule in enumerate(self.rules):
        # Compare all head of rule with goal
        matching_head_var_bindings = rule.head.match_variable_bindings(goal)

        # Find matching rule
        if matching_head_var_bindings is not None:
          matched_head_item = rule.head.subtitute_variable_bindings(matching_head_var_bindings)
          matched_tail_item = rule.tail.subtitute_variable_bindings(matching_head_var_bindings)

          for matching_item in matched_tail_item.query(self):
            matching_tail_var_bindings = matched_tail_item.match_variable_bindings(matching_item)

            yield matched_head_item.subtitute_variable_bindings(
              matching_tail_var_bindings
            )

  @staticmethod
  def merge_bindings(first_bindings_map, second_bindings_map):
    if first_bindings_map is None or second_bindings_map is None:
      return None 

    merged_bindings = {}

    # first_bindings_map: [{Variable1: argument1}, etc] 
    # Append list of dictinaries
    for variable, value in first_bindings_map.items():
      merged_bindings[variable] = value 

    for variable, value in second_bindings_map.items():
      # Check if Variable already in 
      if variable in merged_bindings:
        # Get other value of same Variable 
        existing_variable_binding = merged_bindings[variable]

        # Compare other value and value
        shared_binding = existing_variable_binding.match_variable_bindings(value)

        if shared_binding is not None:
          for variable_, value_ in shared_binding.items():
            merged_bindings[variable_] = value_ 

        else:
          return None 

      else:
        merged_bindings[variable] = value 

    return merged_bindings

  # Return variable's name when print variable object
  def __str__(self):
    return ".\n".join(str(rule) for rule in self.rules)

  # Return self when debug variable object
  def __repr__(self):
    return str(self)



