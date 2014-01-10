import encodings.idna

class IDN(object):

    def __init__(self, input=None):

        self.alabel = None

        if input:
            self.assign(input)

    def assign(self, input):

        if isinstance(input, (list, tuple)):
            candidate = u''
            for codepoint in input:
                candidate += unichr(codepoint)
        else:
            candidate = input

        domain = encodings.idna.ToASCII(candidate)
        self.alabel = domain


    @property
    def ulabel(self):

        ulabel = encodings.idna.ToUnicode(self.alabel)
        return ulabel

    @property
    def codepoints(self):

        codepoints = []
        for character in self.ulabel:
            codepoints.append(ord(character))
        return codepoints

    def __len__(self):

        return len(self.alabel)

    def __unicode__(self):

        return self.ulabel

    def __str__(self):

        return self.alabel

    def __repr__(self):

        return "%s(\'%s\')" % (self.__class__.__name__, self.alabel)

