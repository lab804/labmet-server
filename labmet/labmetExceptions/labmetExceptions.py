__author__ = 'joao'


class InputException(Exception):
    """Input Exception

    Raises exceptions when forbidden
    parameters are used as inputs

    :raises: InputException
    """


class InputTypeException(Exception):
    """Wrong Input type Exceptions

    Raises exceptions when a forbidden
    type is used as parameter

    :raises: InputTypeException
    """
    pass


class InputRangeException(Exception):
    """Wrong Input Range Exception

    Raises exceptions when the input
    is out of bounds

    :raises: InputRangeException
    """