import pandas as pd
from enum import Enum

def enforce_type(value,value_name,type):
    if not isinstance(value,type):
        raise TypeError(f"Value must be of value_name {type}, got {type(value)}")


class ColumnPolicy:
    def __init__(self):
        pass

    def name(self,name:str):
        enforce_type(value = name,value_name="Name",type=str)
        self.name = name
        return self

    def type(self,type_):
        enforce_type(value = type_,value_name="Type",type=type)
        self.type = type_
        return self

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
            if type(i) != policy.type:
                print(f"Type {type(i)}, Required: {policy.type}")
                print(f"Mismatch found: {i}")




if __name__ == "__main__":
    df = pd.read_csv("datasets/spaceship-titanic/train.csv");
    print(df.head())
    rf = RuleForger(df)
    policy = ColumnPolicy()\
            .name("HomePlanet")\
            .type(str)
    rf.add_column_policy(policy)
    rf.validate()


    # policy = [{
    #               "column":"HomePlanet",
    #           },]



