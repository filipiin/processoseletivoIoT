

#### Commit e Push

Após suas alterações:

```bash
git add .
git commit -m "Descrição clara do que foi feito"
git push
```


## Relatório do Candidato
---

### Identificação do Candidato

- **Nome completo: Filipe Leite Ribeiro**
- **GitHub: https://github.com/filipiin**

---

## Visão Geral da Solução

O objetivo do projeto é criar um contador de peças pra uma esteira de fábrica. Ele usa um sensor de luz pra ver quando a peça passa e conta ela, também consegue avisar se alguma peça ficar travada no meio do caminho disparando um alerta. Se precisar começar de novo o operador pode apertar um botão e resetar tudo.

---

## Arquitetura do Sistema Embarcado

O programa fica rodando o tempo todo num loop, olhando pro sensor e o botão.

Pra não travar o sistema com pausas eu fiz um esquema que só compara a hora que a peça entrou com a hora atual, assim o programa continua livre pra fazer outras coisas e ler o botão sem congelar. O fluxo funciona assim: ele lê a claridade, avalia se a esteira ta livre ou com peça e depois toma a decisão de somar no contador ou dar o alerta.

---

## Componentes Utilizados na Simulação


ESP32: É a placa principal que processa tudo e controla as entradas.

Sensor LDR (Pino 34): É a nossa barreira de luz, ele que percebe a sombra quando a peça passa na frente.

Botão (Pino 5): Serve pro usuário resetar a contagem, ele já tá com o resistor interno de pull-up ligado pra facilitar a montagem.

---

## Decisões Técnicas Relevantes

Valores diretos do sensor: Em vez de usar a fórmula pra transformar o sinal em Lux, eu preferi olhar pro valor puro que o sensor devolve. Se a leitura passa de 2045 quer dizer que escureceu e a peça ta ali. Isso deixou o código muito mais rápido e gastando menos matemática.
 
Contar só na saída: O sistema só conta a peça quando a luz volta ao normal e não quando a peça entra. Por que se contar na entrada e a peça der uma balançada ou travar, o contador ia ficar doido somando várias vezes a mesma peça.

Filtro do botão: Fiz um debounce contando o tempo pra evitar que um aperto mecânico no botão conte como vários toques.
---

## Resultados Obtidos

O sistema tá funcionando super bem e conta as peças direito sempre que elas saem do sensor. O aviso de micro-parada também dispara certinho cravado em 5 segundos se a esteira travar, e ele avisa só uma vez. Como não tem código bloqueando o andamento do loop o validador do Wokwi aprovou os testes de primeira.

---

## Comentários Adicionais (Opcional)

No começo eu tava quebrando a cabeça tentando fazer o cálculo do Lux funcionar em tempo real, mas depois percebi que pro teste passar e o sistema ficar rápido ler os números crus do ADC direto era bem mais rapido e menos custoso. 

---

> Este relatório faz parte da avaliação técnica.  
> Clareza, objetividade e organização são tão importantes quanto o funcionamento do código.

---

## Especificação dos Testes Automatizados (Wokwi CI)

Para que o projeto seja validado com sucesso na esteira de integração contínua (CI), o firmware escrito em MicroPython deve interagir corretamente com as leituras dos sensores descritos em cada cenário e enviar as mensagens de status exatas.

### Requisitos Críticos de Implementação

1. **Casamento Exato de Strings:** O Wokwi CI faz uma verificação estrita caractere por caractere. Se houver divergência em maiúsculas/minúsculas, acentuação ou falta de pontuação, o teste irá falhar.
2. **Arquitetura Não-Bloqueante:** Evite o uso de funções bloqueantes. Elas podem fazer com que o firmware perca a janela de tempo em que o simulador altera o peso, quebrando a sincronia do teste automatizado.

---

## Suporte

Em caso de dúvidas:

- Consulte o material dos cursos EAD
- Leia atentamente este README
- Analise os logs das GitHub Actions
- Utilize os canais oficiais para contato com os instrutores
