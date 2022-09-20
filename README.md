# Projeto Análise de Sentimentos

## Sugestão de nome da aplicação:

**"PyGht Sentiment Time"**

## Resumo

O projeto tem fundamento na **metodologia CRISP-DM** para desenvolvimento das etapas de transformação de dados e produção de conhecimento de forma gerenciável.
Com esse fundamento, terá como propósito as seguintes etapas:\
	1. **Proposta**\
	Superada a fase clássica de entendimento do negócio pertinente à metologia empregada, uma vez que a base de dados foi fornecida e com tratamento de dados de sentimento dos tweets coletados de API do Twitter.\
	Assim, após reuniões com o squad, delimitou-se a o projeto em uma aplicação de avaliação de análise de sentimento com base no tema e palavra alvo fornecidos pelo usuário, correlacionando-os com a polaridade (positividade, neutralidade e/ou negatividade) em face do período de tempo (horário do dia e dia da semana), apresentando análises gráficas para tanto. \
	2. **Entendimento**\
	Serão consideras a proposta e a problematização do projeto para averiguação da possibilidade de adequação ao conjunto de dados e a respectiva viabilidade de execução da proposta: coleta inicial, descrição, análise exploratória e verificação de qualidade e integridade do conjunto de dados.
	Em caso de necessidade, em face da contextualização e viabilidade do projeto, será submetido a reavaliação e adequação da proposta do projeto.\
	3. **Preparação**\
	Superada a etapa antecedente e produzidos os insights necessários, nessa etapa o squad distribuirá a execução das tarefas para: seleção, limpeza, construção, integração e formatação do conjunto de dados.\
	4. **Modelagem**\
	Recebido o conjunto de dados, será avaliada a necessidade de ajuste, prosseguindo ou retornando a etapa anterior, caso necessário.
	Devidamente adequado, nessa etapa o squad distribuirá a execução das tarefas para: seleção da técnica, testes, construção e avaliação do modelo.\
	5. **Avaliação**\
	Aqui, superadas as etapas anteriores,  o squad distribuirá a execução das tarefas para: avaliação dos resultados, revisão do processo e definição sobre a implementação ou adequação do projeto.
	Entendidas necessárias alterações ao projeto e/ou ao processo, após a revisão, proceder-se-ão às devidas adequações. \
	6. **Implantação**\
	Por fim, na etapa final, o squad distribuirá a execução das tarefas para: planejamento da implantação, monitoração e manutenção da aplicação, relatório final e revisão do projeto.

**Fluxo de execução do projeto**:
```mermaid
graph TD
    A[Análise Sentimento Twitter] -->|Obtenção base de dados| B((Proposta / Entrega 24.09))
    B -->|Contextualização e Viabilidade| C{Entendimento / Entrega 24.09 }
    C --> |Reavaliação e Adequação| B
	C -->|Insights| D((Preparação / Entrega 22.10))
    D --> E{Modelagem / Entrega 22.10}
    E -->|Ajuste| D
	E --> F{Avaliação / Entrega 19.11}
	F --> |Adaptação| B
	F --> G((Implantação / Entrega 19.11))
````
## Entregas
1. Etapas 1 e 2: **24.09.2022**
2. Etapas 3 e 4: **22.10.2022**
3. Etapas 5 e 6: **19.11.2022**

## Justificativa
Diante da dinamicidade introduzida no cotidiano das pessoas pelas mídias sociais, bem como pela evolução tecnológica que proporcionou a coleta, extração e compartilhamento dos dados, muitas informações relevante podem ser obtidas por meio de técnidas de análise de sentimentos.\
A partir desse projeto, busca-se encontrar insights a apresentar resultados relevantes sobre a avaliação de sentimentos com base na classificação por polaridade em determinados períodos de tempo, do dia e da semana, produzindo informações e promovendo insights importantes para diversas atividades.

**Fluxo da aplicação final**:

```mermaid
stateDiagram-v2
    [*] --> Entrada
	Entrada --> POSITIVA
    POSITIVA --> Run_App
	Run_App --> Gráfico_Sentimento
	Run_App --> Gráfico_Período
	Run_App --> Nuvem_Palavras 
	Gráfico_Sentimento --> MSG_Sucesso
	Gráfico_Período --> MSG_Sucesso
	Nuvem_Palavras --> MSG_Sucesso
	MSG_Sucesso --> MSG_Continua
    Entrada --> NEGATIVA
    NEGATIVA --> MSG_Erro
	MSG_Erro --> MSG_Continua
	MSG_Continua --> SIM
	MSG_Continua --> NÃO
	SIM --> Entrada
	NÃO --> [*]
```

## Equipe
1. _Amanda Moreira_ [https://github.com/amandamoreyra]
2. _Rayanne Oliveira dos Santos_ [https://github.com/RayanneOlivera]
3. _Kaio Emanule_ [https://github.com/keikorr]
4. _Tarciano Filho_ [https://github.com/tarcianofilho]
5. _Renato Rodrigues Vieira dos Santos_ [https://github.com/renato-rodrig]
6. _Leonardo Monteiro_ [https://github.com/lemont037]
7. _Ítalo Magalhães_ [https://github.com/italo-mgl]
8. _José Aurelio Kovalczuk de Oliveira_ [https://github.com/joseaureliok]
