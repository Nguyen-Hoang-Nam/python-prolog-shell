from components.parser import Parser
from collections import defaultdict
from components.interpreter import Variable

class Solver(object):
  def __init__(self, tokens, database):
    self.tokens = tokens 
    self.database = database

  def run(self):
    query = Parser(self.tokens).parse_query()

    query_variable_map = {}
    variable_in_query = False

    for argument in query.arguments:
      if isinstance(argument, Variable):
        variable_in_query = True
        query_variable_map[argument.name] = argument

    matching_query_terms = [item for item in self.database.query(query)]

    if matching_query_terms:
      if query_variable_map:

        solutions_map = defaultdict(list)
        for matching_query_term in matching_query_terms:
          matching_variable_bindings = query.match_variable_bindings(
            matching_query_term 
          )

          for variable_name, variable in query_variable_map.items():
            solutions_map[variable_name].append(
              matching_variable_bindings.get(variable)
            )
        
        return solutions_map
      
      else:
        return True if not variable_in_query else None 
      
    else:
      return False if not variable_in_query else None