
cdef class RuleForger:
    cdef object df
    cdef dict column_validators
    cdef list row_validators
    cpdef void load_from_config(self, str config_path)
    cpdef void add_policy(self, object policy)
    cpdef void validate(self)
    cpdef void validate_row_policy(self)
    cpdef void validate_column_policy(self)
