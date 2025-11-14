cdef class Validator:
    cpdef bint validate(self, object element):
        raise NotImplementedError

cdef class TypeValidator(Validator):
    def __cinit__(self, object expected_type):
        self.expected_type = expected_type

    cpdef bint validate(self, object element):
        return isinstance(element, self.expected_type)
