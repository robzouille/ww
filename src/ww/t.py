# TODO: anonymous namedtuple that can be created inline
# TODO: tuples can be either with names or not (but not both)

import ww


class t(tuple):
    @property
    def len(self):
        return len(self)

    def index(self, value):
        """
        Args:
            value: index

        Returns: index of the values

        Raises:
            ValueError: value is not in list
        """

        for i, x in enumerate(self):
            if x == value:
                return i

        raise ValueError("{} is not in list".format(value))

    def to_l(self):
        """
        Args: self

        Returns: a l that stems from self
        """
        return ww.l(self)

    def to_d(self):
        """
        Args: self

        Returns: a d that stems from self

        Raises:
            ValueError: dictionary update sequence element #index has length
            len(tuple); 2 is required

            TypeError: cannot convert dictionary update sequence element
            #index to a sequence
        """
        for i, x in enumerate(self):
            if type(x) == int:
                raise TypeError("cannot convert dictionary update sequence "
                                "element #{} to a sequence".format(i))
            elif len(x) != 2:
                raise ValueError(("dictionary update sequence element #{0} "
                                 "has length {1}; 2 is required")
                                 .format(i, len(x)))
        return ww.d(self)
