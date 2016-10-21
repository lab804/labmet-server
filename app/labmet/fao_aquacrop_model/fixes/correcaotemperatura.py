#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'joaotrevizoliesteves, Murilo Ijanc'
__copyright__ = "Copyright 2015, Lab804"
__license__ = "BSD"
__version__ = "0.1"

import math


class CTCIIIInverno(object):
    """
    Correção de temperatura de cultura, utilizada no
    calculo de produtividade potêncial, propostos por
    Barbieri & Tuon(1992) para culturas de inverno do
    tipo CIII.
    """
    def __init__(self, temperatura):
        try:
            self.temperatura = float(temperatura)
        except:
            raise

    def ctn(self):
        """
        Correção de temperatura para céu nublado
        """
        if 15.0 <= self.temperatura <= 20.0:
            return 0.7 + 0.0035 * self.temperatura - 0.001 * math.pow(self.temperatura, 2)
        else:
            return 0.25 + 0.0875 * self.temperatura - 0.0025 * math.pow(self.temperatura, 2)

    def ctc(self):
        """
        Correção de temperatura para céu claro
        """
        if 15.0 <= self.temperatura <= 20.0:
            return 0.25 + 0.0875 * self.temperatura - 0.0025 * math.pow(self.temperatura, 2)
        else:
            return -0.5 + 0.175 * self.temperatura - 0.005 * math.pow(self.temperatura, 2)


class CTCIIIVerao(CTCIIIInverno):
    """
    Correção de temperatura de cultura, utilizada no
    calculo de produtividade potêncial, propostos por
    Barbieri & Tuon(1992) para culturas de verão do
    tipo CIII.
    """
    def ctn(self):
        """
        Correção de temperatura para céu nublado
        """
        if 16.5 <= self.temperatura <= 37.0:
            return 0.583 + 0.014 * self.temperatura\
                   + 0.0013 * math.pow(self.temperatura, 2)\
                   - 0.000037 * math.pow(self.temperatura, 3)
        else:
            return -0.0425 + 0.035 * self.temperatura\
                   + 0.00325 * math.pow(self.temperatura, 2)\
                   - 0.0000925 * math.pow(self.temperatura, 3)

    def ctc(self):
        """
        Correção de temperatura para céu claro
        """
        if 16.5 <= self.temperatura <= 37.0:
            return -0.0425 + 0.035 * self.temperatura\
                   + 0.00325 * math.pow(self.temperatura, 2)\
                   - 0.0000925 * math.pow(self.temperatura, 3)
        else:
            return -1.085 + 0.07 * self.temperatura\
                   + 0.0065 * math.pow(self.temperatura, 2)\
                   - 0.000185 * math.pow(self.temperatura, 3)


class CTCIV(CTCIIIInverno):
    """
    Correção de temperatura de cultura, utilizada no
    calculo de produtividade potêncial, propostos por
    Barbieri & Tuon(1992) para culturas de verão do
    tipo CIV.
    """
    def ctn(self):
        """
        Correção de temperatura para céu nublado
        """
        if self.temperatura >= 16.5:
            return -1.064 + 0.173 * self.temperatura - 0.0029 * math.pow(self.temperatura, 2)
        else:
            return -4.16 + 0.4325 * self.temperatura - 0.00725 * math.pow(self.temperatura, 2)

    def ctc(self):
        """
        Correção de temperatura para céu claro
        """
        if self.temperatura < 16.5:
            return -4.16 + 0.4325 * self.temperatura - 0.00725 * math.pow(self.temperatura, 2)
        else:
            return -9.32 + 0.865 * self.temperatura - 0.0145 * math.pow(self.temperatura, 2)