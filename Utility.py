class Auxcarrello():
    quantità = 0
    totale = 0

class Active():
    #index, shop, blog, contact
    pagine = [1, 0, 0, 0]

    def disattiva(self, active):
        for i in range(4):
            self.pagine[i] = 0
        self.pagine[active] = 1
pages = Active()

class SliderHelp():
    #mex, ordini_r, ordini_e, fatture_a, fatture_v, ddt, scontrini
    sliders = [0,0,0,0,0,0,0]

    def aggiorna(self, i, value):
        self.sliders[i] += int(value)
        if self.sliders[i] < 0:
            self.sliders[i] = 0

    def endSlied(self, i):
        return 10*(self.sliders[i] + 1)
help = SliderHelp()