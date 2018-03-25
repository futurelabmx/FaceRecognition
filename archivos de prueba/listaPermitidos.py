class flabianos:
    """ Lista de invitados a la cena del señor en el laboratorio """

    def __init__(self):
        self.Invitados=['Luis Sustaita','Ricardo Mirón Torres',
               'Aldo Fernando Olmeda','Paco López Ortiz','Oliver A. López',
               'MD Diaz','Cristofer Nava','Miguel Aguirre','Polo A. Ruiz','Rodolfo Ferro','Christian Oveth Alba Cisneros']

    def TuSiTuNo(self,EllosSi):
        for person in EllosSi:
            if person in self.Invitados:
                print('Bienvenido {}'.format(person))
            else:
                print('Lo siento, aun no trais el omnitrix')
