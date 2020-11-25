#!/usr/bin/python3

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
    print("Welcome to Python Prolog shell (version 1.3.0).")
    print("This is free and open source software \n")
    print("For more information, visit")
    print("https://github.com/Nguyen-Hoang-Nam/python-prolog-shell \n")

    database = None
    command_number = 1 # Count command
    history = []

    while True:
      query = input(str(command_number) + " ?- ")

      line_history = len(history)

      # Query must end with period
      if query[-1] != '.': 
        end_query = False 

        while not end_query:
          next_query = input()

          if next_query == '.':
            end_query = True 

          query += next_query

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
        
      elif query == "halt.": # Exit shell
        break

      elif query == "history.":
        for i in range(len(history)):
          print(history[i])
          
        print("\n")

      elif re.match(DATABASE, query): # Add database [database_file_name].
        file_name = query[1: len(query) - 2] # database_file_name

        try: # Check if database file exist
          # Read entire file and close when done
          with open(file_name + '.pl', 'r') as database_file:
            database_content = database_file.read()
        except: # Database file not exist or can not open
          print(Fore.RED + "ERROR: source '" + file_name + ".pl' does not exist")
          print(Style.RESET_ALL)

        scan = Scan(database_content)
        tokens = scan.get_tokens()
            
        rules = Parser(tokens).parse_rules() # Store rule for database
        database = Database(rules)
        
        # Exist file then print True
        print("true.\n") 
        
      else: # Normal query
        scan = Scan(query)
        tokens = scan.get_tokens()

        if tokens[0] == 'writeln':
          if tokens[2][0] == "'" and tokens[2][-1] == "'":
            print(tokens[2][1: len(tokens[2]) - 1])
          else:
            print(tokens[2])
          print("true.\n") 

        else:
          if database is None: # If user does not add database yet
            print("Unknow procedure \n")
            print("Rules must be loaded from a file")
          else : # Try to run query
            solver = Solver(tokens, database)
            solver.run()

      history.append(query)
      command_number += 1

