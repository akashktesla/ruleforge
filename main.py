import pandas as pd
from enum import Enum

def enforce_type(value,value_name,type):
    if not isinstance(value,type):
        raise TypeError(f"Value must be of value_name {type}, got {type(value)}")


class ColumnPolicy:
    def __init__(self):
        return None
    def name(self,name:str):
        enforce_type(value = name,value_name="name",type= str)
        self.name = name
        return self
    def type(self,type):
        self.type = type
        return self

def clean_with_policy(df,policy):
    print(f"policy: {policy}")


if __name__ == "__main__":
    df = pd.read_csv("datasets/spaceship-titanic/train.csv");
    print(df.head())
    policy = ColumnPolicy()\
            .name("HomePlanet")\
            .type(str)

    print(policy.name)

    # policy = [{
    #               "column":"HomePlanet",
    #           },]



