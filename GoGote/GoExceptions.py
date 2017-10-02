#! /usr/bin/env python3


class GoExceptions(Exception):
    """
    Base exception class for all Exceptions
    GoGote implements.
    """
    pass


class IllegalMoveError(GoExceptions):
    """
    Error that is raised when an illegal Move is attempted

    Attributes:
        move -- the coordiantes of the move that was rejected
        message -- explanation of the error
    """

    def __init__(self, move, message):
        self.move = move
        self.message = message


class KoError(GoExceptions):
    def __init__(self, move, message):
        self.move = move
        self.message = message
