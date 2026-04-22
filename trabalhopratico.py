import abc

# Classes de Dados: Processo e Resultado

class Processo:
    def __init__(self, pid, tempo_chegada, tempo_execucao):
        self.id = pid 
        self.tempoChegada = tempo_chegada 
        self.tempoExecucao = tempo_execucao 
        self.tempoRestante = tempo_execucao 
        self.tempoInicio = -1 
        self.tempoFim = 0 

    def resetar(self):
        self.tempoRestante = self.tempoExecucao
        self.tempoInicio = -1
        self.tempoFim = 0

class ResultadoSimulacao: 
    def __init__(self):
        self.ordemExecucao = [] 
        self.temposExecucaoEfetivos = {} 
        self.tempoEsperaTotal = 0

    def registrarExecucao(self, pid): 
        if not self.ordemExecucao or self.ordemExecucao[-1] != pid:
            self.ordemExecucao.append(pid)

    def registrarTempoFinal(self, p): 
        # Tempo efetivo = Tempo que terminou - Tempo que chegou
        self.temposExecucaoEfetivos[p.id] = p.tempoFim - p.tempoChegada
        # Espera = (Tempo total de vida) - (Tempo que passou trabalhando)
        self.tempoEsperaTotal += (p.tempoFim - p.tempoChegada - p.tempoExecucao)

# Estratégias de Escalonamento UML Interface Algoritmo

class Algoritmo(metaclass=abc.ABCMeta): 
    @abc.abstractmethod
    def escolher(self, fila): pass 
    
    @abc.abstractmethod
    def ehPreemptivo(self): pass 

class FCFS(Algoritmo): 
    def escolher(self, fila): return fila.pop(0) if fila else None
    def ehPreemptivo(self): return False

class SJF_NaoPreemptivo(Algoritmo):
    def escolher(self, fila):
        fila.sort(key=lambda p: p.tempoRestante)
        return fila.pop(0) if fila else None
    def ehPreemptivo(self): return False

class SJF_Preemptivo(Algoritmo): 
    def escolher(self, fila):
        fila.sort(key=lambda p: p.tempoRestante)
        return fila.pop(0) if fila else None
    def ehPreemptivo(self): return True

class RoundRobin(Algoritmo): 
    def __init__(self, quantum):
        self.quantum = quantum 
    def escolher(self, fila):
        return fila.pop(0) if fila else None
    def ehPreemptivo(self): return True

# Simulador Principal

class SimulacaoEscalonador: 
    def __init__(self, algoritmo, ttc):
        self.algoritmo = algoritmo 
        self.ttc = ttc 
        self.tempoAtual = 0 
        self.filaProntos = [] 
        self.resultado = ResultadoSimulacao() 

    def executar(self, lista_processos): 
        processos_restantes = sorted(lista_processos, key=lambda p: p.tempoChegada)
        total_processos = len(lista_processos)
        processos_finalizados = 0
        processo_na_cpu = None
        quantum_restante = getattr(self.algoritmo, 'quantum', None)

        while processos_finalizados < total_processos:
            # Chegada de processos
            while processos_restantes and processos_restantes[0].tempoChegada <= self.tempoAtual:
                self.filaProntos.append(processos_restantes.pop(0))
                # o novo processo pode forçar re-escolha
                if self.algoritmo.ehPreemptivo() and processo_na_cpu:
                    self.filaProntos.append(processo_na_cpu)
                    processo_na_cpu = None

            # Escolha do processo
            if processo_na_cpu is None:
                processo_na_cpu = self.algoritmo.escolher(self.filaProntos)
                if processo_na_cpu:
                    # Troca de Contexto (TTC) 
                    if self.resultado.ordemExecucao and self.resultado.ordemExecucao[-1] != processo_na_cpu.id:
                        self.tempoAtual += self.ttc
                    
                    self.resultado.registrarExecucao(processo_na_cpu.id)
                    if processo_na_cpu.tempoInicio == -1:
                        processo_na_cpu.tempoInicio = self.tempoAtual
                    quantum_restante = getattr(self.algoritmo, 'quantum', None)

            # Execução na CPU
            if processo_na_cpu:
                processo_na_cpu.tempoRestante -= 1
                self.tempoAtual += 1
                if quantum_restante is not None: quantum_restante -= 1

                # Verificações de saída da CPU
                if processo_na_cpu.tempoRestante == 0:
                    processo_na_cpu.tempoFim = self.tempoAtual
                    self.resultado.registrarTempoFinal(processo_na_cpu)
                    processo_na_cpu = None
                    processos_finalizados += 1
                elif quantum_restante == 0: # Fim do Quantum (Round Robin)
                    self.filaProntos.append(processo_na_cpu)
                    processo_na_cpu = None
            else:
                self.tempoAtual += 1 # CPU Ociosa

        return self.resultado

# Interface de Entrada e Exibição

def main():
    print("--- Simulador de Escalonamento IFRS ---")
    n = int(input("Número de processos: ")) 
    processos = []
    for i in range(n):
        pid = int(input(f"PID do processo {i+1}: ")) 
        t_chegada = int(input(f"Tempo de chegada do processo {pid}: "))
        t_exec = int(input(f"Tempo de execução (burst) do processo {pid}: ")) 
        processos.append(Processo(pid, t_chegada, t_exec))

    print("\nPolíticas: 1.FCFS | 2.SJF (N-P) | 3.SJF (P) | 4.Round Robin")
    opcao = int(input("Escolha a política: ")) 
    
    ttc = int(input("Tempo de Troca de Contexto (TTC): "))  
    quantum = 0
    if opcao == 4:
        quantum = int(input("Quantum: ")) 
        alg = RoundRobin(quantum)
    elif opcao == 1: alg = FCFS()
    elif opcao == 2: alg = SJF_NaoPreemptivo()
    elif opcao == 3: alg = SJF_Preemptivo()

    sim = SimulacaoEscalonador(alg, ttc)
    res = sim.executar(processos)

    print("\n--- RESULTADO DA SIMULAÇÃO ---")
    print(f"Ordem de Execução: {res.ordemExecucao}")
    print(f"Tempos de Execução Efetivos: {res.temposExecucaoEfetivos}") 
    
    if opcao in [1, 2]: 
        print(f"Tempo Médio de Espera: {res.tempoEsperaTotal / n:.2f}")

if __name__ == "__main__":
    main()
