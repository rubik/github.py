class GithubPyError(Exception):
    '''Base class for all github.py errors.'''

class APIError(GithubPyError):
    '''Raised when Github API returns an error.'''