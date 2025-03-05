# Script de Download Automatizado com Selenium Netsuite

## Descrição

Este script Python foi desenvolvido para automatizar o download de múltiplos arquivos de um website NetSuite. Ele utiliza a biblioteca Selenium para controlar um navegador Chrome, navegar entre páginas e clicar automaticamente em links de download. O script é projetado para baixar até 30.000 arquivos, navegando pelas páginas do site até que o limite seja atingido ou não haja mais páginas disponíveis.

## Funcionalidades

O script executa as seguintes ações:

1.  **Configuração do WebDriver:**
    *   Inicializa um navegador Chrome maximizado utilizando o Selenium WebDriver.
    *   Define um tempo de espera implícito de 15 segundos para que os elementos da página carreguem, melhorando a robustez do script ao lidar com carregamentos assíncronos.

2.  **Navegação para a URL Alvo:**
    *   Abre o navegador na URL especificada, que aponta para uma página de documentos do NetSuite.

3.  **Função `baixar_todos_arquivos()`:**
    *   Localiza todos os elementos de link de download na página atual utilizando XPath (`//a[text()='Fazer download']`).
    *   Itera sobre cada link de download encontrado:
        *   Rola a página até que o link esteja visível, garantindo que o Selenium possa interagir com ele. (Para mais velocidade certifique-se que todos os links aparecem na tela diminuindo o zoom)
        *   Clica no link para iniciar o download do arquivo.
        *   Imprime no console o link do arquivo cujo download foi iniciado.
        *   Adiciona um pequeno delay de 2 segundos entre os downloads para evitar sobrecarregar o servidor e garantir que cada download seja iniciado corretamente.
        *   Inclui tratamento de exceção para capturar e imprimir erros que possam ocorrer durante o download de um arquivo específico.

4.  **Função `proxima_pagina()`:**
    *   Localiza o botão "Próximo" de paginação utilizando XPath (`//*[@id='segment_sel_fs']/span[2]/button[2]']`).
    *   Verifica se o botão "Próximo" está desativado ou oculto (indicando que não há mais páginas):
        *   Se estiver desativado ou oculto, imprime uma mensagem informando que o download foi finalizado e retorna `False`.
    *   Rola a página até o botão "Próximo" para garantir a visibilidade.
    *   Clica no botão "Próximo" para navegar para a próxima página.
    *   Imprime uma mensagem indicando a navegação para a próxima página.
    *   Adiciona um tempo de espera de 5 segundos para permitir que a próxima página carregue completamente.
    *   Inclui tratamento de exceção para capturar e imprimir erros que possam ocorrer ao tentar avançar para a próxima página.

5.  **Loop Principal de Download:**
    *   Aguarda o usuário pressionar Enter para iniciar o processo de download.
    *   Inicializa um contador `total_baixados` para rastrear o número total de arquivos baixados e define um `limite_total` de 30.000 downloads.
    *   Entra em um loop `while` que continua enquanto o `total_baixados` for menor que o `limite_total`.
    *   Dentro do loop:
        *   Chama a função `baixar_todos_arquivos()` para iniciar o download de todos os arquivos na página atual.
        *   Conta o número de links de download encontrados na página atual para atualizar o `total_baixados`.
        *   Imprime o total de arquivos baixados até o momento.
        *   Verifica se o `total_baixados` atingiu ou ultrapassou o `limite_total` ou se a função `proxima_pagina()` retorna `False` (indicando que não há mais páginas). Se alguma dessas condições for verdadeira, o loop é interrompido.

6.  **Finalização e Tratamento de Erros:**
    *   Imprime "Download concluído!" ao final do processo de download bem-sucedido.
    *   Implementa tratamento para `KeyboardInterrupt` para permitir que o usuário interrompa o script manualmente.
    *   Inclui um bloco `try...except` para capturar e imprimir erros inesperados que possam ocorrer durante a execução do script.
    *   No bloco `finally`, garante que o navegador Chrome seja fechado (`driver.quit()`) ao final da execução, independentemente de ocorrerem erros ou não.

## Bibliotecas Utilizadas

*   **Selenium:** (`selenium`, `selenium.webdriver.common.by`, `selenium.webdriver.support.ui`, `selenium.webdriver.support.expected_conditions`)
    *   Utilizada para automação de navegadores web. Permite controlar o Chrome, navegar em páginas web, interagir com elementos (clicar em links, rolar a página) e esperar por elementos dinâmicos.

*   **time:** (`time`)
    *   Utilizada para adicionar pausas (`time.sleep()`) no script. Isso é útil para controlar a velocidade de execução, evitar sobrecarga do servidor e garantir que elementos da página carreguem corretamente antes de interagir com eles.

## Pré-requisitos

Para executar este script, você precisa ter instalado:

*   **Python:** Certifique-se de ter o Python instalado em seu sistema.
*   **Selenium:** Instale a biblioteca Selenium utilizando pip:
    ```bash
    pip install selenium
    ```
*   **ChromeDriver:**
    *   Baixe o ChromeDriver compatível com a versão do seu navegador Google Chrome.
    *   Extraia o executável do ChromeDriver e coloque-o em um diretório que esteja no seu PATH do sistema, ou especifique o caminho para o ChromeDriver ao inicializar o `webdriver.Chrome()`.

## Como Executar

1.  **Instale os pré-requisitos** conforme listado na seção anterior.
2.  **Salve o script** em um arquivo Python (por exemplo, `download_script.py`).
3.  **Execute o script** a partir do terminal:
    ```bash
    python download_script.py
    ```
4.  O script irá aguardar você pressionar a tecla `Enter` para iniciar o processo de download.
5.  Acompanhe o progresso e as mensagens de log no terminal.

## Limitações e Considerações

*   **Dependência da Estrutura do Site:** O script é altamente dependente da estrutura HTML da página do NetSuite, especialmente dos seletores XPath utilizados para encontrar os links de download e o botão "Próximo". Qualquer alteração na estrutura do site pode quebrar o script, exigindo ajustes nos seletores.
*   **Tratamento de Erros:** Embora o script inclua tratamento de exceções, ele pode não cobrir todos os cenários de erro possíveis. É importante monitorar a execução do script.
*   **Limite de Download:** O script possui um limite de download de 30.000 arquivos. Este limite pode ser ajustado alterando a variável `limite_total`.
*   **Velocidade de Download:** A velocidade de download é influenciada pela velocidade da conexão de internet, pelo tempo de resposta do servidor e pelo delay de 2 segundos adicionado entre os downloads.
*   **NetSuite e Autenticação:** Este script assume que a autenticação no NetSuite já foi realizada ou que a URL fornecida dá acesso direto aos arquivos.
*   **Detecção de Botões Desativados/Ocultos:** O script verifica se o botão "Próximo" está desativado ou oculto com base no atributo "class" e na visibilidade. Dependendo da implementação do site, outras formas de detecção podem ser necessárias.

## Autor

\[Ricardo B Meneses]

