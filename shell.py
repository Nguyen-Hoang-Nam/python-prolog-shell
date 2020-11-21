import re

from components.interpreter import Database
from components.scan import Scan
from components.parser import Parser
from components.solver import Solver 

from colorama import Fore, Back, Style 

DATABASE = r"^\[[A-Za-z0-9]+\]\."

class Shell():
  def main(self):
    database = None
    command_number = 1
    while True:
      query = input(str(command_number) + " ?- ")

      if query[-1] != '.':
        print("false\n")
      else:
        if query == "halt.":
          break
        elif re.match(DATABASE, query):
          file_name = query[1: len(query) - 2]

          try:
            database_file = open(file_name + ".pl", "r")
            database_line = 0
            rules = []

            for expression in database_file:
              database_line += 1

              # Check express is not an empty line
              if expression != "\n" and expression[0] != '%':

                # Split expression into tokens
                scan = Scan(expression)
                tokens = scan.tokens()

                # Valid expression must end with a period
                if tokens[len(tokens) - 1] != ".":
                  print("Line " + str(database_line) + ": " + expression)
                  print("Unexpected end of file.")
                  break
                
                rule = Parser(tokens).parse_rule()
                rules.append(rule)
            
            database = Database(rules)
            
            # Exist file then print True
            print("true\n")
          except:
            print(Fore.RED + "ERROR: source '" + file_name + ".pl' does not exist")
            print(Style.RESET_ALL) 
          
        else:
          if database is None:
            print("Unknow procedure \n")
            print("Rules must be loaded from a file")
          else :
            scan = Scan(query)
            tokens = scan.tokens()

            solver = Solver(tokens, database)
            solution = solver.run()
            print(str(solution) + "\n")

      command_number += 1
        

if __name__ == '__main__':
  Shell().main()

