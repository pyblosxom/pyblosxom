"""
This module holds the Request class which encapsulates the data
involved in executing a pyblosxom request.
"""

class Request:
    """
    This class holds the PyBlosxom request.  It holds configuration
    information, HTTP/CGI information, and data that we calculate
    and transform over the course of execution.

    There should be only one instance of this class floating around
    and it should get created by pyblosxom.cgi and passed into the
    PyBlosxom instance which will do further manipulation on the
    Request instance.
    """
    def __init__(self):
        # this holds configuration data that the user changes 
        # in config.py
        self._configuration = {}

        # this holds HTTP/CGI oriented data specific to the request
        # and the environment in which the request was created
        self._http = {}

        # this holds run-time data which gets created and transformed
        # by pyblosxom during execution
        self._data = {}

    def getConfiguration(self):
        return self._configuration

    def getHttp(self):
        return self._http

    def getData(self):
        return self._data

    def dumpRequest(self):
        # some dumping method here?  pprint?
        pass

    def __populateDict(self, currdict, newdict):
        for mem in newdict.keys():
            currdict[mem] = newdict[mem]

    def addHttp(self, d):
        """
        Takes in a dict and adds/overrides values in the existing
        http dict with the new values.

        @param d: the dict with the new keys/values to add
        @type  d: dict
        """
        self.__populateDict(self._http, d)

    def addData(self, d):
        """
        Takes in a dict and adds/overrides values in the existing
        data dict with the new values.

        @param d: the dict with the new keys/values to add
        @type  d: dict
        """
        self.__populateDict(self._data, d)

    def addConfiguration(self, d):
        """
        Takes in a dict and adds/overrides values in the existing
        configuration dict with the new values.

        @param d: the dict with the new keys/values to add
        @type  d: dict
        """
        self.__populateDict(self._configuration, d)

# vim: shiftwidth=4 tabstop=4 expandtab
