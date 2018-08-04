def distance(a, b):
   "Calculates the Levenshtein distance between a and b."
   n, m = len(a), len(b)
   if n > m:
      # Make sure n <= m, to use O(min(n,m)) space
      a, b = b, a
      n, m = m, n

   current_column = range(n+1) # Keep current and previous column, not entire matrix
   for i in range(1, m+1):
      previous_column, current_column = current_column, [i]+[0]*n
      for j in range(1,n+1):
         add, delete, change = previous_column[j]+1, current_column[j-1]+1, previous_column[j-1]
         if a[j-1] != b[i-1]:
            change += 1
         current_column[j] = min(add, delete, change)

   return current_column[n]

def distance_2(text, pattern):
   "Calculates the Levenshtein distance between text and pattern."
   text_len, pattern_len = len(text), len(pattern)

   current_column = range(pattern_len+1)
   min_value = pattern_len
   end_pos = 0
   for i in range(1, text_len+1):
      previous_column, current_column = current_column, [0]*(pattern_len+1) # !!!
      for j in range(1,pattern_len+1):
         add, delete, change = previous_column[j]+1, current_column[j-1]+1, previous_column[j-1]
         if pattern[j-1] != text[i-1]:
            change += 1
         current_column[j] = min(add, delete, change)

      if min_value > current_column[pattern_len]: # !!!
         min_value = current_column[pattern_len]
         end_pos = i

   return min_value, end_pos

def distance_3(text, pattern):
   min_value, end_pos = distance_2(text, pattern)
   min_value, start_pos = distance_2(text[end_pos-1::-1], pattern[::-1])
   start_pos = end_pos - start_pos
   return min_value, start_pos, end_pos, text[start_pos:end_pos], pattern
