import requests
from bs4 import BeautifulSoup

def longestSubstringFinder(string1, string2):
    answer = ""
    len1, len2 = len(string1), len(string2)
    for i in range(len1):
        for j in range(len2):
            lcs_temp=0
            match=''
            while ((i+lcs_temp < len1) and (j+lcs_temp<len2) and string1[i+lcs_temp] == string2[j+lcs_temp]):
                match += string2[j+lcs_temp]
                lcs_temp+=1
            if (len(match) > len(answer)):
                answer = match
    return answer

def longestCommonSubsequence(X,Y):
  return lcsubsequence(X,Y,len(X),len(Y))

def lcsubsequence(X, Y, m, n):
    L = [[0 for x in range(n+1)] for x in range(m+1)]
  
    # Following steps build L[m+1][n+1] in bottom up fashion. Note
    # that L[i][j] contains length of LCS of X[0..i-1] and Y[0..j-1] 
    for i in range(m+1):
        for j in range(n+1):
            if i == 0 or j == 0:
                L[i][j] = 0
            elif X[i-1] == Y[j-1]:
                L[i][j] = L[i-1][j-1] + 1
            else:
                L[i][j] = max(L[i-1][j], L[i][j-1])
  
    # Following code is used to print LCS
    index = L[m][n]
  
    # Create a character array to store the lcs string
    lcs = [""] * (index+1)
    lcs[index] = ""
  
    # Start from the right-most-bottom-most corner and
    # one by one store characters in lcs[]
    i = m
    j = n
    while i > 0 and j > 0:
  
        # If current character in X[] and Y are same, then
        # current character is part of LCS
        if X[i-1] == Y[j-1]:
            lcs[index-1] = X[i-1]
            i-=1
            j-=1
            index-=1
  
        # If not same, then find the larger of two and
        # go in the direction of larger value
        elif L[i-1][j] > L[i][j-1]:
            i-=1
        else:
            j-=1
  
    return "".join(lcs)

def getWordAndDefinition(text):
  text = text.strip()
  parenIndex = text.find("(")
  word = text[:parenIndex].strip()
  definition = text[parenIndex+1:].replace(")", "").strip()

  if parenIndex == -1: #turn it into an acronym
    word = "".join( [word[0].upper() for word in text.split()] )
    definition = text
  
  return {"word": word, "definition": definition}

def defineGoonAcronym(acronym):
  '''
  get acronym that's most similar
  similarity is defined as the longest common subsequence
  '''

  #get list of all current words in the goontionary:
  url = "https://docs.google.com/document/d/e/2PACX-1vRQpuBXtQUGrGXcMzIhpZRuNCfNyj-pNv39u8KLCg1uR3yIe9oT6ZEVF0e4jnkrHl-UC0ujPFqNXf_p/pub"
  soup = BeautifulSoup(requests.get(url).content, "lxml")
  wordsAndDefinitions = []
  for string in soup.find("div", attrs={"id":"contents"}).div.children:
    wordsAndDefinitions.append( getWordAndDefinition( string.text ) )

  #I try to find the max sum of the longest common subsequence and substring (this favors consecutive letters)
  similarityScore = 0
  lcsList = []
  #for each word, check the longest common subsequence
  for wad in wordsAndDefinitions:
    lcs = longestCommonSubsequence(acronym.upper(), wad["word"].upper())
    lcs2 = longestSubstringFinder(acronym.upper(), wad["word"].upper())
    if lcs is None or lcs2 is None:
      continue
    elif len(lcs) + len(lcs2) > similarityScore:
      similarityScore = len(lcs) + len(lcs2)
      lcsList = [{"goon word": wad["word"], "goon definition": wad["definition"], "lcs": lcs}]
    elif len(lcs) + len(lcs2) ==  similarityScore:
      lcsList.append({"goon word": wad["word"], "goon definition": wad["definition"], "lcs": lcs})

  return lcsList