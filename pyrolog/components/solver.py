from components.parser import Parser
from collections import defaultdict
from components.interpreter import Variable
from components.helper import getch

from colorama import Fore, Style 

class Solver(object):
  def __init__(self, tokens, database):
    self.tokens = tokens 
    self.database = database

  def run(self):
    # Tokens to Term
    query = Parser(self.tokens).parse_query()
    query_variable = query.contain_variable()
    
    # List of matching queries
    matching_queries = [item for item in self.database.query(query)]

    if matching_queries:
      if query_variable:
        solutions_map = defaultdict(list)
        
        for matching_query in matching_queries:
          # Get matching varialbe from query
          matching_variables = query.match_variable_bindings(
            matching_query
          )

          # Add all result to solution map
          for variable_name, variable in query_variable.items():
            solutions_map[variable_name].append(
              matching_variables.get(variable)
            )
        
        # Get number of result
        for varialbe, value in solutions_map.items():
          value_len = len(value)
          break
        
        end_variable = False 
        value_number = 0
        while not end_variable and value_number < value_len:

          for varialbe, value in solutions_map.items():
            print(str(variable) + ": " + str(value[value_number]))

          query = getch()

          # Show more results or stop
          if(query != ";"):
            end_variable = True
          value_number += 1
          
        # No more results 
        if(value_number == value_len):
          print(Fore.RED + "false. \n" + Style.RESET_ALL)
        else:
          print(". \n")
      
      else: # No varialbe to print
        print("true. \n") if not query_variable else print(Fore.RED + "false. \n" + Style.RESET_ALL)
      
    else: # Not found matching query
      print(Fore.RED + "false. \n" + Style.RESET_ALL)