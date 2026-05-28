"""Levenshtein distance between 2 strings.
    Source: http://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python, first version
"""
def levenshtein1(s1, s2,m):
 # returns levenshtein distance, but returns m if
 # the distance would be greater than or equal to m.
 # this is done for efficiency in tests such as
 # if levenshtein1(s1, s2,m) < m:
 if len(s1) < len(s2):
  return levenshtein1(s2, s1,m)
 
 # len(s1) >= len(s2)
 if len(s2) == 0:
  return len(s1)
 if (len(s2) - len(s1))>= m: # first optimization
  return m
 previous_row = xrange(len(s2) + 1)
 for i, c1 in enumerate(s1):
  current_row = [i + 1]
  for j, c2 in enumerate(s2):
   insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
   deletions = current_row[j] + 1    # than s2
   substitutions = previous_row[j] + (c1 != c2)
   current_row.append(min(insertions, deletions, substitutions))
  previous_row = current_row
  # experience shows the following is not an optimization, but changes
  # the result.  It must be that the last value in previous_row can 
  # decrease as well as increase!  (This needs further examination)
  #if previous_row[-1] >= m: # second optimization
  # return m
 
 return previous_row[-1]

def levenshtein(s1, s2):
 if len(s1) < len(s2):
  return levenshtein(s2, s1)
 
 # len(s1) >= len(s2)
 if len(s2) == 0:
  return len(s1)
 
 previous_row = xrange(len(s2) + 1)
 for i, c1 in enumerate(s1):
  current_row = [i + 1]
  for j, c2 in enumerate(s2):
   insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
   deletions = current_row[j] + 1    # than s2
   substitutions = previous_row[j] + (c1 != c2)
   current_row.append(min(insertions, deletions, substitutions))
  previous_row = current_row
 
 return previous_row[-1]
