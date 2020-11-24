#!/usr/bin/env python

import re

from components.interpreter import Database
from components.scan import Scan
from components.parser import Parser
from components.solver import Solver 
from components.helper import getch
from sys import platform

from colorama import Fore, Style 

DATABASE = r"^\[[A-Za-z0-9_]+\]\."

class Shell():
  def main(self):
    print("Welcome to Python Prolog shell (version 1.3.0). This is free and open source software \n")
    print("For more information, visit https://github.com/Nguyen-Hoang-Nam/python-prolog-shell")

    database = None
    command_number = 1 # Count command
    history = []

    while True:
      query = input(str(command_number) + " ?- ")

      line_history = len(history)

      if query == "up.":
        print("\n")

        if line_history > 0:
          line_history -= 1
          query = history[line_history]
          command_number += 1
          print(str(command_number) + " ?- " + query)

      elif query == "down.":
        print("\n")

        if line_history < len(history):
          line_history += 1
          query = history[line_history]
          command_number += 1
          print(str(command_number) + " ?- " + query)
        

      if query[-1] != '.': # Query must end with period
        print("Unexpected end of file.")
        print("false.\n")

      else:
        if query == "halt.": # Exit shell
          break
        elif re.match(DATABASE, query): # Add database [database_file_name].
          file_name = query[1: len(query) - 2] # database_file_name

          try: # Check if database file exist
            database_file = open(file_name + ".pl", "r")
          except: # Database file not exist or can not open
            print(Fore.RED + "ERROR: source '" + file_name + ".pl' does not exist")
            print(Style.RESET_ALL)

          database_line = 0 # Useful when show exact error line in db file
          rules = [] # Store rule for database

          for expression in database_file:
            database_line += 1

            # Check express is not an empty line and not comment
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
          print("true.\n") 
          
        else: # Normal query
          
          if database is None: # If user does not add database yet
            print("Unknow procedure \n")
            print("Rules must be loaded from a file")
          else : # Try to run query
            scan = Scan(query)
            tokens = scan.tokens()

            solver = Solver(tokens, database)
            solver.run()

      history.append(query)
      command_number += 1
        
# Run shell after start program
if __name__ == '__main__':
  Shell().main()

