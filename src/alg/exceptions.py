class InputSimplexException(Exception):

    def __init__(self, object_name):
        Exception.__init__(self)
        self.object_name = object_name
        self.err_type = "Error in input parameters, check: "

    def message(self):
        return self.err_type + self.object_name


class SimplexAlgorithmException(Exception):

    def __init__(self):
        Exception.__init__(self)
        self.err_type = "The objective function is not " \
                        "bounded below on many constraints."

    def message(self):
        return self.err_type


class LoopingAlgorithmException(Exception):

    def __init__(self):
        Exception.__init__(self)
        self.err_type = "A looping phenomenon has occurred in the algorithm." \
                        " Please try changing variable limits or " \
                        "entering other data."

    def message(self):
        return self.err_type


class IncompleteTaskRankException(Exception):

    def __init__(self):
        Exception.__init__(self)
        self.type_err = "The constraint matrix has an incomplete rank," \
                        " the rank matrix should equal the number of rows," \
                        " check the data."

    def message(self):
        return self.type_err


class NotSolveSimplexException(Exception):

    def __init__(self):
        Exception.__init__(self)
        self.err_type = "No solutions."

    def message(self):
        return self.err_type
