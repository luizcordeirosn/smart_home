# Smart Home Hub

Bem-vindo ao Smart Home Hub, uma aplicação de linha de comando para simular e gerenciar uma variedade de dispositivos inteligentes. Este projeto utiliza uma arquitetura orientada a eventos com o padrão Observer para registrar as atividades dos dispositivos e uma máquina de estados para gerenciar o ciclo de vida de cada um.

## 📋 Funcionalidades

Esta simulação fornece um **Hub** central para gerenciar e interagir com múltiplos dispositivos inteligentes. Todas as mudanças de estado e eventos importantes são automaticamente registrados em um arquivo CSV para análise.

### Dispositivos Suportados
* **Door**: Pode estar `LOCKED`, `UNLOCKED`, `OPENED`.
* **Bulb**: Pode ser ligada (`ON`)/desligada (`OFF`) e ter seu brilho (`brightness`) e cor (`current_color`) ajustados.
* **Outlet**: Pode ser ligada (`ON`)/desligada (`OFF`), rastreando o consumo de energia (`Wh`).
* **Sprinkler**: Pode estar `IDLE`, `WATERING`, ou `PAUSED`, rastreando o consumo de água (`Litros*h`).
* **Thermostat**: Pode estar `IDLE`, `HEATING`, ou `COOLING` para manter uma temperatura alvo.
* **Camera**: Pode estar ligada (`ON`)/desligada (`OFF`) e pode estar em estado de `RECORDING`.

### Funcionalidades Principais
A interface de linha de comando (CLI) permite que você:
-   Liste todos os dispositivos configurados.
-   Veja o status detalhado e os atributos de um dispositivo específico.
-   Execute comandos em qualquer dispositivo (ex: `lock` em uma porta, `set_brightness` em uma lâmpada).
-   Altere o nome de um dispositivo.
-   Defina e execute rotinas envolvendo múltiplos dispositivos (ex: `leaving_home`, `good_night`).
-   Gere relatórios de uso e atividade.
-   Adicione e remova dispositivos dinamicamente.
-   Salve a configuração atual dos dispositivos em um arquivo JSON.

## 🚀 Como Começar

Siga estas instruções para colocar o projeto em funcionamento na sua máquina local.

### Pré-requisitos
* Python 3.10 ou mais recente.

### Instalação

1.  **Clone o repositório:**
    ```bash
    git clone git@github.com:luizcordeirosn/smart_home.git
    cd smart_home
    ```

2.  **(Opcional mas Recomendado) Crie um Ambiente Virtual:**
    É altamente recomendado usar um ambiente virtual para manter as dependências isoladas.
    ```bash
    # Crie o ambiente virtual
    python3 -m venv venv

    # Ative-o
    # No macOS/Linux:
    source venv/bin/activate
    # No Windows:
    .\venv\Scripts\activate
    ```

3.  **Instale as Dependências:**
    Instale todas as bibliotecas necessárias a partir do arquivo `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

### Executando a Aplicação

Para iniciar a interface de linha de comando interativa do Smart Home Hub, execute o seguinte comando a partir do **diretório raiz** do projeto:

```bash
python3 -m smart_home.core.cli
```
Isso iniciará o menu principal, onde você pode interagir com a simulação da casa inteligente.

## 📝 Uso

Assim que a aplicação estiver rodando, o menu principal será apresentado. Simplesmente digite o número correspondente à opção desejada e pressione Enter.

### Opções do Menu Principal

* `1. List Devices`: Mostra um resumo de todos os dispositivos configurados e seu estado atual.
* `2. Show Device Details`: Pede por um tipo e ID de dispositivo para mostrar todos os seus atributos.
* `3. Execute Command on Device`: Permite que você execute um comando (gatilho) específico em um dispositivo, como `lock` ou `turn_on`.
* `4. Change Device Attribute`: Permite modificar o nome de um dispositivo.
* `5. Run Routine`: Executa uma rotina pré-configurada (ex: `leaving_home`).
* `6. Generate Report`: Abre um sub-menu com vários relatórios de análise.
* `7. Save Configuration`: Salva o estado e os atributos atuais de todos os dispositivos no arquivo de configuração.
* `8. Add Device`: Um assistente para adicionar um novo dispositivo ao hub.
* `9. Remove Device`: Remove um dispositivo do hub.
* `10. Exit`: Salva a configuração final e sai da aplicação.

### Dados e Logs

* **Configuração (`smart_home/data/smart_house_config.json`):** Este arquivo armazena a configuração inicial do hub e seus dispositivos. A aplicação lê este arquivo ao iniciar e pode salvá-lo através do menu.
* **Log de Eventos (`smart_home/data/events_log.csv`):** Todas as mudanças de estado e eventos importantes são automaticamente registrados neste arquivo CSV para persistência e análise.
* **Relatórios (`smart_home/data/devices_report.csv`):** Os relatórios gerados são salvos neste arquivo.