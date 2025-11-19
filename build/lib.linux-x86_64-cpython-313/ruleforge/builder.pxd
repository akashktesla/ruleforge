cdef class ColumnPolicyBuilder:
    cdef list validators
    cdef str scope 
    cdef str name
    cpdef add_validator(self, validator)

cdef class RowPolicyBuilder:
    cdef str scope
    cdef list validators
    cpdef add_validator(self, object validator)
