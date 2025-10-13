from modelos.avaliacao import Avaliacao

class Restaurante: 
    restaurantes = []

    def __init__(self, nome, categoria):
        self._nome = nome.title()
        self._categoria = categoria.upper()
        self._ativo = False
        self._avaliacao = []
        Restaurante.restaurantes.append(self)

    def __str__(self):
        return f'{self._nome} | {self._categoria} | {self._ativo}'

    @classmethod 
    def listar_restaurantes(cls):
        print(f'\n{'Nome do restaurante'.ljust(25)} | {'Categoria'.ljust(25)} | {'Status'}\n')
        for restaurante in cls.restaurantes:
            print(f'{restaurante._nome.ljust(25)} | {restaurante._categoria.ljust(25)} | {restaurante.ativo}') 
    
    @property
    def ativo(self):
        return '⌧' if self._ativo else '☐'
    
    def alternar_estador(self): 
        self._ativo = not self._ativo

    def receber_avaliacao(self, cliente, nota): 
        avaliacao = Avaliacao(cliente=cliente, nota=nota)
        self._avaliacao.append(avaliacao)

    def media_avaliacoes(self):
        if not self._avaliacao: 
            return 0 
        media_das_notas = round(sum(avaliacao._nota for avaliacao in self._avaliacao)/len(self._avaliacao), 1)
        return media_das_notas
    