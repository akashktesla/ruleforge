cdef class ColumnPolicyBuilder:
    cdef public list validators
    cdef public str scope 
    cdef public str name
    def __cinit__(self, str name):
        self.name = name
        self.scope = "column"
        self.validators = []

    cpdef add_validator(self, validator):
        self.validators.append(validator)
        return self


cdef class RowPolicyBuilder:
    cdef public str scope
    cdef public list validators
    def __cinit__(self):
        self.scope = "row"
        self.validators = []

    cpdef add_validator(self, object validator):
        self.validators.append(validator)
        return self
