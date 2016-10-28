#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math

__author__ = 'joaotrevizoliesteves, Murilo Ijanc'
__copyright__ = "Copyright 2015, Lab804"
__license__ = "BSD"
__version__ = "0.1"


class LeafAreaIndexFix(object):
    """ Leaf Area Index Fix

    Correction of leaf area index based in the standard
    hypothetical crop of Wit(1965), brought to a real
    culture with max leaf index test

    :param: iaf: Maximum leaf area index(dimensionless)
    :type: iaf: int or float
    """
    def __init__(self, iaf):
        try:
            self.iaf = float(iaf)
        except Exception as e:
            print("Erro: %s" % e)

    def leaf_area_index_fix(self):
        """leaf area index calculated

        The value of the Wits leaf area index
        """
        leaf_fix = 0.0093 + 0.185 * self.iaf - 0.0175 * math.pow(self.iaf, 2)
        if leaf_fix > 5.0:
            leaf_fix = 5.0
        return leaf_fix
#