#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math


class Thornthwaite(object):
    """
    Método empírico baseado apenas na temperatura média do ar,
    sendo esta sua principal vantagem. Foi desenvolvido para condições
    de clima úmido e, por isso, normalmente apresenta sub-estimativa
    da ETP em condições de clima seco. Apesar dessa limitação, é um
    método bastante empregado para fins climatológicos, na escala
    mensal. Esse método parte de uma ET padrão (ETp),
    a qual é a ET para um mês de 30 dias e com N = 12h.
    """

    def __init__(self, avg_temp, photoperiod, n_days,
                 avg_anual_temp):
        try:
            self.avg_temp = float(avg_temp)
            self.photoperiod = float(photoperiod)
            self.n_days = self.period_validation(n_days)
            self.avg_anual_temp = float(avg_anual_temp)
        except Exception as e:
            print("Error: %s" % e)

        self.__temp_max_etp = 26.5

    @staticmethod
    def period_validation(period):
        """
        Funcao para validar quantidade de dias maximo e minimo
        dentro de um mes.
        """
        if int(period) >= 1 and int(period) <= 31:
            return period
        else:
            raise Exception('Periodo tem que ser maior que 1 e menor \
                            que 31')

    def temp_etp(self):
        """
        Funcao para retornar o tipo de calculo ETP.
        """
        if self.avg_temp >= 0 and self.avg_temp <= self.__temp_max_etp:
            return True
        else:
            return False

    def I(self):
        return round(12 * math.pow((0.2 * self.avg_anual_temp), 1.514), 2)

    def A(self, i):
        return round(0.49239 + (1.7912 * (math.pow(10, -2) * i)) \
                   - (7.71 * (math.pow(10, -5) * math.pow(i, 2))) \
                   + (6.75 * (math.pow(10, -7) * math.pow(i, 3))), 2)

    def cor(self):
        return round(self.photoperiod / 12.0 * \
                     self.n_days / 30.0, 2)

    def ETp(self):
        i = self.I()
        a = self.A(i)
        if self.temp_etp():
            return round(16 * math.pow((10 * self.avg_temp / i), a), 2)
        else:
            return round(-415.85 + ((32.24 * self.avg_temp) - \
                                    (0.43 * math.pow(self.avg_temp, 2))), 2)

    def ETP(self):
        """ Funcao que retorna ETP por mes"""
        cor = self.cor()
        ETp = self.ETp()
        return round(cor * ETp, 2)

    def ETPDia(self):
        """ Funcao que retorna ETP por dia"""
        cor = self.cor()
        ETp = self.ETp()
        return round((cor * ETp) / self.n_days, 2)

    def __str__(self):
        return "%.2f mm/mes - %.2f mm/dia" % (self.ETP(), self.ETPDia())


class ThornthwaiteCamargo(Thornthwaite):
    """
    É o método de Thornthwaite, porém adaptado por Camargo et al.
    (1999) para ser empregado em qualquer condição climática.
    Para tanto, utiliza-se uma temperatura efetiva (Tef), que expressa
    a amplitude térmica local, ao invés da temperatura média do ar. A
    vantagem é que nessa nova formulação a ETP não é mais subestimada
    em condições de clima seco. A desvantagem é que há agora necessidade
    de dados de Tmax e Tmin. Assim como no método original de Thornthwaite,
    esse método parte de uma ET padrão (ETp), a qual é a ET para um mês
    de 30 dias e com N = 12h
    """


    def __init__(self, temp_max, temp_min, photoperiod, n_days,
                 avg_anual_temp):
        try:
            self.tef = self.calculate_tef(temp_max, temp_min)
        except Exception as e:
            print("Error: %s" % e)

        Thornthwaite.__init__(self, self.tef, photoperiod, n_days,
                              avg_anual_temp)


    def calculate_tef(self, t_max, t_min):
        """ Funcao para calcular Temperatura Efetiva"""
        if t_max > t_min:
            return round(0.36 * (3 * t_max - t_min), 2)
        else:
            raise AttributeError('Temperatura maxima tem que ser maior que a minima.')


if __name__ == '__main__':
    test = Thornthwaite(24.4, 13.4, 31, 21.1)
    print("Thornthwaite: \t\t", test)
    test2 = ThornthwaiteCamargo(10, 13, 10.6, 31, 21.1)
    print("Thornthwaite Camargo: \t", test2)
