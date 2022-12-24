if selected == "Sobre":
    st.markdown(
    """
    O Twitter desde de sua criação tem se destacado como uma notória rede social, seja pela sua gama de usuários, ou pela quantidade de conteúdos criados a cada momento!
    Conteúdos estes que por sua vez geram dados e mais dados, dados que ultrapassam a barreira dos 280 caracteres e chegam para nós em inúmeros formatos, sejam posts, imagens, hashtags... 
    A partir do "Detector de sentimentos do Twitter", busca-se encontrar insights que apresentem resultados relevantes sobre a avaliação de sentimentos das palavras buscadas, considerando a classificação por polaridade, trazendo importantes informaçoes para diversas atividades.
    Diante da dinamicidade introduzida no cotidiano das pessoas pelas mídias sociais, bem como pela evolução tecnológica que proporcionou a coleta, extração e compartilhamento dos dados, muitas informações relevantes podem ser obtidas por meio de técnicas de análise de sentimentos. 
    Para utilizar a aplicação, basta que o usuário forneça a tema por meio de palavra-chave, que passará por análise algorítmica e retornará gráficos com análise de sentimento, representado pela classificação por polaridade, e nuvem de palavras para o(s) tema(s) sugerido(s). 
    """
    )

if selected == "Fluxo do APP":
    st.markdown(
    """
       ## Fluxo da Aplicação
    ```mermaid
    stateDiagram-v2
        [*] --> Entrada
        Entrada --> Válida
        Válida --> Processamento
        Processamento --> Gráfico_Sentimento
        Processamento --> Nuvem_Palavras 
        Gráfico_Sentimento --> Mensagem_Sucesso
        Nuvem_Palavras --> Mensagem_Sucesso
        Mensagem_Sucesso --> FIM
        Entrada --> Inválida
        Inválida --> Mensagem_Erro
        Mensagem_Erro --> FIM
    ```
    """
    )

        
if selected == "Desenvolvedores":
    st.markdown(
    """      
    ## Desenvolvedores
     - [Tarciano Filho](https://github.com/tarcianofilho)
     - [Rayanne Oliveira](https://github.com/RayanneOlivera)
     - [José Aurelio](https://github.com/joseaureliok)
     - [Kaio Emanuel](https://github.com/keikorr)
     - [Amanda Moreira](https://github.com/amandamoreyra)
    """
    )