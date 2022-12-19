# Santa Concorrência!
"""    
    A nova nave do império, a temida BAT2, está quase pronta para 
    aniquilar a ameaça rebelde. Falta apenas o núcleo de controle de 
    processos concorrentes para que ela funcione a plena capacidade. 
    O sistema operacional se encarrega de enviar as solicitações de 
    processos, e você foi designado para implementar o controle da ordem 
    de execução de partes dos procs utilizando a abordagem round-robin. 
    O sistema operacional já determina a fatia de tempo de cada 
    solicitação: a execução de um comando especial.

    A comunicação com o sistema é simples, as funcionalidades são 
    apresentadas como descritas acima pelo sistema operacional, e seu 
    programa deve organizá-las e executá-las conforme solicitado pelas
    instâncias superiores.
"""

class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items)-1]

    def size(self):
        return len(self.items)


class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items)-1]

    def size(self):
        return len(self.items)


def crypto(S):
    """
    Define uma chave criptográfica.

    A partir da sequência 𝑆 de não mais que 8 símbolos + ou − que 
    indicam, respectivamente, que a ordem dos dígitos adjacentes 
    deve ser crescente ou decrescente. Esta função gera o menor 
    número possível com dígitos distintos.
    
    Args:
        S (str): sequência de símbolos.
    """
    aux = Stack()
    numbers = Stack()
    encrypted = []
    for i in range((len(S)+1), 0, -1):
        numbers.push(i)
    for sign in S:
        if sign == "-":
            aux.push(numbers.pop())
        elif sign == "+":
            encrypted.append(numbers.pop())
            while not aux.isEmpty():
                encrypted.append(aux.pop())
    while not numbers.isEmpty():
        encrypted.append(numbers.pop())
    while not aux.isEmpty():
        encrypted.append(aux.pop())
    
    for i in encrypted:
        print(i, end="")
    print()


def merge(gaps):
    """
    Apresenta uma sequência de intervalos
    
    Os intervalos são apresentados sem sobreposição, em ordem, criada
    a partir dos I intervalos dados. Cada intervalo é definido por
    valores inteiros no formato [x_0, x_1], separados por espaço,
    tais que x_0 <= x_1.

    Args:
        gaps (str): intervalos.
    """
    coordinates = [] 
    queue = Queue()
    interval = []
    gaps = gaps.replace(", ", " ").split("] ")
    for gap in gaps:
        elem = gap.strip("[]").split()
        elem[0], elem[1] = int(elem[0]), int(elem[1])
        coordinates.append(elem)
    coordinates = sorted(coordinates)
    for i in coordinates:
        queue.enqueue(i)
    interval.append(queue.dequeue())
    
    i = 0
    while not queue.isEmpty():
        if queue.peek()[0] <= interval[i][1] and queue.peek()[1] > interval[i][1]:
            interval[i][1] = queue.dequeue()[1]
        elif queue.peek()[0] <= interval[i][1] and queue.peek()[1] <= interval[i][1]:
            queue.dequeue()
        else:
            interval.append(queue.dequeue())
            i += 1

    for i in interval:
        print(i, end=" ")
    print()


def deYodafy(string):
    """
    Decodifica uma sequência de palavras.
    
    Decodifica as instruções fornecidas como uma sequência de palavras 
    (e pontuação), invertendo sua ordem para que façam sentido.

    Args:
        string (str): sequência de palavras e pontuação.
    """
    dot = string[-1]
    string = string.rstrip(string[-1])
    string_decoded = string.split()
    string_decoded[0] += dot
    print(" ".join(string_decoded[::-1]))


def process(proc):
    """
    Executa o próximo command especial disponível conforme o algoritmo round-robin.

    Args:
        proc (Queue): fila de execução com comandos a executar
    """
    if proc.peek()[0][0] == "crypto":
        crypto(proc.peek()[0][1])   
    elif proc.peek()[0][0] == "merge":
        merge(proc.peek()[0][1])            
    elif proc.peek()[0][0] == "deYodafy":
        deYodafy(proc.peek()[0][1])         
    if len(proc.peek()) > 1:
        not_executed = proc.dequeue()[1::]
        execution_queue.enqueue(not_executed)
    else:
        execution_queue.dequeue()


def halt(counter): 
    """
    Interrompe a execução e mostra quantas solicitações ficaram órfãs
    (não foram finalizadas) e a quantidade total de comandos que não 
    foram executados.
    
    Args:
        counter (int): contador de comandos órfãos.
    """
    print(f"{execution_queue.size()} processo(s) e {counter} comando(s) órfão(s).")


execution_queue = Queue()
requests = []
command = ""
commands_counter = 0

while "halt" not in command:
    command = input().split()
    if command[0] == "add":
        """
        Adiciona uma solicitação com x>0 procs à fila de execução. 
        Este comando é seguido de x instâncias de um dos 3 comandos 
        especiais (crypto, merge, deYodafy), que devem ser executados
        na ordem em que são fornecidos para completar o processo.
        """
        x = int(command[1])
        for i in range(x):
            proc = input().split(" ", 1)
            requests.append(proc)
            commands_counter += 1 
        execution_queue.enqueue(requests)
        requests = []            
    elif command[0] == "process":
        if execution_queue.size() == 0:
            continue
        else:
            process(execution_queue)   
        commands_counter -= 1                       
    elif command[0] == "halt":
        halt(commands_counter) 

# python 01_santa_concorrencia.py < test01.txt > result01.txt | python 01_santa_concorrencia.py < test02.txt > result02.txt | python 01_santa_concorrencia.py < test03.txt > result03.txt | python 01_santa_concorrencia.py < test04.txt > result04.txt | python 01_santa_concorrencia.py < test05.txt > result05.txt | python 01_santa_concorrencia.py < test06.txt > result06.txt | python 01_santa_concorrencia.py < test07.txt > result07.txt | python 01_santa_concorrencia.py < test08.txt > result08.txt | python 01_santa_concorrencia.py < test09.txt > result09.txt | python 01_santa_concorrencia.py < test10.txt > result10.txt | python 01_santa_concorrencia.py < test11.txt > result11.txt | python 01_santa_concorrencia.py < test12.txt > result12.txt | python 01_santa_concorrencia.py < test13.txt > result13.txt
