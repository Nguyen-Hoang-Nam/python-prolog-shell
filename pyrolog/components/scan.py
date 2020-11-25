import re
from colorama import Fore, Style 

# Check:
# _ Single line comment "%"
# _ Multiple lines comment "/*...*/"
COMMENT_REGEX = r"\/\*.*?\*\/|%[^\r\n]*$"

# Kind of token to split
# 1: Normal atom [A-Za-z0-9_]
# 2: Arguments with space \'[A-Za-z0-9_\-,]+\s.[A-Za-z0-9_\-, ]+\' 
# 3: Declaration :\-
# 4: Inequality \\==
# 5: Negation \\+
# 6: Other operator [()\.,;]
TOKEN_REGEX = r"\'[A-Za-z0-9_][A-Za-z0-9_\-\,\.\? ]*\'|[A-Za-z0-9_]+|:\-|\\==|==|\\\+|[()\.,;]"

class Scan:

  def __init__(self, rule):
    self.rule = rule 
    self.tokens = []

  def remove_comment(self):
    regex = re.compile(COMMENT_REGEX, re.MULTILINE | re.DOTALL)
    self.rule = regex.sub(r'', self.rule)

  def error(self):
    if self.tokens[0] == "\\==" or self.tokens[0] == "==" or self.tokens[0] == ":-":
      print(Fore.RED + "Error: Syntax error. \n" + Style.RESET_ALL)

  def infix_to_prefix(self):
    length = range(len(self.tokens))
    for i in length:
      # Swap first parameter and operator
      if self.tokens[i] == "\\==" or self.tokens[i] == "==":
        temp = self.tokens[i]
        self.tokens[i] = self.tokens[i - 1]
        self.tokens[i - 1] = temp

  def create_tokens(self):
    self.remove_comment()

    # Split rule to list of token
    # Example: love(romeo, juliet) -> ['love', '(', 'romeo', ',', 'juliet', ')', '.']
    iterator = re.finditer(TOKEN_REGEX, self.rule)
    self.tokens = [token.group() for token in iterator]

  def get_tokens(self):
    self.create_tokens()
    self.error()
    self.infix_to_prefix()

    return self.tokens
