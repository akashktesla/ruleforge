import pandas as pd
from enum import Enum
import re
import json
import builtins



def enforce_type(value,value_name,type):
    if not isinstance(value,type):
        raise TypeError(f"Value must be of value_name {type}, got {type(value)}")


class ColumnPolicyBuilder:
    def __init__(self,name):
        self.name = name
        self.scope = "column"
        self.validators = []

    def add_validator(self,validator):
        self.validators.append(validator)
        return self

class RowPolicyBuilder:
    def __init__(self):
        self.scope = "row"
        self.validators = []

    def add_validator(self,validator):
        self.validators.append(validator)
        return self


class RuleForger:
    def __init__(self,df):
        self.df = df
        self.column_validators = {}
        self.row_validators = []

    def load_from_config(self,config):
        with open(config) as f:
            data = json.loads(f.read())
            #Column scope
            # print(data["column"])
            for i in data["column"].keys():
                column_builder = ColumnPolicyBuilder(i)
                for validator in data["column"][i]:
                    if validator["validator"].lower()=="type":
                        type_ = getattr(builtins, validator["type"])
                        column_builder.add_validator(TypeValidator(type_))
                    elif validator["validator"].lower()=="regex":
                        #Get or default values
                        pattern = validator.get("pattern","")
                        full_match = validator.get("full_match",True)
                        flags = validator.get("flags",0)
                        negate = validator.get("negate",False)
                        column_builder.add_validator(RegexValidator(pattern,full_match,negate,flags))
                    elif validator["validator"].lower()=="nullable":
                        nullable = validator.get("nullable",False)
                        column_builder.add_validator(NullValidator(nullable))
                    elif validator["validator"].lower()=="Constraint":
                        nullable = validator.get("expr","")
                        column_builder.add_validator(ConstraintValidator(expr))
                    elif validator["validator"].lower()=="customFunc":
                        func = globals().get(validator.get("func"))
                        column_builder.add_validator(CustomFunctionValidator(func))
                self.add_policy(column_builder)




    def add_policy(self,policy):
        if policy.scope == "column":
            try:
                self.column_validators[policy.name].extend(policy.validators)
            except:
                self.column_validators[policy.name] = policy.validators

        elif policy.scope == "row":
            self.row_validators.extend(policy.validators)

    def validate(self):
        self.validate_row_policy()
        self.validate_column_policy()

    def validate_row_policy(self):
        for row in self.df.itertuples():
            for validator in self.row_validators:
                validator.validate(row)
    def validate_column_policy(self):
        for column_name in self.column_validators.keys():
            for element in self.df[column_name]:
                #Validate Type
                for validator in self.column_validators[column_name]:
                    if not validator.validate(element):
                        print(f"Value failed: {element}")

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

class CustomFunctionValidator():
    def __init__(self,func):
        self.func = func
    def validate(self,element):
        return self.func(element)


def print_data(row):
    print(f"HomePlanet: {row.HomePlanet}, CryoSleep: {row.CryoSleep}")
    return True


if __name__ == "__main__":
    df = pd.read_csv("datasets/spaceship-titanic/train.csv")
    print(df.head())
    rf = RuleForger(df)
    rf.load_from_config("config.json")
    print(rf.column_validators)
    rf.validate()



    # v = RegexValidator(r"^[A-Z]{2}\d{4}$")
    # print(v.validate("AB1234")) 
    # print(v.validate("abc1234")) 

    # v = ConstraintValidator("element%2 ==0")
    # print(v.validate(23))


"""
TODO: 
2. row wise validators mayb or ig scope could cover that idk
3. Rule book - load_from_rule_book() - probably implement this after architecture is complete
"""
