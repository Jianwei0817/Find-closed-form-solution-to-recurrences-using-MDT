
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 15:21:00 2019
@author: jwangdk
"""
import sympy
from sympy import *
from sympy.abc import c, n, b, y, z, l, k
from z3 import *
import z3
import time
import copy
import sys

f=sympy.Function('f')

MTT=1800 #(:seconds)



def sympy_to_z3(sympy_var_list):     

    z3_vars = [] 
    z3_var_map = {} 

    for var in sympy_var_list: 
     name = var.name 
     z3_var = z3.Real(name) 
     z3_var_map[name] = z3_var 
     z3_vars.append(z3_var) 
    return z3_vars

#def sympy_to_z3(sympy_var):     
#    name = sympy_var.name 
#    z3_var = z3.Real(name) 
#    return z3_var



def sortConj(Conjecture_space):
    
    before_conj=dict()
    for i in list(Conjecture_space):
        before_conj[i.subs(n,2)]=i
    after_conj=sorted(before_conj)
    sorted_conj=[]
    for i in after_conj:        
        sorted_conj.append(before_conj[i])
    #print(sorted_conj)
    return sorted_conj


def conjectureSpace_1(iter_num):
    Conjecture_base=set()    
    CONJ=[]
    CONJ.append(c)
    Conjecture_base.add(n)    
    Conjecture_space=set()
    Conjecture_space.add(n)    
    count_1=0
    while(count_1<=iter_num):
        for conj1 in Conjecture_base:
            #Conjecture_space.add(expand(Symbol(chr(random.randint(80,90)))*conj1))
            for conj2 in Conjecture_base:             
                #Conjecture_space.add(expand(Symbol(chr(random.randint(83,85)))*conj1)+expand(Symbol(chr(random.randint(86,88)))*conj2))
                Conjecture_space.add(expand(conj1*conj2))            
        Conjecture_base=Conjecture_base.union(Conjecture_space)
       
        count_1=count_1+1
    sorted_space=sortConj(Conjecture_space)
    conj=c
    
    for i in range(len(sorted_space)):
        conj=conj+(sympy.Symbol(chr(65+i))*(sorted_space)[i]) 
        CONJ.append(conj)
              
   
    return CONJ


def induction_prover_cond(cond1,final_cond,final_conj1,final_conj2,recurr_expression1,recurr_expression2,m,R_):

    
    if final_cond.subs(n,m):
        
        
        if final_conj1.subs(n,m)==R_[f(m)]:
            
            R_[f(k)]=final_conj1.subs(n,k)
            #print(R_[f(k)])
            #print(final_conj1.subs(n,k))
            cmp1_frt=final_conj1.subs(n,(k+1))
            #print("#"*20)
            #print(sympy.expand(cmp1_frt))
            if (cond1.subs(n,m)).subs(f(m),R_[f(m)]):
                temp1=recurr_expression1.subs(n,k)  
                result_exp1=sympy.solve(temp1,f(k+1),check=False)[0]    
                cmp1_snd=result_exp1.subs(f(k),R_[f(k)])
                
            else:
                temp1=recurr_expression2.subs(n,k)
                result_exp1=sympy.solve(temp1,f(k+1),check=False)[0]
                cmp1_snd=result_exp1.subs(f(k),R_[f(k)]) 
                                                   
            #print(sympy.expand(cmp1_snd))

        else:   
            #print("Unfortunately!")
            return False
        
        R_[f(l)]=final_conj2.subs(n,l)
        cmp2_frt=final_conj2.subs(n,(l+1))
        if not (cond1.subs(n,m)).subs(f(m),R_[f(m)]):
            temp2=recurr_expression1.subs(n,l)  
            result_exp2=sympy.solve(temp2,f(l+1),check=False)[0]    
            cmp2_snd=result_exp2.subs(f(l),R_[f(l)])
        else:
            temp2=recurr_expression2.subs(n,l)
            result_exp2=sympy.solve(temp2,f(l+1),check=False)[0]
            cmp2_snd=result_exp2.subs(f(l),R_[f(l)])         
        #print("*"*20)
        #print(sympy.expand(cmp2_frt))
        #print(sympy.expand(cmp2_snd))
        #print("*"*20)    
    else: 
        
        
        if final_conj2.subs(n,m)==R_[f(m)]:
            
            R_[f(k)]=final_conj2.subs(n,k)            
            cmp2_frt=final_conj2.subs(n,(k+1))
            #print("#"*20)
            #print(sympy.expand(cmp2_frt))
            if (cond1.subs(n,m)).subs(f(m),R_[f(m)]):
                temp2=recurr_expression1.subs(n,k)  
                result_exp2=sympy.solve(temp2,f(k+1),check=False)[0]    
                cmp2_snd=result_exp2.subs(f(k),R_[f(k)])
                
            else:
                temp2=recurr_expression2.subs(n,k)
                result_exp2=sympy.solve(temp2,f(k+1),check=False)[0]
                cmp2_snd=result_exp2.subs(f(k),R_[f(k)])       
                                            
            #print(sympy.expand(cmp2_snd))

        else:   
            #print("Unfortunately!")
            return False         
        
        R_[f(l)]=final_conj1.subs(n,l)
        cmp1_frt=final_conj1.subs(n,(l+1))
        if not (cond1.subs(n,m)).subs(f(m),R_[f(m)]):
            temp1=recurr_expression1.subs(n,l)  
            result_exp1=sympy.solve(temp1,f(l+1),check=False)[0]    
            cmp1_snd=result_exp1.subs(f(l),R_[f(l)])
        else:
            temp1=recurr_expression2.subs(n,l)
            result_exp1=sympy.solve(temp1,f(l+1),check=False)[0]
            cmp1_snd=result_exp1.subs(f(l),R_[f(l)])         
        #print("*"*20)

    if sympy.expand(cmp1_frt) == sympy.expand(cmp1_snd) or sympy.expand(cmp2_frt) == sympy.expand(cmp2_snd):
        
        return True
    else:
        
        return False 

def conjectureSpace_2(iter_num):
    Conjecture_base=set()
    
    CONJ=[]
    CONJ.append(b)

    Conjecture_base.add(n)
    
    Conjecture_space=set()
    Conjecture_space.add(n)
    
    count_1=0

    while(count_1<=iter_num):
        for conj1 in Conjecture_base:
            #Conjecture_space.add(expand(Symbol(chr(random.randint(80,90)))*conj1))

            for conj2 in Conjecture_base:
             
                #Conjecture_space.add(expand(Symbol(chr(random.randint(83,85)))*conj1)+expand(Symbol(chr(random.randint(86,88)))*conj2))
                Conjecture_space.add(expand(conj1*conj2))
                
                
             
        Conjecture_base=Conjecture_base.union(Conjecture_space)
       
        count_1=count_1+1
    sorted_space=sortConj(Conjecture_space)
    conj=b
    
    for i in range(len(sorted_space)):
        conj=conj+(sympy.Symbol(chr(90-i))*(sorted_space)[i]) 
        CONJ.append(conj)
               
   
    return CONJ

def conditionSpace(iter_num):
    Conjecture_base=set()
    
    CONDITION=[]
    

    Conjecture_base.add(n)
    
    Conjecture_space=set()
    Conjecture_space.add(n)
    
    count_1=0

    while(count_1<=iter_num):
        for conj1 in Conjecture_base:
            #Conjecture_space.add(expand(Symbol(chr(random.randint(80,90)))*conj1))

            for conj2 in Conjecture_base:
             
                #Conjecture_space.add(expand(Symbol(chr(random.randint(83,85)))*conj1)+expand(Symbol(chr(random.randint(86,88)))*conj2))
                Conjecture_space.add(expand(conj1*conj2))
                
                
             
        Conjecture_base=Conjecture_base.union(Conjecture_space)
       
        count_1=count_1+1
    sorted_space=sortConj(Conjecture_space)
    conj=z
    
    for i in range(len(sorted_space)):
        conj=conj+(sympy.Symbol(chr(111+i))*(sorted_space)[i]) 
        CONDITION.append(conj)
                
   
    return CONDITION




def Solve_cond_r(m,init_value,cond1=None,recurr_expression1=None,recurr_expression2=None):
    break_Flag=False
 
    
    R_={}
    R_[f(m)]=init_value
    
    eqs=[]
    
    start=time.clock()

    
    A,B,C,D,E,F,G,H,I,J,K,L,M=sympy.symbols('A,B,C,D,E,F,G,H,I,J,K,L,M')
    N,O,P,Q,R,S,T,U,V,W,X,Y,Z=sympy.symbols('N,O,P,Q,R,S,T,U,V,W,X,Y,Z')
    b,c,o,p,q,r,s,t,u,v,w,x,y,z=sympy.symbols('b,c,o,p,q,r,s,t,u,v,w,x,y,z')
    

    past_conj_set=[]
    for space_size in range(sys.maxsize):
        Condition_space=[]
        cond_space=conditionSpace(space_size)
        
        for cond in cond_space:
            Condition_space.append(cond>=0)
            #Condition_space.append(cond>0)
        '''
        Condition_space.append(cond_space[-1]>=0)
        Condition_space.append(cond_space[-1]>0)'''
            
        for condition in Condition_space:
            
            for conj1 in conjectureSpace_1(space_size):
                
                for conj2 in conjectureSpace_2(space_size):
                    if (condition,conj1,conj2) in past_conj_set: 
                        continue
                    else:
                        past_conj_set.append((condition,conj1,conj2))
                    
                    print("Conjecture: 'ite(%s, %s, %s)'."%(condition,conj1,conj2))
                    
                    for i in [(j+m) for j in range(30)]:
                        
                        cd=condition.subs(n,i)
                        
                        

                        if (cond1.subs(n,i)).subs(f(i),R_[f(i)]):
                                                      
                            r_eq=recurr_expression1.subs(n,i)        
                        else:
                                                     
                            r_eq=recurr_expression2.subs(n,i)

                                                
                        p_=r_eq.subs(f(i),R_[f(i)])
                        R_[f(i+1)]=sympy.solve(p_,f(i+1),check=False)[0]                      
                        left=R_[f(i)]   

                        
                        right1=conj1.subs(n,i)
                        right2=conj2.subs(n,i)
                        

                        sympy_var_list1=[A,B,C,D,E,F,G,H,I,J,K,L,M]
                        A,B,C,D,E,F,G,H,I,J,K,L,M=sympy_to_z3(sympy_var_list1)
                        sympy_var_list2=[N,O,P,Q,R,S,T,U,V,W,X,Y,Z]
                        N,O,P,Q,R,S,T,U,V,W,X,Y,Z=sympy_to_z3(sympy_var_list2)
                        sympy_var_list3=[b,c,o,p,q,r,s,t,u,v,w,x,y,z]
                        b,c,o,p,q,r,s,t,u,v,w,x,y,z=sympy_to_z3(sympy_var_list3)
                        
                        
                        
                        cd=(eval(str(cd)))
                        right1=(eval(str(right1)))
                        right2=(eval(str(right2)))
                        
                        
                        
                        z3.If(cd,right1,right2)
                        eqs.append(z3.If(cd, right1==left, right2==left))  
                        #print(eqs)
                        
                        A,B,C,D,E,F,G,H,I,J,K,L,M=sympy.symbols('A,B,C,D,E,F,G,H,I,J,K,L,M')
                        N,O,P,Q,R,S,T,U,V,W,X,Y,Z=sympy.symbols('N,O,P,Q,R,S,T,U,V,W,X,Y,Z')
                        b,c,o,p,q,r,s,t,u,v,w,x,y,z=sympy.symbols('b,c,o,p,q,r,s,t,u,v,w,x,y,z')

                    
                    sol=z3.Solver()
                    sol.add(eqs)
                    result=sol.check()
                    
                    
                    if result==z3.sat:
                        end=time.clock()
                        time_cost=end-start
                        mol=sol.model()
                        #print(type(str(bb)))
                        rr=dict()
                        
                        for d in mol.decls():
                            
                            rr[eval(d.name())]=sympy.Rational(str(mol[d]))
        
                        final_conj1=conj1.subs(rr)
                        #print(final_conj1)
                        final_conj2=conj2.subs(rr)
                        #print(final_conj2)
                        final_cond=condition.subs(rr)
                        
                        res=induction_prover_cond(cond1,final_cond,final_conj1,final_conj2,recurr_expression1,recurr_expression2,m,R_)
                        
                        if res:                                
                            #print(condition)
                            #print(final_cond)
                            #print(R_)
                            print("Congratulations!!The conjecture f(n)=ite(%s, %s, %s) must be correct!!!"%(final_cond,final_conj1,final_conj2))
                            print("Usage of time:", time_cost, "seconds")
                            #return[final_cond,final_conj1,final_conj2,time_cost]
                            break_Flag=True
                            break
                        else:
                            end=time.clock()
                            time_cost=end-start
                            if time_cost>=MTT:
                                break_Flag=True
                                print("Sorry, we cannot find the closed form solution to this recurrence in %s mins!"%(int(MTT/60)))
                                #return -1
                                break
                            else:
                                R_={}
                                R_[f(m)]=init_value
                                eqs=[]
                                print("*"*20)
                    else:
                        end=time.clock()
                        time_cost=end-start
                        if time_cost>=MTT:
                            break_Flag=True
                            print("Sorry, we cannot find the closed form solution to this recurrence in %s mins!"%(int(MTT/60)))
                            #return -1
                            break
                        else:
                            R_={}
                            R_[f(m)]=init_value    
                            eqs=[]
                            #print("The conjecture 'ite(%s, %s, %s)' is NOT correct."%(condition,conj1,conj2))
                            #print("*"*20)
                            
                if break_Flag==True:
                    break
            if break_Flag==True:
                break
        if break_Flag==True:
            break

  
if __name__=="__main__":
    "some examples"
    Solve_cond_r(1,2,n<10,f(n+1)-f(n)+2*n**2-3*n,f(n+1)-f(n)-2*n+3)

    
    
    
    
    
    
