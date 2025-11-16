cdef class Validator:
    cpdef bint validate(self, object element) 


cdef class TypeValidator(Validator):
    cdef object expected_type
    cpdef bint validate(self, object element)

cdef class NullValidator(Validator):
    cdef bint nullable
    cpdef bint validate(self, object element)

cdef class RegexValidator(Validator):
    cdef str pattern
    cdef bint full_match
    cdef bint negate
    cdef object engine
    cpdef bint validate(self, object element)

cdef class ConstraintValidator(Validator):
    cdef str expr
    cpdef bint validate(self, object element)

cdef class CustomFunctionValidator(Validator):
    cdef object func
    cpdef bint validate(self, object element):

