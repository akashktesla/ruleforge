import pandas as pd
from enum import Enum
import re

def enforce_type(value,value_name,type):
    if not isinstance(value,type):
        raise TypeError(f"Value must be of value_name {type}, got {type(value)}")


class RuleForger:
    def __init__(self,df):
        self.df = df
        self.column_policies = []

    def add_column_policy(self,policy):
        self.column_policies.append(policy)

    def validate(self):
        for policy in self.column_policies:
            self.validate_column_policy(policy)

    def validate_column_policy(self,policy):
        for i in df[policy.name]:
            #Validate Type
            for validator in policy.validators:
                if not validator.validate(i):
                    print(f"Value failed: {i}")

class ColumnPolicy:
    def __init__(self,name):
        enforce_type(value = name,value_name="Name",type=str)
        self.name = name
        self.validators = []

    def add_validator(self,validator):
        self.validators.append(validator)
        return self
    


#Validators 

class Validator():
    def validate():
        raise "Validate function is not implemented"

class TypeValidator(Validator):
    def __init__(self,type_):
        self.type = type_
    def validate(self,element):
        if type(element) == self.type:
            return True
        else:
            return False

class NullValidator(Validator):
    def __init__(self,nullable):
        self.nullable = nullable
    def validate(self,element):
        if self.nullable:
            return True
        else:
            if element !=None:
                return True
            else:
                return False

class RegexValidator(Validator):
    def __init__(self,pattern,full_match=True,negate=False,flags=0):
        self.pattern = pattern
        self.full_match = full_match
        self.negate = negate
        self.engine = re.compile(pattern,flags)

    def validate(self,element):
        if element is None:
            return True
        if type(element)!=str:
            return False
        if self.full_match:
            return bool(self.engine.fullmatch(element)) ^ self.negate
        else:
            return bool(self.engine.search(element)) ^ self.negate

class ConstraintValidator():
    def __init__(self,expr):
        self.expr = expr
    def validate(self,element):
        try:
            return bool(eval(self.expr))
        except:
            return False




if __name__ == "__main__":
    # df = pd.read_csv("datasets/spaceship-titanic/train.csv");
    # print(df.head())
    # rf = RuleForger(df)
    # policy = ColumnPolicy("HomePlanet")\
    #         .add_validator(NullValidator(False))\
    #         .add_validator(TypeValidator(str))
    # rf.add_column_policy(policy)
    # rf.validate()

    # v = RegexValidator(r"^[A-Z]{2}\d{4}$")
    # print(v.validate("AB1234")) 
    # print(v.validate("abc1234")) 

    v = ConstraintValidator("element%2 ==0")
    print(v.validate(23))


"""
TODO: 
1. implement scop for validators
2. row wise validators mayb or ig scope could cover that idk
"""

