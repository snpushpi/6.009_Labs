"""6.009 Lab 6 -- Autocomplete"""

# NO ADDITIONAL IMPORTS!
from text_tokenize import tokenize_sentences


class Trie:
    def __init__(self):
        """
        Initialize an empty trie.
        """
        self.value = None
        self.children = {}
        self.type = None

    def __getitem__(self, key):
        """
        Return the value for the specified prefix.  If the given key is not in
        the trie, raise a KeyError.  If the given key is of the wrong type,
        raise a TypeError.
        """
        if type(key)!=self.type:
            raise TypeError
        else:
            current_trie = self.children
            if type(key)!=tuple:
                if key=='':
                    if self.value!=None:
                        return self.value
                    else:
                        raise KeyError
                else:
                    for i in range(len(key)):
                        if key[i] in current_trie:
                            if i!=len(key)-1:
                                current_trie = current_trie[key[i]].children
                        else:
                            raise KeyError 
                    else:
                        if current_trie[key[i]].value == None:
                            raise KeyError
                        else:
                            return current_trie[key[i]].value
            else:
                if key==():
                    if key not in current_trie:
                        raise KeyError
                    else:
                        return self.value
                else:
                    
                    for i in range(len(key)):
                        if (key[i],) in current_trie:
                            if i!=len(key)-1:
                                current_trie = current_trie[(key[i],)].children
                        else:
                            raise KeyError 
                    else:
                        if current_trie[(key[i],)].value == None:
                            raise KeyError
                        else:
                            return current_trie[(key[i],)].value

    def __setitem__(self, key, value):
        """
        Add a key with the given value to the trie, or reassign the associated
        value if it is already present in the trie.  Assume that key is an
        immutable ordered sequence.  Raise a TypeError if the given key is of
        the wrong type.
        """
       
        current_trie = self.children
        if self.type== None:
            self.type = type(key)
        else:
            if self.type!=type(key):
                raise TypeError
        if self.type!= tuple:
            for i in range(len(key)):
                if key[i] in current_trie:
                    if i!=len(key)-1:
                        current_trie=current_trie[key[i]].children
                    else:
                        current_trie[key[i]].value = value

                else:
                    current_trie[key[i]]= Trie()
                    current_trie[key[i]].type = self.type
                    if i!=len(key)-1:
                        current_trie[key[i]].children={}
                        current_trie[key[i]].value=None
                        current_trie=current_trie[key[i]].children
                    else:
                        current_trie[key[i]].children={}
                        current_trie[key[i]].value=value
        else:
            for i in range(len(key)):
                if (key[i],) in current_trie:
                    if i!=len(key)-1:
                        current_trie=current_trie[(key[i],)].children
                    else:
                        current_trie[(key[i],)].value = value

                else:
                    current_trie[(key[i],)]= Trie()
                    current_trie[(key[i],)].type = self.type
                    if i!=len(key)-1:
                        current_trie[(key[i],)].children={}
                        current_trie[(key[i],)].value=None
                        current_trie=current_trie[(key[i],)].children
                    else:
                        current_trie[(key[i],)].children={}
                        current_trie[(key[i],)].value=value
    def __delitem__(self, key):
        """
        Delete the given key from the trie if it exists.
        """
        current_trie = self.children
        if self.type!= tuple:
            for i in range(len(key)):
                if key[i] in current_trie:
                    if i!=len(key)-1:
                        current_trie=current_trie[key[i]].children
                    else:
                        current_trie[key[i]].value = None

                else:
                    raise KeyError
        else:
            for i in range(len(key)):
                if (key[i],) in current_trie:
                    if i!=len(key)-1:
                        current_trie=current_trie[(key[i],)].children
                    else:
                        current_trie[(key[i],)].value = None

                else:
                    raise KeyError


        
    def __contains__(self, key):
        """
        Return True if key is in the trie and has a value, return False otherwise.
        """
        current_trie = self.children
        if self.type!= tuple:
            for i in range(len(key)):
                if key[i] in current_trie:
                    if i!=len(key)-1:
                        current_trie=current_trie[key[i]].children
                    else:
                        if current_trie[key[i]].value == None:
                            return False
                        else:
                            return True

                else:
                    return False
        else:
            for i in range(len(key)):
                if (key[i],) in current_trie:
                    if i!=len(key)-1:
                        current_trie=current_trie[(key[i],)].children
                    else:
                        if current_trie[(key[i],)].value == None:
                            return False
                        else:
                            return True

                else:
                    return False
    def my_generator(self,word):
 
                
            if self.value!= None:
                yield (word, self.value)
            
            for child in self.children:
            
        
                yield from self.children[child].my_generator(word + child)

    def __iter__(self):
        """
`        Generator of (key, value) pairs for all keys/values in this trie and
        its children.  Must be a generator or iterator!
        """
    
        yield from self.my_generator(word='' if self.type!= tuple else ())
def make_word_trie(text):
    """
    Given a piece of text as a single string, return a Trie whose keys are the
    words in the text, and whose values are the number of times the associated
    word appears in the text
    """
    t= Trie()
    my_list = tokenize_sentences(text)
    for line in my_list:
        for word in line.split():
            if word in t:
                t[word]+=1
            else:
                t[word]=1
    return t
def make_phrase_trie(text):
    """
    Given a piece of text as a single string, return a Trie whose keys are the
    sentences in the text (as tuples of individual words) and whose values are
    the number of times the associated sentence appears in the text.
    """
    t = Trie()
    my_list = tokenize_sentences(text)
    for line in my_list:
        if tuple(line.split()) in t:
            t[tuple(line.split())]+=1
        else:
            t[tuple(line.split())]=1
    return t
##    my_list = list(t)
##    new_list = []
##    for elt in my_list:
##        new_list.append((elt[1],elt[0]))
##    new_list.sort(reverse = True)
##    result_list = []
##    i = 0
##    for elt in new_list:
##        i=i+1
##        result_list.append(elt)
##        if i ==4:
##            break
##
##    return result_list
def autocomplete(trie, prefix, max_count=None):
    """
    Return the list of the most-frequently occurring elements that start with
    the given prefix.  Include only the top max_count elements if max_count is
    specified, otherwise return all.

    Raise a TypeError if the given prefix is of an inappropriate type for the
    trie.
    """
    my_type = trie.type
    if my_type!=type(prefix):
        raise TypeError
    if max_count==0:
        return []
    else:
        if len(prefix)==0:
            my_list=list(trie)
        else:
            
            my_children= trie.children
            if type(prefix)!=tuple:#do something if that's a string 
                for i in range(len(prefix)):#start traversing through our trie
                    if prefix[i] not in my_children:
                        return []
                    else:
                        if i!=len(prefix)-1:
                            my_children=my_children[prefix[i]].children
                        else:
                            my_children = my_children[prefix[i]]
            else:
                for i in range(len(prefix)):
                    if (prefix[i],) not in my_children:
                        return []
                    else:
                        if i!=len(prefix)-1:
                            my_children = my_children[(prefix[i],)].children
                        else:
                            my_children = my_children[(prefix[i],)]              
            
            my_list = list(my_children)
        
        final_list = []
        i=0
        for elt in my_list:
            if prefix+elt[0] in trie:
                final_list.append((trie[prefix+elt[0]],prefix+elt[0]))
        final_list.sort(reverse= True)
        
        result_list=[]
        i=0
        if max_count==None or max_count>len(my_list):
            for elt in final_list:
                result_list.append(elt[1])
        else:
            for elt in final_list:
                result_list.append(elt[1])
                i = i+1
                if i>=max_count:
                    break
        return result_list
    
    
def autocorrect(trie, prefix, max_count=None):
    """
    Return the list of the most-frequent words that start with prefix or that
    are valid words that differ from prefix by a small edit.  Include up to
    max_count elements from the autocompletion.  If autocompletion produces
    fewer than max_count elements, include the most-frequently-occurring valid
    edits of the given word as well, up to max_count total elements.

    Do not use a brute-force method that involves generating/looping over
    all the words in the trie.
    """
    print(max_count)
    check_list = autocomplete(trie,prefix,max_count)
    check_set=set(check_list)
    
    new_set = set()
    if len(check_list)==max_count:
        print(check_list)
        return check_list
    elif max_count!= None and len(check_list)>max_count:
        print(check_list[:max_count])
        return check_list[:max_count]
    else:#we have to do some edits to make our suggested list, we are making insertions here
        result_list=[]
        result_list.extend(check_list)
        for i in range(len(prefix)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                print(prefix[:i]+c+prefix[i:])
                if prefix[:i]+c+prefix[i:] in trie and prefix[:i]+c+prefix[i:] not in check_set:
                    new_set.add((trie[prefix[:i]+c+prefix[i:]],prefix[:i]+c+prefix[i:]))
        for i in range(len(prefix)):#making deletions here
            if prefix[:i]+prefix[i+1:] in trie and prefix[:i]+prefix[i+1:] not in check_set :
                new_set.add((trie[prefix[:i]+prefix[i+1:]],prefix[:i]+prefix [i+1:]))
        for i in range(len(prefix)):#making replacements here
            for c in 'abcdefghijklmnopqrstuvwxyz':
                if prefix[:i]+c+prefix[i+1:] in trie and prefix[:i]+c+prefix[i+1:] not in check_set:
                    new_set.add((trie[prefix[:i]+c+prefix[i+1:]],prefix[:i]+c+prefix[i+1:]))
        for i in range(1,len(prefix)):#making swaping  here
            if prefix[:i-1]+prefix[i]+prefix[i-1]+prefix[i+1:] in trie and prefix[:i-1]+prefix[i]+prefix[i-1]+prefix[i+1:] not in check_set : 
                #new_list.append((trie[prefix[:i-1]+prefix[i]+prefix[i-1]+prefix[i+1:]],prefix[:i-1]+prefix[i]+prefix[i-1]+prefix[i+1:]))
                new_set.add((trie[prefix[:i-1]+prefix[i]+prefix[i-1]+prefix[i+1:]],prefix[:i-1]+prefix[i]+prefix[i-1]+prefix[i+1:]))
    new_list=list(new_set)
    new_list.sort(reverse = True)
    i=0
    length= len(new_list)+len(check_list)
    if max_count==None or max_count> length :
        for elt in new_list:
            result_list.append(elt[1])
        return result_list
    else:
        for elt in new_list:
            i=i+1
            result_list.append(elt[1])
            if i >=max_count-len(check_list):
                print(result_list)
                return result_list
        
def helper_cutter(pattern):
    pattern2 = ''
    for i in range(len(pattern)):
        if pattern[i]!='*':
            pattern2 = pattern2 + pattern[i]
        else:
            if len(pattern2)!=0:
                if pattern2[-1]=='*':
                    continue
                else:
                    pattern2 = pattern2 + pattern[i]
            else:
                pattern2 = pattern2 + pattern[i]
    return pattern2            
def helper_checker_2(pattern):#returns deducting all asterisks if there is no letter in pattern
    pattern2=''
    for c in pattern:
        if c!='*':
            pattern2 = pattern2 + c
    return len(pattern2)
    
def word_filter(trie, pattern,my_string = ''):
    """
    Return list of (word, freq) for all words in trie that match pattern.
    pattern is a string, interpreted as explained below:
         * matches any sequence of zero or more characters,
         ? matches any single character,
         otherwise char in pattern char must equal char in word.

    Do not use a brute-force method that involves generating/looping over
    all the words in the trie.
    """
    #we will first check its first character, if it's a question mark, we will just apply recursion on all of its child node and apply recursion on each of them.
    #if the first letter is an asterisk, we will create add the elements of all of its child and then apply reursion there.
    #if we face a letter we simply go its child
    pattern = helper_cutter(pattern)
    my_list = []
    if pattern == '*':
        if  my_string in trie:
            return [(my_string,trie[my_string])]+[(my_string+elt[0],elt[1]) for elt in list(trie)]
        else:
            return [(my_string+elt[0],elt[1]) for elt in list(trie)]
        return list(set(my_list))
    flag = False
    special_string= False
    j = None
    for i in range(len(pattern)):
        j = i
        if pattern[i] not in ['*','?']:
            break
        else:
            if pattern[i]=='*':
                flag = True

    if j == len(pattern)-1:
        if flag == True:
            special_string = True
    if special_string == True:
        special_length= helper_checker_2(pattern)
        for e in list(trie):
            if len(e[0])>=special_length:
                if (my_string+e[0],e[1]) not in my_list:
                    my_list.append((my_string+e[0],e[1]))
        return list(set(my_list))
    if pattern=='':
        if trie.value!= None:
           
            my_list.append((my_string, trie.value))
        return list(set(my_list)) 
    if pattern[0]=='?':
        for node in trie.children:
            my_list = my_list + word_filter(trie.children[node],pattern[1:],my_string+node)
    elif pattern[0] == '*':
        my_list = my_list + word_filter(trie,pattern[1:],my_string)
        for node in trie.children:
            my_list = my_list + word_filter(trie.children[node],pattern[:],my_string+node)
    else:
        if pattern[0] not in trie.children:
            return []
        else:
            my_list = my_list + word_filter(trie.children[pattern[0]],pattern[1:],my_string+pattern[0])
  
    return list(set(my_list))

# you can include test cases of your own in the block below.
if __name__ == '__main__':
    with open("resources\corpora\Pride and Prejudice.txt", encoding="utf-8") as f:
        text = f.read()
    trie = make_word_trie(text)
    print(word_filter(trie,'r?c*t'))
    pass
