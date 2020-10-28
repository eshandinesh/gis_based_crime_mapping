import skfuzzy as fuzz
import numpy as np
from skfuzzy import control as ctrl


class FuzzyController:
    rule1 = None
    rule2 = None
    rule3 = None
    rule4 = None
    rule5 = None
    rule6 = None
    rule7 = None
    rule8 = None
    rule9 = None
    rule10 = None
    rule11 = None
    rule12 = None
    rule13 = None
    rule14 = None
    rule15 = None
    rule16 = None
    rule17 = None
    rule18 = None
    rule19 = None
    rule20 = None
    rule21 = None
    rule22 = None
    rule23 = None
    rule24 = None
    rule25 = None
    rule26 = None
    rule27 = None
    rule28 = None
    rule29 = None
    rule30 = None
    rule31 = None
    rule32 = None
    rule33 = None
    rule34 = None
    rule35 = None
    rule36 = None
    rule37 = None
    rule38 = None
    rule39 = None
    rule40 = None
    rule41 = None
    rule42 = None
    rule43 = None
    rule44 = None
    rule45 = None
    rule46 = None
    rule47 = None
    rule48 = None
    rule49 = None
    rule50 = None
    rule51 = None
    rule52 = None
    rule53 = None
    rule54 = None
    rule55 = None
    rule56 = None
    rule57 = None
    rule58 = None
    rule59 = None
    rule60 = None
    rule61 = None
    rule62 = None
    rule63 = None
    rule64 = None
    rule65 = None
    rule66 = None
    rule67 = None
    rule68 = None
    rule69 = None
    rule70 = None
    rule71 = None
    rule72 = None
    rule73 = None
    rule74 = None
    rule75 = None
    rule76 = None
    rule77 = None
    rule78 = None
    rule79 = None
    rule80 = None
    rule81 = None
    rule82 = None
    rule83 = None
    rule84 = None
    rule85 = None
    rule86 = None
    rule87 = None
    rule88 = None
    rule89 = None
    rule90 = None
    rule91 = None
    rule92 = None
    rule93 = None
    rule94 = None
    rule95 = None
    rule96 = None
    rule97 = None
    rule98 = None
    rule99 = None
    rule100 = None
    rule101 = None
    rule102 = None
    rule103 = None
    rule104 = None
    rule105 = None
    rule106 = None
    rule107 = None
    rule108 = None
    rule109 = None
    rule110 = None
    rule111 = None
    rule112 = None
    rule113 = None
    rule114 = None
    rule115 = None
    rule116 = None
    rule117 = None
    rule118 = None
    rule119 = None
    rule120 = None
    rule121 = None
    rule122 = None
    rule123 = None
    rule124 = None
    rule125 = None

    slope_scale_degree = None
    aspect_scale_degree = None
    elevation_meter = None
    susceptibility_rule = None
    susceptibility = None

    def __init__(self):
        self.slope_scale_degree = ctrl.Antecedent(np.arange(0, 90, 0.01), 'Slope')
        self.aspect_scale_degree = ctrl.Antecedent(np.arange(0, 359, 0.01), 'Aspect')
        self.elevation_meter = ctrl.Antecedent(np.arange(-1024, 6500, 0.01), 'Elevation')
        self.susceptibility = ctrl.Consequent(np.arange(0, 100, 0.01), 'Susceptibility')
        self.membership_functions_slope()
        self.membership_function_aspect()
        self.membership_function_elevation()
        self.membership_function_susceptibility()
        print ('rule base start')
        self.rulebase()
        self.addRule()

    def membership_functions_slope(self):
        self.slope_scale_degree['very unimportant'] = fuzz.trapmf(self.slope_scale_degree.universe, [-5, 0, 5, 10])
        self.slope_scale_degree['unimportant'] = fuzz.trapmf(self.slope_scale_degree.universe, [8, 15, 25, 30])
        self.slope_scale_degree['important'] = fuzz.trapmf(self.slope_scale_degree.universe, [25, 30, 40, 45])
        self.slope_scale_degree['very important'] = fuzz.trapmf(self.slope_scale_degree.universe, [40, 45, 55, 65])
        self.slope_scale_degree['extremely important'] = fuzz.trapmf(self.slope_scale_degree.universe, [60, 70, 90, 90])

    def membership_function_aspect(self):
        self.aspect_scale_degree['very unimportant'] = fuzz.trapmf(self.aspect_scale_degree.universe, [-1, 40, 60, 100])
        self.aspect_scale_degree['unimportant'] = fuzz.trapmf(self.aspect_scale_degree.universe, [50, 100, 150, 200])
        self.aspect_scale_degree['important'] = fuzz.trapmf(self.aspect_scale_degree.universe, [150, 200, 250, 300])
        self.aspect_scale_degree['very important'] = fuzz.trapmf(self.aspect_scale_degree.universe,
                                                                 [250, 280, 330, 359])
        self.aspect_scale_degree['extremely important'] = fuzz.trapmf(self.aspect_scale_degree.universe,
                                                                      [300, 330, 359, 359])

    def membership_function_elevation(self):
        self.elevation_meter['extremely important'] = fuzz.trapmf(self.elevation_meter.universe,
                                                                         [4000, 5000, 6500, 6500])
        self.elevation_meter['very important'] = fuzz.trapmf(self.elevation_meter.universe,
                                                                    [1000, 2000, 3500, 5000])
        self.elevation_meter['important'] = fuzz.trapmf(self.elevation_meter.universe,
                                                                  [600, 1000, 1500, 2000])
        self.elevation_meter['unimportant'] = fuzz.trapmf(self.elevation_meter.universe,
                                                                       [200, 350, 600, 1000])
        self.elevation_meter['very unimportant'] = fuzz.trapmf(self.elevation_meter.universe,
                                                                            [-1024, -1024, 300, 350])

    def membership_function_susceptibility(self):
        self.susceptibility['Very Low'] = fuzz.trapmf(self.susceptibility.universe, [0, 0, 10, 20])
        self.susceptibility['Low'] = fuzz.trapmf(self.susceptibility.universe, [15, 20, 25, 30])
        self.susceptibility['Medium'] = fuzz.trapmf(self.susceptibility.universe, [25, 35, 45, 50])
        self.susceptibility['High'] = fuzz.trapmf(self.susceptibility.universe, [40, 50, 60, 80])
        self.susceptibility['Very High'] = fuzz.trapmf(self.susceptibility.universe, [70, 80, 100, 100])

    def rulebase(self):
        self.rule1 = ctrl.Rule(
            self.slope_scale_degree['very unimportant'] & self.aspect_scale_degree['very unimportant'] &
            self.elevation_meter['very unimportant'], self.susceptibility['Very Low'])
        self.rule2 = ctrl.Rule(
            self.slope_scale_degree['very unimportant'] & self.aspect_scale_degree['very unimportant'] &
            self.elevation_meter['unimportant'], self.susceptibility['Low'])
        self.rule3 = ctrl.Rule(
            self.slope_scale_degree['very unimportant'] & self.aspect_scale_degree['very unimportant'] &
            self.elevation_meter['important'], self.susceptibility['Medium'])
        self.rule4 = ctrl.Rule(
            self.slope_scale_degree['very unimportant'] & self.aspect_scale_degree['very unimportant'] &
            self.elevation_meter['very important'], self.susceptibility['High'])
        self.rule5 = ctrl.Rule(
            self.slope_scale_degree['very unimportant'] & self.aspect_scale_degree['very unimportant'] &
            self.elevation_meter['extremely important'], self.susceptibility['Very High'])
        self.rule6 = ctrl.Rule(self.slope_scale_degree['very unimportant'] & self.aspect_scale_degree['unimportant'] &
                               self.elevation_meter['very unimportant'], self.susceptibility['Very Low'])
        self.rule7 = ctrl.Rule(self.slope_scale_degree['very unimportant'] & self.aspect_scale_degree['unimportant'] &
                               self.elevation_meter['unimportant'], self.susceptibility['Low'])
        self.rule8 = ctrl.Rule(self.slope_scale_degree['very unimportant'] & self.aspect_scale_degree['unimportant'] &
                               self.elevation_meter['important'], self.susceptibility['Medium'])
        self.rule9 = ctrl.Rule(self.slope_scale_degree['very unimportant'] & self.aspect_scale_degree['unimportant'] &
                               self.elevation_meter['very important'], self.susceptibility['High'])
        self.rule10 = ctrl.Rule(self.slope_scale_degree['very unimportant'] & self.aspect_scale_degree['unimportant'] &
                                self.elevation_meter['extremely important'], self.susceptibility['Very High'])
        self.rule11 = ctrl.Rule(
            self.slope_scale_degree['very unimportant'] & self.aspect_scale_degree['important'] & self.elevation_meter[
                'very unimportant'], self.susceptibility['Very Low'])
        self.rule12 = ctrl.Rule(
            self.slope_scale_degree['very unimportant'] & self.aspect_scale_degree['important'] & self.elevation_meter[
                'unimportant'], self.susceptibility['Low'])
        self.rule13 = ctrl.Rule(
            self.slope_scale_degree['very unimportant'] & self.aspect_scale_degree['important'] & self.elevation_meter[
                'important'], self.susceptibility['Medium'])
        self.rule14 = ctrl.Rule(
            self.slope_scale_degree['very unimportant'] & self.aspect_scale_degree['important'] & self.elevation_meter[
                'very important'], self.susceptibility['High'])
        self.rule15 = ctrl.Rule(
            self.slope_scale_degree['very unimportant'] & self.aspect_scale_degree['important'] & self.elevation_meter[
                'extremely important'], self.susceptibility['Very High'])
        self.rule16 = ctrl.Rule(
            self.slope_scale_degree['very unimportant'] & self.aspect_scale_degree['very important'] &
            self.elevation_meter['very unimportant'], self.susceptibility['Very Low'])
        self.rule17 = ctrl.Rule(
            self.slope_scale_degree['very unimportant'] & self.aspect_scale_degree['very important'] &
            self.elevation_meter['unimportant'], self.susceptibility['Low'])
        self.rule18 = ctrl.Rule(
            self.slope_scale_degree['very unimportant'] & self.aspect_scale_degree['very important'] &
            self.elevation_meter['important'], self.susceptibility['Medium'])
        self.rule19 = ctrl.Rule(
            self.slope_scale_degree['very unimportant'] & self.aspect_scale_degree['very important'] &
            self.elevation_meter['very important'], self.susceptibility['High'])
        self.rule20 = ctrl.Rule(
            self.slope_scale_degree['very unimportant'] & self.aspect_scale_degree['very important'] &
            self.elevation_meter['extremely important'], self.susceptibility['Very High'])
        self.rule21 = ctrl.Rule(
            self.slope_scale_degree['very unimportant'] & self.aspect_scale_degree['extremely important'] &
            self.elevation_meter['very unimportant'], self.susceptibility['Very Low'])
        self.rule22 = ctrl.Rule(
            self.slope_scale_degree['very unimportant'] & self.aspect_scale_degree['extremely important'] &
            self.elevation_meter['unimportant'], self.susceptibility['Low'])
        self.rule23 = ctrl.Rule(
            self.slope_scale_degree['very unimportant'] & self.aspect_scale_degree['extremely important'] &
            self.elevation_meter['important'], self.susceptibility['Medium'])
        self.rule24 = ctrl.Rule(
            self.slope_scale_degree['very unimportant'] & self.aspect_scale_degree['extremely important'] &
            self.elevation_meter['very important'], self.susceptibility['High'])
        self.rule25 = ctrl.Rule(
            self.slope_scale_degree['very unimportant'] & self.aspect_scale_degree['extremely important'] &
            self.elevation_meter['extremely important'], self.susceptibility['Very High'])
        self.rule26 = ctrl.Rule(self.slope_scale_degree['unimportant'] & self.aspect_scale_degree['very unimportant'] &
                                self.elevation_meter['very unimportant'], self.susceptibility['Very Low'])
        self.rule27 = ctrl.Rule(self.slope_scale_degree['unimportant'] & self.aspect_scale_degree['very unimportant'] &
                                self.elevation_meter['unimportant'], self.susceptibility['Low'])
        self.rule28 = ctrl.Rule(self.slope_scale_degree['unimportant'] & self.aspect_scale_degree['very unimportant'] &
                                self.elevation_meter['important'], self.susceptibility['Medium'])
        self.rule29 = ctrl.Rule(self.slope_scale_degree['unimportant'] & self.aspect_scale_degree['very unimportant'] &
                                self.elevation_meter['very important'], self.susceptibility['High'])
        self.rule30 = ctrl.Rule(self.slope_scale_degree['unimportant'] & self.aspect_scale_degree['very unimportant'] &
                                self.elevation_meter['extremely important'], self.susceptibility['Very High'])
        self.rule31 = ctrl.Rule(
            self.slope_scale_degree['unimportant'] & self.aspect_scale_degree['unimportant'] & self.elevation_meter[
                'very unimportant'], self.susceptibility['Very Low'])
        self.rule32 = ctrl.Rule(
            self.slope_scale_degree['unimportant'] & self.aspect_scale_degree['unimportant'] & self.elevation_meter[
                'unimportant'], self.susceptibility['Low'])
        self.rule33 = ctrl.Rule(
            self.slope_scale_degree['unimportant'] & self.aspect_scale_degree['unimportant'] & self.elevation_meter[
                'important'], self.susceptibility['Medium'])
        self.rule34 = ctrl.Rule(
            self.slope_scale_degree['unimportant'] & self.aspect_scale_degree['unimportant'] & self.elevation_meter[
                'very important'], self.susceptibility['High'])
        self.rule35 = ctrl.Rule(
            self.slope_scale_degree['unimportant'] & self.aspect_scale_degree['unimportant'] & self.elevation_meter[
                'extremely important'], self.susceptibility['Very High'])
        self.rule36 = ctrl.Rule(
            self.slope_scale_degree['unimportant'] & self.aspect_scale_degree['important'] & self.elevation_meter[
                'very unimportant'], self.susceptibility['Very Low'])
        self.rule37 = ctrl.Rule(
            self.slope_scale_degree['unimportant'] & self.aspect_scale_degree['important'] & self.elevation_meter[
                'unimportant'], self.susceptibility['Low'])
        self.rule38 = ctrl.Rule(
            self.slope_scale_degree['unimportant'] & self.aspect_scale_degree['important'] & self.elevation_meter[
                'important'], self.susceptibility['Medium'])
        self.rule39 = ctrl.Rule(
            self.slope_scale_degree['unimportant'] & self.aspect_scale_degree['important'] & self.elevation_meter[
                'very important'], self.susceptibility['High'])
        self.rule40 = ctrl.Rule(
            self.slope_scale_degree['unimportant'] & self.aspect_scale_degree['important'] & self.elevation_meter[
                'extremely important'], self.susceptibility['Very High'])
        self.rule41 = ctrl.Rule(
            self.slope_scale_degree['unimportant'] & self.aspect_scale_degree['very important'] & self.elevation_meter[
                'very unimportant'], self.susceptibility['Very Low'])
        self.rule42 = ctrl.Rule(
            self.slope_scale_degree['unimportant'] & self.aspect_scale_degree['very important'] & self.elevation_meter[
                'unimportant'], self.susceptibility['Low'])
        self.rule43 = ctrl.Rule(
            self.slope_scale_degree['unimportant'] & self.aspect_scale_degree['very important'] & self.elevation_meter[
                'important'], self.susceptibility['Medium'])
        self.rule44 = ctrl.Rule(
            self.slope_scale_degree['unimportant'] & self.aspect_scale_degree['very important'] & self.elevation_meter[
                'very important'], self.susceptibility['High'])
        self.rule45 = ctrl.Rule(
            self.slope_scale_degree['unimportant'] & self.aspect_scale_degree['very important'] & self.elevation_meter[
                'extremely important'], self.susceptibility['Very High'])
        self.rule46 = ctrl.Rule(
            self.slope_scale_degree['unimportant'] & self.aspect_scale_degree['extremely important'] &
            self.elevation_meter['very unimportant'], self.susceptibility['Very Low'])
        self.rule47 = ctrl.Rule(
            self.slope_scale_degree['unimportant'] & self.aspect_scale_degree['extremely important'] &
            self.elevation_meter['unimportant'], self.susceptibility['Low'])
        self.rule48 = ctrl.Rule(
            self.slope_scale_degree['unimportant'] & self.aspect_scale_degree['extremely important'] &
            self.elevation_meter['important'], self.susceptibility['Medium'])
        self.rule49 = ctrl.Rule(
            self.slope_scale_degree['unimportant'] & self.aspect_scale_degree['extremely important'] &
            self.elevation_meter['very important'], self.susceptibility['High'])
        self.rule50 = ctrl.Rule(
            self.slope_scale_degree['unimportant'] & self.aspect_scale_degree['extremely important'] &
            self.elevation_meter['extremely important'], self.susceptibility['Very High'])
        self.rule51 = ctrl.Rule(
            self.slope_scale_degree['important'] & self.aspect_scale_degree['very unimportant'] & self.elevation_meter[
                'very unimportant'], self.susceptibility['Very Low'])
        self.rule52 = ctrl.Rule(
            self.slope_scale_degree['important'] & self.aspect_scale_degree['very unimportant'] & self.elevation_meter[
                'unimportant'], self.susceptibility['Low'])
        self.rule53 = ctrl.Rule(
            self.slope_scale_degree['important'] & self.aspect_scale_degree['very unimportant'] & self.elevation_meter[
                'important'], self.susceptibility['Medium'])
        self.rule54 = ctrl.Rule(
            self.slope_scale_degree['important'] & self.aspect_scale_degree['very unimportant'] & self.elevation_meter[
                'very important'], self.susceptibility['High'])
        self.rule55 = ctrl.Rule(
            self.slope_scale_degree['important'] & self.aspect_scale_degree['very unimportant'] & self.elevation_meter[
                'extremely important'], self.susceptibility['Very High'])
        self.rule56 = ctrl.Rule(
            self.slope_scale_degree['important'] & self.aspect_scale_degree['unimportant'] & self.elevation_meter[
                'very unimportant'], self.susceptibility['Very Low'])
        self.rule57 = ctrl.Rule(
            self.slope_scale_degree['important'] & self.aspect_scale_degree['unimportant'] & self.elevation_meter[
                'unimportant'], self.susceptibility['Low'])
        self.rule58 = ctrl.Rule(
            self.slope_scale_degree['important'] & self.aspect_scale_degree['unimportant'] & self.elevation_meter[
                'important'], self.susceptibility['Medium'])
        self.rule59 = ctrl.Rule(
            self.slope_scale_degree['important'] & self.aspect_scale_degree['unimportant'] & self.elevation_meter[
                'very important'], self.susceptibility['High'])
        self.rule60 = ctrl.Rule(
            self.slope_scale_degree['important'] & self.aspect_scale_degree['unimportant'] & self.elevation_meter[
                'extremely important'], self.susceptibility['Very High'])
        self.rule61 = ctrl.Rule(
            self.slope_scale_degree['important'] & self.aspect_scale_degree['important'] & self.elevation_meter[
                'very unimportant'], self.susceptibility['Very Low'])
        self.rule62 = ctrl.Rule(
            self.slope_scale_degree['important'] & self.aspect_scale_degree['important'] & self.elevation_meter[
                'unimportant'], self.susceptibility['Low'])
        self.rule63 = ctrl.Rule(
            self.slope_scale_degree['important'] & self.aspect_scale_degree['important'] & self.elevation_meter[
                'important'], self.susceptibility['Medium'])
        self.rule64 = ctrl.Rule(
            self.slope_scale_degree['important'] & self.aspect_scale_degree['important'] & self.elevation_meter[
                'very important'], self.susceptibility['High'])
        self.rule65 = ctrl.Rule(
            self.slope_scale_degree['important'] & self.aspect_scale_degree['important'] & self.elevation_meter[
                'extremely important'], self.susceptibility['Very High'])
        self.rule66 = ctrl.Rule(
            self.slope_scale_degree['important'] & self.aspect_scale_degree['very important'] & self.elevation_meter[
                'very unimportant'], self.susceptibility['Very Low'])
        self.rule67 = ctrl.Rule(
            self.slope_scale_degree['important'] & self.aspect_scale_degree['very important'] & self.elevation_meter[
                'unimportant'], self.susceptibility['Low'])
        self.rule68 = ctrl.Rule(
            self.slope_scale_degree['important'] & self.aspect_scale_degree['very important'] & self.elevation_meter[
                'important'], self.susceptibility['Medium'])
        self.rule69 = ctrl.Rule(
            self.slope_scale_degree['important'] & self.aspect_scale_degree['very important'] & self.elevation_meter[
                'very important'], self.susceptibility['High'])
        self.rule70 = ctrl.Rule(
            self.slope_scale_degree['important'] & self.aspect_scale_degree['very important'] & self.elevation_meter[
                'extremely important'], self.susceptibility['Very High'])
        self.rule71 = ctrl.Rule(self.slope_scale_degree['important'] & self.aspect_scale_degree['extremely important'] &
                                self.elevation_meter['very unimportant'], self.susceptibility['Very Low'])
        self.rule72 = ctrl.Rule(self.slope_scale_degree['important'] & self.aspect_scale_degree['extremely important'] &
                                self.elevation_meter['unimportant'], self.susceptibility['Low'])
        self.rule73 = ctrl.Rule(self.slope_scale_degree['important'] & self.aspect_scale_degree['extremely important'] &
                                self.elevation_meter['important'], self.susceptibility['Medium'])
        self.rule74 = ctrl.Rule(self.slope_scale_degree['important'] & self.aspect_scale_degree['extremely important'] &
                                self.elevation_meter['very important'], self.susceptibility['High'])
        self.rule75 = ctrl.Rule(self.slope_scale_degree['important'] & self.aspect_scale_degree['extremely important'] &
                                self.elevation_meter['extremely important'], self.susceptibility['Very High'])
        self.rule76 = ctrl.Rule(
            self.slope_scale_degree['very important'] & self.aspect_scale_degree['very unimportant'] &
            self.elevation_meter['very unimportant'], self.susceptibility['Very Low'])
        self.rule77 = ctrl.Rule(
            self.slope_scale_degree['very important'] & self.aspect_scale_degree['very unimportant'] &
            self.elevation_meter['unimportant'], self.susceptibility['Low'])
        self.rule78 = ctrl.Rule(
            self.slope_scale_degree['very important'] & self.aspect_scale_degree['very unimportant'] &
            self.elevation_meter['important'], self.susceptibility['Medium'])
        self.rule79 = ctrl.Rule(
            self.slope_scale_degree['very important'] & self.aspect_scale_degree['very unimportant'] &
            self.elevation_meter['very important'], self.susceptibility['High'])
        self.rule80 = ctrl.Rule(
            self.slope_scale_degree['very important'] & self.aspect_scale_degree['very unimportant'] &
            self.elevation_meter['extremely important'], self.susceptibility['Very High'])
        self.rule81 = ctrl.Rule(
            self.slope_scale_degree['very important'] & self.aspect_scale_degree['unimportant'] & self.elevation_meter[
                'very unimportant'], self.susceptibility['Very Low'])
        self.rule82 = ctrl.Rule(
            self.slope_scale_degree['very important'] & self.aspect_scale_degree['unimportant'] & self.elevation_meter[
                'unimportant'], self.susceptibility['Low'])
        self.rule83 = ctrl.Rule(
            self.slope_scale_degree['very important'] & self.aspect_scale_degree['unimportant'] & self.elevation_meter[
                'important'], self.susceptibility['Medium'])
        self.rule84 = ctrl.Rule(
            self.slope_scale_degree['very important'] & self.aspect_scale_degree['unimportant'] & self.elevation_meter[
                'very important'], self.susceptibility['High'])
        self.rule85 = ctrl.Rule(
            self.slope_scale_degree['very important'] & self.aspect_scale_degree['unimportant'] & self.elevation_meter[
                'extremely important'], self.susceptibility['Very High'])
        self.rule86 = ctrl.Rule(
            self.slope_scale_degree['very important'] & self.aspect_scale_degree['important'] & self.elevation_meter[
                'very unimportant'], self.susceptibility['Very Low'])
        self.rule87 = ctrl.Rule(
            self.slope_scale_degree['very important'] & self.aspect_scale_degree['important'] & self.elevation_meter[
                'unimportant'], self.susceptibility['Low'])
        self.rule88 = ctrl.Rule(
            self.slope_scale_degree['very important'] & self.aspect_scale_degree['important'] & self.elevation_meter[
                'important'], self.susceptibility['Medium'])
        self.rule89 = ctrl.Rule(
            self.slope_scale_degree['very important'] & self.aspect_scale_degree['important'] & self.elevation_meter[
                'very important'], self.susceptibility['High'])
        self.rule90 = ctrl.Rule(
            self.slope_scale_degree['very important'] & self.aspect_scale_degree['important'] & self.elevation_meter[
                'extremely important'], self.susceptibility['Very High'])
        self.rule91 = ctrl.Rule(self.slope_scale_degree['very important'] & self.aspect_scale_degree['very important'] &
                                self.elevation_meter['very unimportant'], self.susceptibility['Very Low'])
        self.rule92 = ctrl.Rule(self.slope_scale_degree['very important'] & self.aspect_scale_degree['very important'] &
                                self.elevation_meter['unimportant'], self.susceptibility['Low'])
        self.rule93 = ctrl.Rule(self.slope_scale_degree['very important'] & self.aspect_scale_degree['very important'] &
                                self.elevation_meter['important'], self.susceptibility['Medium'])
        self.rule94 = ctrl.Rule(self.slope_scale_degree['very important'] & self.aspect_scale_degree['very important'] &
                                self.elevation_meter['very important'], self.susceptibility['High'])
        self.rule95 = ctrl.Rule(self.slope_scale_degree['very important'] & self.aspect_scale_degree['very important'] &
                                self.elevation_meter['extremely important'], self.susceptibility['Very High'])
        self.rule96 = ctrl.Rule(
            self.slope_scale_degree['very important'] & self.aspect_scale_degree['extremely important'] &
            self.elevation_meter['very unimportant'], self.susceptibility['Very Low'])
        self.rule97 = ctrl.Rule(
            self.slope_scale_degree['very important'] & self.aspect_scale_degree['extremely important'] &
            self.elevation_meter['unimportant'], self.susceptibility['Low'])
        self.rule98 = ctrl.Rule(
            self.slope_scale_degree['very important'] & self.aspect_scale_degree['extremely important'] &
            self.elevation_meter['important'], self.susceptibility['Medium'])
        self.rule99 = ctrl.Rule(
            self.slope_scale_degree['very important'] & self.aspect_scale_degree['extremely important'] &
            self.elevation_meter['very important'], self.susceptibility['High'])
        self.rule100 = ctrl.Rule(
            self.slope_scale_degree['very important'] & self.aspect_scale_degree['extremely important'] &
            self.elevation_meter['extremely important'], self.susceptibility['Very High'])
        self.rule101 = ctrl.Rule(
            self.slope_scale_degree['extremely important'] & self.aspect_scale_degree['very unimportant'] &
            self.elevation_meter['very unimportant'], self.susceptibility['Very Low'])
        self.rule102 = ctrl.Rule(
            self.slope_scale_degree['extremely important'] & self.aspect_scale_degree['very unimportant'] &
            self.elevation_meter['unimportant'], self.susceptibility['Low'])
        self.rule103 = ctrl.Rule(
            self.slope_scale_degree['extremely important'] & self.aspect_scale_degree['very unimportant'] &
            self.elevation_meter['important'], self.susceptibility['Medium'])
        self.rule104 = ctrl.Rule(
            self.slope_scale_degree['extremely important'] & self.aspect_scale_degree['very unimportant'] &
            self.elevation_meter['very important'], self.susceptibility['High'])
        self.rule105 = ctrl.Rule(
            self.slope_scale_degree['extremely important'] & self.aspect_scale_degree['very unimportant'] &
            self.elevation_meter['extremely important'], self.susceptibility['Very High'])
        self.rule106 = ctrl.Rule(
            self.slope_scale_degree['extremely important'] & self.aspect_scale_degree['unimportant'] &
            self.elevation_meter['very unimportant'], self.susceptibility['Very Low'])
        self.rule107 = ctrl.Rule(
            self.slope_scale_degree['extremely important'] & self.aspect_scale_degree['unimportant'] &
            self.elevation_meter['unimportant'], self.susceptibility['Low'])
        self.rule108 = ctrl.Rule(
            self.slope_scale_degree['extremely important'] & self.aspect_scale_degree['unimportant'] &
            self.elevation_meter['important'], self.susceptibility['Medium'])
        self.rule109 = ctrl.Rule(
            self.slope_scale_degree['extremely important'] & self.aspect_scale_degree['unimportant'] &
            self.elevation_meter['very important'], self.susceptibility['High'])
        self.rule110 = ctrl.Rule(
            self.slope_scale_degree['extremely important'] & self.aspect_scale_degree['unimportant'] &
            self.elevation_meter['extremely important'], self.susceptibility['Very High'])
        self.rule111 = ctrl.Rule(
            self.slope_scale_degree['extremely important'] & self.aspect_scale_degree['important'] &
            self.elevation_meter['very unimportant'], self.susceptibility['Very Low'])
        self.rule112 = ctrl.Rule(
            self.slope_scale_degree['extremely important'] & self.aspect_scale_degree['important'] &
            self.elevation_meter['unimportant'], self.susceptibility['Low'])
        self.rule113 = ctrl.Rule(
            self.slope_scale_degree['extremely important'] & self.aspect_scale_degree['important'] &
            self.elevation_meter['important'], self.susceptibility['Medium'])
        self.rule114 = ctrl.Rule(
            self.slope_scale_degree['extremely important'] & self.aspect_scale_degree['important'] &
            self.elevation_meter['very important'], self.susceptibility['High'])
        self.rule115 = ctrl.Rule(
            self.slope_scale_degree['extremely important'] & self.aspect_scale_degree['important'] &
            self.elevation_meter['extremely important'], self.susceptibility['Very High'])
        self.rule116 = ctrl.Rule(
            self.slope_scale_degree['extremely important'] & self.aspect_scale_degree['very important'] &
            self.elevation_meter['very unimportant'], self.susceptibility['Very Low'])
        self.rule117 = ctrl.Rule(
            self.slope_scale_degree['extremely important'] & self.aspect_scale_degree['very important'] &
            self.elevation_meter['unimportant'], self.susceptibility['Low'])
        self.rule118 = ctrl.Rule(
            self.slope_scale_degree['extremely important'] & self.aspect_scale_degree['very important'] &
            self.elevation_meter['important'], self.susceptibility['Medium'])
        self.rule119 = ctrl.Rule(
            self.slope_scale_degree['extremely important'] & self.aspect_scale_degree['very important'] &
            self.elevation_meter['very important'], self.susceptibility['High'])
        self.rule120 = ctrl.Rule(
            self.slope_scale_degree['extremely important'] & self.aspect_scale_degree['very important'] &
            self.elevation_meter['extremely important'], self.susceptibility['Very High'])
        self.rule121 = ctrl.Rule(
            self.slope_scale_degree['extremely important'] & self.aspect_scale_degree['extremely important'] &
            self.elevation_meter['very unimportant'], self.susceptibility['Very Low'])
        self.rule122 = ctrl.Rule(
            self.slope_scale_degree['extremely important'] & self.aspect_scale_degree['extremely important'] &
            self.elevation_meter['unimportant'], self.susceptibility['Low'])
        self.rule123 = ctrl.Rule(
            self.slope_scale_degree['extremely important'] & self.aspect_scale_degree['extremely important'] &
            self.elevation_meter['important'], self.susceptibility['Medium'])
        self.rule124 = ctrl.Rule(
            self.slope_scale_degree['extremely important'] & self.aspect_scale_degree['extremely important'] &
            self.elevation_meter['very important'], self.susceptibility['High'])
        self.rule125 = ctrl.Rule(
            self.slope_scale_degree['extremely important'] & self.aspect_scale_degree['extremely important'] &
            self.elevation_meter['extremely important'], self.susceptibility['Very High'])

    def addRule(self):
        self.susceptibility_rule = ctrl.ControlSystem([self.rule1, self.rule2, self.rule3, self.rule4, self.rule5,
                                                  self.rule6, self.rule7, self.rule8, self.rule9, self.rule10,
                                                  self.rule11, self.rule12, self.rule13, self.rule14, self.rule15,
                                                  self.rule16, self.rule17, self.rule18, self.rule19, self.rule20,
                                                  self.rule21, self.rule22, self.rule23, self.rule24, self.rule25,
                                                  self.rule26, self.rule27, self.rule28, self.rule29, self.rule30,
                                                  self.rule31, self.rule32, self.rule33, self.rule34, self.rule35,
                                                  self.rule36, self.rule37, self.rule38, self.rule39, self.rule40,
                                                  self.rule41, self.rule42, self.rule43, self.rule44, self.rule45,
                                                  self.rule46, self.rule47, self.rule48, self.rule49, self.rule50,
                                                  self.rule51, self.rule52, self.rule53, self.rule54, self.rule55,
                                                  self.rule56, self.rule57, self.rule58, self.rule59, self.rule60,
                                                  self.rule61, self.rule62, self.rule63, self.rule64, self.rule65,
                                                  self.rule66, self.rule67, self.rule68, self.rule69, self.rule70,
                                                  self.rule71, self.rule72, self.rule73, self.rule74, self.rule75,
                                                  self.rule76, self.rule77, self.rule78, self.rule79, self.rule80,
                                                  self.rule81, self.rule82, self.rule83, self.rule84, self.rule85,
                                                  self.rule86, self.rule87, self.rule88, self.rule89, self.rule90,
                                                  self.rule91, self.rule92, self.rule93, self.rule94, self.rule95,
                                                  self.rule96, self.rule97, self.rule98, self.rule99, self.rule100,
                                                  self.rule101, self.rule102, self.rule103, self.rule104, self.rule105,
                                                  self.rule106, self.rule107, self.rule108, self.rule109, self.rule110,
                                                  self.rule111, self.rule112, self.rule113, self.rule114, self.rule115,
                                                  self.rule116, self.rule117, self.rule118, self.rule119, self.rule120,
                                                  self.rule121, self.rule122, self.rule123, self.rule124, self.rule125])

    def controller(self, slope, aspect, elevation):
        susceptible = ctrl.ControlSystemSimulation(self.susceptibility_rule)
        susceptible.input['Slope'] = slope
        susceptible.input['Aspect'] = aspect
        susceptible.input['Elevation'] = elevation

        susceptible.compute()

        print (susceptible.output['Susceptibility'])
        self.susceptibility.view(sim = susceptible)
        return susceptible.output['Susceptibility']
        #self.susceptibility.view(sim=susceptible)
        #defuzz_centroid = fuzz.defuzz(self.susceptibility, self.susceptibility, 'centroid')
        #print defuzz_centroid


if __name__ == '__main__':
    fc = FuzzyController()
    fc.controller(5, 50, 100)  # sample with slope=5, aspect=50 and elevation =100
