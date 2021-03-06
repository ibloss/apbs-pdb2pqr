""" Parse the PRINT input file section """
from parameter import Parameter

class Print(Parameter):
    """ This is a very simple section that allows linear combinations of calculated properties to be
    written to standard output.
    
    The syntax of this section is
    
    PRINT {what} [id op id op...] END
    
    The first mandatory argument is what, the quantity to manipulate or print. This variable is a
    string that can assume the following values:

    * energy - Print energies as calculated with an earlier calcenergy ELEC command. Warning: this
    keyword is deprecated and will be removed soon. Please use elecEnergy or apolEnergy as
    appropriate to obtain the desired energy output. For now, use of this keyword will return the
    old results of elecEnergy.
    * force - Print forces as calculated with an earlier calcforce ELEC command. Warning: this
    keyword is deprecated and will be removed soon. Please use elecForce or apolForce as appropriate
    to obtain the desired energy output.
    * elecEnergy - Print electrostatic energies as calculated with an earlier calcenergy ELEC
    command.
    * elecForce - Print forces as calculated with an earlier calcforce ELEC command.
    * apolEnergy - Print energies as calculated with an earlier calcenergy APOLAR command.
    * apolForce - Print forces as calculated with an earlier calcforce APOLAR command.
    
    The next arguments are a series of id op id op id op ... id commands where every id is
    immediately followed by an op and another id. These options have the following form:

    * id - This is a variable string or integer denoting the ID of a particular ELEC or APOLAR
    calculation. String values of id are assume to correspond to the optional "names" that can be
    assigned to ELEC or APOLAR calculations. Integer values of id are assumed to corresponding to
    the sequentially-assigned integer IDs for ELEC or APOLAR calculations. These IDs start at 1 and
    are incremented independently for each new ELEC or AOPLAR calculation.
    * op - Specify the arithmetic operation to be performed on the calculated quantities:
        + Addition
        - Subtraction """
    allowed_what_values = ["elecenergy", "elecforce", "apolenergy", "apolforce"]
    allowed_op_values = ["+", "-"]
    def __init__(self):
        self.what = None
        self.ids = []
        self.ops = []
    
    @property
    def name(self):
        return "print"
    
    def parse(self, tokens):
        whatToken = tokens.pop(0).lower()
        self.what = whatToken
        calcID = int(tokens.pop(0))
        self.ids.append(calcID)
        while True:
            token = tokens.pop(0)
            if token == "end":
                return
            self.ops.append(token)
            calcID = int(tokens.pop(0))
            self.ids.append(calcID)
            
    def validate(self):
        if not self.what in self.allowed_what_values:
            errstr = "Unexpected token %s in PRINT" % self.what
            raise ValueError, errstr
        for op in self.ops:
            if not op in self.allowed_op_values:
                errstr = "Unexpected operator %s in PRINT" % op
                raise ValueError, op
    
    def __str__(self):
        outstr = "print %s " % self.what
        outstr = outstr + "%d " % self.ids[0]
        for iop, op in enumerate(self.ops):
            calcID = self.ids[iop+1]
            outstr = outstr + "%s %d " % (op, calcID)
        outstr = outstr + "end"
        return outstr
    
    def contents(self):
        return { "what" : self.what, "ops" : self.ops, "ids" : self.ids }