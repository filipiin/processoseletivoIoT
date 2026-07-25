import time
from machine import Pin, ADC

LIMIAR_BLOQUEIO = 100   
LIMIAR_LIVRE = 500      
TEMPO_MICROPARADA = 5000 
DEBOUNCE = 250          

# Parâmetros do LDR 
GAMMA = 0.7             
RL10 = 50.0             

# LDR no pino 34 
ldr = ADC(Pin(34))
ldr.atten(ADC.ATTN_11DB)   

# Botão de reset no pino 5 com pull-up interno 
btn = Pin(5, Pin.IN, Pin.PULL_UP)

# Quantas peças já passaram
# True = tem uma peça tampando o sensor agora
# Evita ficar spamando "Micro-parada" toda hora
contador = 0               
bloqueado = False          
inicio_bloqueio = 0        
alerta_emitido = False     

# Controle do debounce do botão
ultimo_btn = 1             
estado_btn = 1             
tempo_btn = 0             

# Pega o número bruto do ADC (0 a 4095)
# Transforma em tensão (V), considerando referência de 5V
# Calcula a resistência do LDR usando divisor de tensão (resistor fixo de 2k)
def ler_lux():
    raw = ldr.read()                
    vol = raw / 4096.0 * 5          
    res = 2000 * vol / (1 - vol / 5)
    
    # Fórmula do datasheet do LDR
    # Invertendo a equação pra achar o Lux
    return pow(RL10 * 1e3 * pow(10, GAMMA) / res, (1 / GAMMA))

    # Mensagem exata que o professor/CI pediu pra aparecer
    # Loop infinito (o sistema fica rodando pra sempre)
def main():
    global contador, bloqueado, inicio_bloqueio, alerta_emitido
    global ultimo_btn, estado_btn, tempo_btn
    
    print("Contador de Producao Inicializado")

    while True:
        agora = time.ticks_ms()   
        lux = ldr.read()      

        # Verifica luz ambiente se tava livre e a luz caiu abaixo do limiar 
        # Marca a hora que a peça entrou e reseta o alerta pra caso tenha sido disparado antes
        if not bloqueado and lux > 2045:
            bloqueado = True
            inicio_bloqueio = agora      
            alerta_emitido = False       
        
        # Se tava bloqueado e a luz subiu acima do limiar -> a peça saiu conta +1
        elif bloqueado and lux < 999:
            bloqueado = False
            contador += 1                
            print(f"Peca detectada! Total: {contador}")

        
        if bloqueado and not alerta_emitido:
            # Calcula quanto tempo a peça tá parada na frente do sensor
            # Só manda uma vez, depois marca como já emitido
            if time.ticks_diff(agora, inicio_bloqueio) > TEMPO_MICROPARADA:
                print("Alerta: Micro-parada detectada!")
                alerta_emitido = True   

        # Lê o estado atual do botão
        leitura = btn.value()           
        
        # Se o estado do botão mudou, atualiza o timestamp da mudança
        # Guarda a leitura pra comparar no próximo ciclo
        if leitura != ultimo_btn:
            tempo_btn = agora
        ultimo_btn = leitura            
        
        # Se o tempo desde a última mudança passou do debounce -> sinal tá estável
        if time.ticks_diff(agora, tempo_btn) > DEBOUNCE:
            # Detecta borda de descida: estava HIGH (1) e agora está LOW (0) -> pressionou
            if leitura == 1 and estado_btn == 0:
                contador = 0
                bloqueado = False
                alerta_emitido = False
                print("Turno resetado com sucesso. Contadores zerados.")

             # Atualiza o estado estável do botão
            estado_btn = leitura         

        # Dá um tempinho de 10ms pra não sobrecarregar o processador (famoso "respiro")
        time.sleep_ms(10)

if __name__ == "__main__":
    main()