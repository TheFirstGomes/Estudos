from modelos.restaurante import Restaurante

restaurante_praca = Restaurante('praça', 'Gourmet')
restaurante_praca.receber_avaliacao('Guina', 10)
restaurante_praca.receber_avaliacao('Lala', 8)
restaurante_praca.receber_avaliacao('Flavio', 5)

def main():
    Restaurante.listar_restaurantes()

if __name__ == '__main__':
    main()