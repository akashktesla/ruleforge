from typing import Dict, List
from .builder import ColumnPolicyBuilder, RowPolicyBuilder
from .validators import (
    TypeValidator,
    RegexValidator,
    NullValidator,
    ConstraintValidator,
    CustomFunctionValidator,
)
import builtins
import pandas as pd
from .loader import load_config

cdef class RuleForger:
    cdef object df
    cdef dict[str,List] column_validators
    cdef List row_validators
    def __cinit__(self,object df):
        self.df = df
        self.column_validators: Dict[str, List] = {}
        self.row_validators: List = []
        #change the shit to path instead of df after it's cythonized

    cdef load_from_config(self, config_path: str):
        data = load_config(config_path)
        for colname, rules in data.get("column", {}).items():
            builder = ColumnPolicyBuilder(colname)
            for rule in rules:
                vtype = rule["validator"].lower()
                if vtype == "type":
                    t = getattr(builtins, rule["type"])
                    builder.add_validator(TypeValidator(t))
                elif vtype == "regex":
                    builder.add_validator(
                        RegexValidator(
                            rule.get("pattern", ""),
                            rule.get("full_match", True),
                            rule.get("negate", False),
                            rule.get("flags", 0),
                        )
                    )
                elif vtype == "nullable":
                    builder.add_validator(NullValidator(rule.get("nullable", False)))
                elif vtype == "constraint":
                    builder.add_validator(ConstraintValidator(rule.get("expr", "")))
                elif vtype == "customfunc":
                    func_name = rule.get("func")
                    func = globals().get(func_name)
                    builder.add_validator(CustomFunctionValidator(func))
            self.add_policy(builder)

    cdef add_policy(self, policy):
        if policy.scope == "column":
            self.column_validators.setdefault(policy.name, []).extend(policy.validators)
        else:
            self.row_validators.extend(policy.validators)

    cdef validate(self):
        self.validate_row_policy()
        self.validate_column_policy()

    cdef validate_row_policy(self):
        for row in self.df.itertuples():
            for validator in self.row_validators:
                validator.validate(row)

    cdef validate_column_policy(self):
        for column_name, validators in self.column_validators.items():
            for element in self.df[column_name]:
                for validator in validators:
                    if not validator.validate(element):
                        print(f"Value failed: {element}")
