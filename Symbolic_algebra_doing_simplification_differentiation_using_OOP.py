import doctest

# NO ADDITIONAL IMPORTS ALLOWED!
# You are welcome to modify the classes below, as well as to implement new
# classes and helper functions as necessary.


class Symbol:
    def __add__(self,other):
        return Add(self,other)
    def __sub__(self,other):
        return Sub(self,other)
    def __mul__(self,other):
        return Mul(self,other)
    def __truediv__(self,other):
        return Div(self,other)
    def __radd__(self,other):
        return Add(other,self)
    def __rsub__(self,other):
        return Sub(other,self)
    def __rmul__(self,other):
        return Mul(other,self)
    def __rtruediv__(self,other):
        return Div(other,self)
def number_check(i,s):#returns a number and an integer string
    int_string = ''
    for j in range(i,len(s)):
        if s[j] not in '1234567890':
            break
        else:
            int_string=int_string+s[j]
    if j==len(s)-1:
        return j+1,int_string
    else:
        return j,int_string
def tokenize(s):
    return_list = []
    i=0
    string = None
    while i<(len(s)):
        if s[i]== ')':
           
            return_list.append(s[i])
            i = i +1
            continue
        if s[i]!=' ':
            
            if s[i] in '1234567890':
                i, string = number_check(i,s)
                return_list.append(string)
                
                
            else:
                if s[i]!='-':
                    
                    return_list.append(s[i])
                  
                    i = i +1
                else:
                    if (i+1)<len(s):
                        if s[i+1] not in '1234567890':
                            return_list.append(s[i])
                            i = i+1
                        else:
                            i, string = number_check(i+1,s)
                            return_list.append('-'+string)
                            
                    else:
                        return_list.append(s[i])
        else:
            i=i+1
    return return_list





def parse(tokens):
   
    def parse_expression(index):
        
        if index<len(tokens):
            token = tokens[index]
            if token == '(':
               
                left,next_index = parse_expression(index+1)
                right,other_index = parse_expression(next_index+1)
                if tokens[next_index] == '+':
                    return Add(left,right),other_index+1
                if tokens[next_index] == '-':
                    return Sub(left,right),other_index+1
                if tokens[next_index] == '*':
                    return Mul(left,right),other_index+1
                if tokens[next_index] == '/':
                    return Div(left,right),other_index+1
            elif token.isdigit()or token[0]=='-':
                return Num(int(token)),index+1
            else:
                return Var(token),index+1
    parsed_expression,next_index = parse_expression(0)
    return parsed_expression
        
def sym(s):
    tokens = tokenize(s)
    return parse(tokens)
        

class Var(Symbol):
    def __init__(self, var):
        """
        Initializer.  Store an instance variable called `name`, containing the
        value passed in to the initializer.
        """
        self.name = var

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'Var(' + repr(self.name) + ')'
    def deriv(self,variable):
        if self.name==variable:
            return Num(1)
        elif self.name!=variable:
            return Num(0)
    def simplify(self):
        return Var(self.name)
    def eval(self,mapping):
        return mapping[self.name]

class Num(Symbol):
    def __init__(self, n):
        """
        Initializer.  Store an instance variable called `n`, containing the
        value passed in to the initializer.
        """
        self.n = n

    def __str__(self):
        return str(self.n)

    def __repr__(self):
        return 'Num(' + repr(self.n) + ')'
    def deriv(self,variable):
        return Num(0)
    def simplify(self):
        return Num(self.n)
    def eval(self,mapping):
        return self.n
class BinOp(Symbol):
    def __init__(self,left,right):
        self.left=left
        self.right=right
        if isinstance(self.left,(int,str)):
            if isinstance(self.left,int):
                self.left=Num(self.left)
            else:
                self.left=Var(self.left)
            
        if isinstance(self.right,(int,str)):
            if isinstance(self.right,int):
                self.right=Num(self.right)
            else:
                self.right=Var(self.right)
    def __str__(self):
        
        if not isinstance(self,(Add,Div,Mul,Sub)):
            return str(self)
            
        my_dict = {'D':4,'M':3,'A':2,'S':1,'O':0}
        str_check=None
        str_r_check=None
        str_l_check=None
        if isinstance(self,Add):
            str_check = 'A'
        elif isinstance(self,Mul):
            str_check = 'M'
        elif isinstance(self,Div):
            str_check = 'D'
        elif isinstance(self,Sub):
            str_check = 'S'
        else:
            str_check='O'
        if isinstance(self.right,Add):
            str_r_check = 'A'
        elif isinstance(self.right,Mul):
            str_r_check = 'M'
        elif isinstance(self.right,Div):
            str_r_check = 'D'
        elif isinstance(self.right,Sub):
            str_r_check = 'S'
        else:
            str_r_check = 'O'
        if isinstance(self.left,Add):
            str_l_check = 'A'
        elif isinstance(self.left,Mul):
            str_l_check = 'M'
        elif isinstance(self.left,Div):
            str_l_check = 'D'
        elif isinstance(self.left,Sub):
            str_l_check = 'S'
        else:
            str_l_check='O'
        if my_dict[str_check]==4 and my_dict[str_l_check]==3:
            if my_dict[str_r_check]!=0:
                return str(self.left) + ' ' + self.symbol+' ('+str(self.right)+')'
            else:
                return str(self.left)+' ' +self.symbol+' '+ str(self.right)
        if my_dict[str_check]==2:
            return str(self.left)+' ' + self.symbol+' '+str(self.right)
        if my_dict[str_check]==1 and my_dict[str_r_check]==2:
            return str(self.left) + ' ' +self.symbol+ ' ('+str(self.right)+')'
                
        
        if my_dict[str_l_check]!=0 and my_dict[str_r_check]!=0:
            if my_dict[str_check]>my_dict[str_r_check]:
                if my_dict[str_check]>my_dict[str_l_check]:
                    return '(' + str(self.left)+') '+self.symbol+' ('+str(self.right)+')'
                else:
                    return str(self.left)+' ' + self.symbol + ' (' + str(self.right)+')'
            elif my_dict[str_check]==my_dict[str_r_check]:
                if my_dict[str_check] in [1,4]:
                    if my_dict[str_l_check]< my_dict[str_check]:
                        return '(' + str(self.left)+') '+self.symbol+' ('+str(self.right)+')'
                    else:
                        return str(self.left)+' ' + self.symbol + ' (' + str(self.right)+')'
                else:
                    if my_dict[str_l_check]< my_dict[str_check]:
                        return '(' + str(self.left)+') '+self.symbol+' '+str(self.right)
                    else:
                        return str(self.left)+' ' + self.symbol + ' ' + str(self.right)
            else:
                if my_dict[str_check]>my_dict[str_l_check]:
                    return '(' + str(self.left)+') '+self.symbol +' '+str(self.right)
                else:
                    return str(self.left)+' '+self.symbol+' '+str(self.right)
        elif my_dict[str_l_check]==0 and my_dict[str_r_check]==0:
            return str(self.left)+' '+ self.symbol+ ' '+ str(self.right)
        else:
            if my_dict[str_l_check]==0:
                
                if my_dict[str_r_check]<my_dict[str_check]:
                    
                    return str(self.left)+' '+self.symbol+' ('+str(self.right)+')'
                elif my_dict[str_r_check]==my_dict[str_check]:
                   
                    if my_dict[str_check] in [1,4]:
                       
                        return str(self.left)+' '+self.symbol+' '+ '(' + str(self.right)+')'
                    else:
                        return str(self.left)+' '+self.symbol+' '+ str(self.right)
                else:
                    
                    return str(self.left)+' '+self.symbol+' '+str(self.right)
            else:
                if my_dict[str_l_check]<my_dict[str_check]:
                    return '(' + str(self.left)+') '+self.symbol+' '+str(self.right)
                else:
                    return str(self.left)+' '+self.symbol+' '+ str(self.right)
class Add(BinOp):
    def __init__(self,left,right):
         BinOp.__init__(self,left,right)
         self.symbol = '+'
    def __repr__(self):
        return 'Add('+repr(self.left)+','+ repr(self.right) + ')'
    def deriv(self,variable):
        return self.left.deriv(variable)+self.right.deriv(variable)
    def simplify(self):
        left1 = self.left.simplify()
        right1 = self.right.simplify()
        if isinstance(left1,Num) and left1.n==0:
         
            return right1
        if isinstance(right1,Num) and right1.n==0:
        
             return left1
        if isinstance(left1,Num) and isinstance(right1,Num):
            return Num(left1.n + right1.n)
        return left1+right1
    def eval(self,mapping):
        left1 = self.left.eval(mapping)
        right1 = self.right.eval(mapping)
        return left1+right1
class Sub(BinOp):
    def __init__(self,left,right):
         BinOp.__init__(self,left,right)
         self.symbol = '-'
    def __repr__(self):
        return 'Sub('+repr(self.left)+','+repr(self.right) + ')'
    def deriv(self,variable):
        return self.left.deriv(variable)-self.right.deriv(variable)
    def simplify(self):
        left1 = self.left.simplify()
        right1 = self.right.simplify()
        if isinstance(right1,Num) and right1.n==0:
            return left1
        if isinstance(left1,Num) and isinstance(right1,Num):
            return Num(left1.n - right1.n)
        return left1-right1
    def eval(self,mapping):
        left1 = self.left.eval(mapping)
        right1 = self.right.eval(mapping)
        return left1-right1
class Mul(BinOp):
    def __init__(self,left,right):
         BinOp.__init__(self,left,right)
         self.symbol = '*'
    def __repr__(self):
        return 'Mul('+repr(self.left)+','+repr(self.right) + ')'
    def deriv(self,variable):
        return self.left*self.right.deriv(variable)+self.right*self.left.deriv(variable)
    def simplify(self):
        left1 = self.left.simplify()
        right1 = self.right.simplify()
        if isinstance(left1,Num) and left1.n==0:
            return Num(0)
        if isinstance(right1,Num) and right1.n==0:
            return Num(0)
        if isinstance(left1,Num) and left1.n==1:
            return right1
        if isinstance(right1,Num) and right1.n==1:
            return left1
        if isinstance(left1,Num) and isinstance(right1,Num):
            return Num(left1.n*right1.n)
        return left1*right1
    def eval(self,mapping):#question , why they are integer types but doing ??
        left1=self.left.eval(mapping)
        right1=self.right.eval(mapping)
        return left1*right1
class Div(BinOp):
    def __init__(self,left,right):
         BinOp.__init__(self,left,right)
         self.symbol = '/'
    def __repr__(self):
        return 'Div('+repr(self.left)+','+repr(self.right) + ')'
    def deriv(self,variable):
        return (self.right*self.left.deriv(variable)-self.left*self.right(variable))/(self.right)*(self.right)
    def simplify(self):
        left1 = self.left.simplify()
        right1 = self.right.simplify()
        if isinstance(left1,Num) and left1.n==0:
            return Num(0)
        if isinstance(right1,Num) and right1.n==1:
            return left1
        if isinstance(right1,Num) and isinstance(left1,Num):
            return Num(left1.n/right1.n)
        
        return left1/right1
    def eval(self,mapping):
        left1=self.left.eval(mapping)
        right1=self.right.eval(mapping)
        return left1/right1
if __name__ == '__main__':
    
    while True:
        my_input=input()
        if my_input!='QUIT':
          
            result = sym(my_input)
            print(repr(result))
        else:
            break
        
    
        
    doctest.testmod()
