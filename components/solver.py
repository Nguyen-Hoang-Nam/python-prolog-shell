from components.parser import Parser
from collections import defaultdict
from components.interpreter import Variable
from components.helper import getch

from colorama import Fore, Style 
from sys import stdout

class Solver(object):
  def __init__(self, tokens, database):
    self.tokens = tokens 
    self.database = database

  def run(self):
    # Query much be Term or Conjunction
    query = Parser(self.tokens).parse_query()

    query_variable_map = {}

    # Check if variable in query
    variable_in_query = False

    for argument in query.arguments:
      
      # Check if argument is Variable
      if isinstance(argument, Variable):
        variable_in_query = True

        # Store Variable in query_variable_map
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
        
        for varialbe, value in solutions_map.items():
          value_len = len(value)
          break
        
        end_variable = False 
        value_number = 0
        while not end_variable and value_number < value_len:
          for varialbe, value in solutions_map.items():
            print(str(variable) + ": " + str(value[value_number]))

          query = getch()
          print(";")

          if(query != ";"):
            end_variable = True
          value_number += 1
          
        if(value_number == value_len):
          print(Fore.RED + "false. \n" + Style.RESET_ALL)
        else:
          print(". \n")
      
      else:
        print("true. \n") if not variable_in_query else print(Fore.RED + "false. \n" + Style.RESET_ALL)
      
    else:
      print(Fore.RED + "false. \n" + Style.RESET_ALL)