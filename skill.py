class Skill:
    def __init__(self, name, description, value, eg, number):
        self.name = name
        self.description = description
        self.value = value
        self.eg = eg
        self.number = number

class FloorSkill(Skill):
    def __init__(self, name, description, value, eg, number, isConnected, strengthElement, circleElement, oneLegBalance, doubleSalto):
        super().__init__(name, description, value, eg, number)
        self.isConnected = isConnected
        self.strengthElement = strengthElement
        self.circleElement = circleElement
        self.oneLegBalance = oneLegBalance
        self.doubleSalto = doubleSalto

class PommelSkill(Skill):
    def __init__(self, name, description, value, eg, number, fullSpindle, fullSpindleTravels, fullCrossSupTravels, fullRussianTravels):
        super().__init__(name, description, value, eg, number)
        self.fullSpindle = fullSpindle
        self.fullSpindleTravels = fullSpindleTravels
        self.fullCrossSupTravels = fullCrossSupTravels
        self.fullRussianTravels = fullRussianTravels

class RingsSkill(Skill):
    def __init__(self, name, description, value, eg, number, swingToHS, strengthShape):
        super().__init__(name, description, value, eg, number)
        self.swingToHS = swingToHS
        self.strengthShape = strengthShape

class PbarsSkill(Skill):
    def __init__(self, name, description, value, eg, number, fwdUprise, giantSwing, felgeSwing):
        super().__init__(name, description, value, eg, number)
        self.fwdUprise = fwdUprise
        self.giantSwing = giantSwing
        self.felgeSwing = felgeSwing
    
class HbarSkill(Skill):
    def __init__(self, name, description, value, number, eg, adlerType):
        super().__init__(name, description, value, number, eg)
        self.adlerType = adlerType