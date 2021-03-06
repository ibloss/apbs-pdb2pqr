""" Handle the storage of APBS input file parameters """
from abc import ABCMeta, abstractmethod, abstractproperty
import sys

float_epsilon = sys.float_info.epsilon

class Parameter(object):
    """ Parameter structure to simplify storing input file values """
    __metaclass__ = ABCMeta
    
    @abstractproperty
    def name(self):
        """ Each parameter class should define a name """
        pass
    
    @abstractmethod
    def parse(self, tokens):
        """ This function should pop tokens off the top of a stack and parse them.  The stack should
        be modified. """
        pass
    
    @abstractmethod
    def validate(self):
        """ Validate the contents of this parameter.  Raise Exception on error. """
        pass
    
    @abstractmethod
    def contents(self):
        """ Return the contents of this parameter as a dictionary """
        pass
    
    @abstractmethod
    def __str__(self):
        pass
    
class OneStringParameter(Parameter):
    """ Generic class for one-string parameter """
    def __init__(self):
        self.parm = None

    def parse(self, tokens):
        self.parm = tokens.pop(0)
    
    def validate(self):
        try:
            if not self.parm in self.allowed_values:
                errstr = "Unknown option %s for %s" % (self.parm, self.name)
                raise ValueError, errstr
        except AttributeError:
            pass
    
    def __str__(self):
        outstr = "%s %s" % (self.name, self.parm)
        return outstr
    
    def contents(self):
        return { self.name : self.parm }

class OneIntegerParameter(Parameter):
    """ Generic class for one-integer parameter """
    def __init__(self):
        self.parm = None

    def parse(self, tokens):
        self.parm = int(tokens.pop(0))
    
    def validate(self):
        if self.parm is None:
            errstr = "Missing value for parameter %s" % self.name
            raise ValueError, errstr
    
    def __str__(self):
        outstr = "%s %d" % (self.name, self.parm)
        return outstr
    
    def contents(self):
        return { self.name : self.parm }

class ParameterSection(Parameter):
    """ Complex parameters as found in an input file section """
    def __init__(self):
        self.content_dict = {}
    
    def contents(self):
        return self.content_dict
    

class OneFloatParameter(Parameter):
    """ Generic class for one-float parameter """
    def __init__(self):
        self.parm = None

    def parse(self, tokens):
        self.parm = float(tokens.pop(0))
    
    def validate(self):
        if self.parm is None:
            errstr = "Missing value for parameter %s" % self.name
            raise ValueError, errstr
    
    def __str__(self):
        outstr = "%s %g" % (self.name, self.parm)
        return outstr
    
    def contents(self):
        return { self.name : self.parm }

class ThreeFloatParameter(Parameter):
    """ Generic class for three-float parameter """
    def __init__(self):
        self.xfloat = None
        self.yfloat = None
        self.zfloat = None
    
    def parse(self, tokens):
        self.xfloat = float(tokens.pop(0))
        self.yfloat = float(tokens.pop(0))
        self.zfloat = float(tokens.pop(0))
    
    def validate(self):
        # Validation happens through parsing
        pass
    
    def __str__(self):
        outstr = "%s %g %g %g" % (self.name, self.xfloat, self.yfloat, self.zfloat)
        return outstr
    
    def contents(self):
        return { "xfloat" : xfloat, "yfloat" : yfloat, "zfloat" : zfloat }

class ThreeIntegerParameter(Parameter):
    """ Generic class for three-int parameter """
    def __init__(self):
        self.xint = None
        self.yint = None
        self.zint = None
    
    def parse(self, tokens):
        self.xint = int(tokens.pop(0))
        self.yint = int(tokens.pop(0))
        self.zint = int(tokens.pop(0))
    
    def validate(self):
        # Validation happens through parsing
        pass
    
    def __str__(self):
        outstr = "%s %d %d %d" % (self.name, self.xint, self.yint, self.zint)
        return outstr
    
    def contents(self):
        return { "xint" : xint, "yint" : yint, "zint" : zint }

class FormatPathParameter(Parameter):
    """ Generic READ statement with format and path """
    def __init__(self):
        self.format = None
        self.path = None
    
    def contents(self):
        return { "format" : self.format, "path" : self.path }

    def parse(self, tokens):
        self.format = tokens.pop(0)
        path = "\"%s\"" % tokens.pop(0)
        self.path = path
    
    def validate(self):
        if not self.format in self.allowed_values:
            errstr = "Unknown token %s in %s" % (self.format, self.name)
            raise ValueError, errstr

    def __str__(self):
        return " ".join([self.name, self.format, self.path])