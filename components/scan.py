import re

TOKEN_REGEX = r"[A-Za-z0-9_]+|\'[A-Za-z0-9_\-,]+\s.[A-Za-z0-9_\-, ]+\'|:\-|[()\.,]"

class Scan:

  def __init__(self, rule):
    self.rule = rule 

  def tokens(self):
    # Split rule to list of token
    # Example: love(romeo, juliet) -> ['love', '(', 'romeo', ',', 'juliet', ')', '.']
    
    iterator = re.finditer(TOKEN_REGEX, self.rule)
    return [token.group() for token in iterator]