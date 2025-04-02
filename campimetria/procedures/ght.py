class GHT:
    probabilidade_ght = [0.0] * 76
    desvio_padrao = [0] * 76
    base_estatistica_05 = [0] * 76
    base_estatistica_10 = [0] * 76
    base_estatistica_20 = [0] * 76
    base_estatistica_50 = [0] * 76
    GH = 0

    def __init__(self, dictionary=None):
        self.dictionary = dictionary
        self.delta_prob_paciente = [0.0] * 5
        self.delta_base = [0] * 5
        self.a_sup = [[] for _ in range(5)]
        self.a_inf = [[] for _ in range(5)]
        self.all_region = []

    def atribui_indices_das_areas(self, olho, programa):
        if programa == "Central30":
            if olho == "Direito":
                self.a_sup = [[31, 32, 33], [21, 22, 23, 24], [19, 20, 28, 29, 30], [5, 6, 11, 12, 13, 14], [7, 8, 15, 16]]
                self.a_inf = [[41, 42, 43], [51, 52, 53, 54], [38, 39, 40, 49, 50], [59, 60, 61, 62, 67, 68], [63, 64, 69, 70]]
            elif olho == "Esquerdo":
                self.a_sup = [[32, 33, 34], [21, 22, 23, 24], [25, 26, 35, 36, 37], [7, 8, 13, 14, 15, 16], [5, 6, 11, 12]]
                self.a_inf = [[42, 43, 44], [51, 52, 53, 54], [45, 46, 47, 55, 56], [61, 62, 63, 64, 69, 70], [59, 60, 67, 68]]
        self.all_region = [idx for sublist in self.a_sup + self.a_inf for idx in sublist]

    def ght_laudo(self):
        self.atribui_indices_das_areas("Direito", "Central30")

        if self.gh99_5() or GHT.GH > 6:
            return self.dictionary.get("Sensibilidade Anormalmente Elevada")
        elif self.delta(100):
            return self.dictionary.get("Fora dos Limites Normais")
        elif self.sum():
            return self.dictionary.get("Fora dos Limites Normais")
        elif self.delta(50):
            return self.dictionary.get("Linha de Fronteira - Redução Geral da Sensibilidade") if self.gh0_5() else self.dictionary.get("Linha de Fronteira")
        else:
            return self.dictionary.get("Redução Geral da Sensibilidade") if self.gh0_5() else self.dictionary.get("Dentro dos Limites Normais")

    def gh99_5(self):
        inc_zero, inc_five = 0, 0
        for idx in self.all_region:
            if GHT.desvio_padrao[idx] + GHT.GH > 0:
                inc_zero += 1
            if GHT.desvio_padrao[idx] + GHT.GH > 5:
                inc_five += 1
        return inc_five > 5

    def delta(self, limite):
        self.calcula_delta_prob_paciente()
        return any(abs(delta) > limite for delta in self.delta_prob_paciente)

    def calcula_delta_prob_paciente(self):
        self.delta_prob_paciente = [
            self.somatoria_probabilidade_lim_paciente(self.a_sup[i]) - self.somatoria_probabilidade_lim_paciente(self.a_inf[i])
            for i in range(5)
        ]

    def somatoria_probabilidade_lim_paciente(self, area):
        soma = 0
        for idx in area:
            if GHT.probabilidade_ght[idx] >= 1.0:
                aux = 0
            elif GHT.probabilidade_ght[idx] >= 0.05:
                aux = 2
            elif GHT.probabilidade_ght[idx] >= 0.02:
                aux = 5
            elif GHT.probabilidade_ght[idx] >= 0.01:
                aux = 5 * abs(GHT.desvio_padrao[idx])
            else:
                aux = 10 * abs(GHT.desvio_padrao[idx])
            soma += aux
        return soma

    def sum(self):
        limite = 1.2
        return any(
            ((self.somatoria_probabilidade_lim_paciente(self.a_sup[i]) * 100) / self.sum_lim_base_01(self.a_sup[i]) > limite and
             (self.somatoria_probabilidade_lim_paciente(self.a_inf[i]) * 100) / self.sum_lim_base_01(self.a_inf[i]) > limite)
            for i in range(5)
        )

    def sum_lim_base_01(self, area):
        return sum(10 * abs(GHT.base_estatistica_10[idx]) for idx in area)

    def gh0_5(self):
        return GHT.GH < -2
