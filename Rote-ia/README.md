# Rote.IA: Plataforma Integrada Open-WebUI e Langflow - Projeto Skynet

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-25.0.3+-blue.svg)](https://www.docker.com/)
[![Docker-Compose](https://img.shields.io/badge/Docker_compose-2.24.6+-blue.svg)](https://docs.docker.com/compose/install/linux/)
[![Langflow](https://img.shields.io/badge/langflow-1.0.16+-blue.svg)](https://www.langflow.org/)
[![Open-webui](https://img.shields.io/badge/open%20webui-0.3.21+-blue.svg)](https://docs.openwebui.com/)
## Visão Geral

**Rote.IA** é uma plataforma totalmente integrada e containerizada, que combina o poder do [Open-WebUI](https://github.com/open-webui/open-webui) e do [Langflow](https://github.com/logspace-ai/langflow) para o desenvolvimento de aplicações baseadas em IA. Projetada com escalabilidade e flexibilidade em mente, esta plataforma utiliza Docker para garantir portabilidade e facilidade de implantação, permitindo que os desenvolvedores foquem na criação de soluções robustas de IA sem complicações na configuração do ambiente.

Este repositório contém as configurações do Docker Compose, que permitem executar ambos os serviços em harmonia, possibilitando experimentação com modelos de IA, processamento de dados e desenvolvimento de aplicações em um único ecossistema unificado.

### Principais Funcionalidades

- **Integração Perfeita**: Combina o Open-WebUI e o Langflow em um único ambiente Docker.
- **Armazenamento Persistente de Dados**: Garante a persistência de dados com volumes montados para ambos os serviços.
- **Pronto para Personalização**: Totalmente customizável, com um arquivo `.env` que facilita a configuração de chaves API, nomes e parâmetros do sistema.
- **Execução Automática e Sem Intervenção**: Projetado para ser executado em ambientes de produção com mínima intervenção manual.
- **Escalável e Extensível**: Pode ser usado como núcleo para pipelines baseados em IA maiores ou ser estendido com mais serviços conforme necessário.

## Tecnologias Utilizadas

- **Docker**: Containerização para ambientes isolados e reprodutíveis.
- **Open-WebUI**: Plataforma frontend para gerenciamento de modelos de IA.
- **Langflow**: Motor de fluxo de trabalho para gestão, execução e integração de serviços de IA.
- **Semantic-Router**: Roteador de serviços baseado em NLP.

## Como Começar

### Pré-requisitos

Certifique-se de que você tem os seguintes itens instalados:

- [Docker](https://www.docker.com/products/docker-desktop)
- [Docker Compose](https://docs.docker.com/compose/)

### Instruções de Configuração

1. Clone este repositório:
   ```bash
   git clone https://github.com/Jcnok/Desafio-Langflow.git
   cd Rote-ia
   ```

2. Crie um arquivo `.env` com as seguintes variáveis de ambiente ou utilize o arquivo env.example e depois renomeie para .env:

   ```bash
   WEBUI_NAME="Rote.ia"
   OPENAI_API_KEY="SUA_OPENAI_API_KEY"
   ```

3. Construa e execute os serviços utilizando Docker Compose:

   ```bash
   docker-compose up -d
   ```

4. Acesse os serviços via navegador:

   - **WebUI**: Acesse [http://localhost:8080](http://localhost:8080)
   - **Langflow**: Acesse [http://localhost:7860](http://localhost:7860)

### Parar os Serviços

Para parar e remover os containers:

```bash
docker-compose down
```

## Estrutura do Projeto

```
├── Flow/                     # Os json do projeto para a langflow
├── open-webui/
│   └── _data/                # Diretório de dados para WebUI
├── langflow/
│   └── data/                 # Diretório de dados para Langflow
├── webui_rote_ia_v2.json     # Função para integrar api langflow com open-webui
├── .env(env.example)         # Variáveis de ambiente (chaves API, configuração)
├── docker-compose.yaml       # Configuração do Docker Compose
└── README.md                 # Esta documentação
```

## Personalização

### Atualizando Dependências

O Langflow suporta pacotes Python adicionais, como `semantic-router`. Você pode atualizar ou adicionar outros pacotes modificando o comando no arquivo `docker-compose.yaml` na seção do serviço `langflow`:

```yaml
command: /bin/sh -c "pip install [NOVO_PACOTE] && python -m langflow run --host=0.0.0.0 --port=7860 --timeout=1800"
```

### Adicionando Novos Serviços

Para estender esta configuração com outros serviços, edite o arquivo `docker-compose.yaml` e defina novos containers na seção `services`. Serviços adicionais podem incluir um banco de dados, um message broker, ou endpoints de API personalizados.

## Diretrizes para Contribuição

Contribuições da comunidade são bem-vindas! Sinta-se à vontade para fazer um fork do repositório e abrir um pull request com melhorias, correções de bugs ou novas funcionalidades.

## Roteiro Futuro

- **Melhorias na UI/UX do WebUI**: Fornecer opções adicionais de customização para a interface do WebUI, de acordo com as necessidades específicas dos usuários.
- **Opções de Implantação Avançada**: Explorar a integração com Kubernetes para implementações distribuídas e em larga escala.

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## Contato

Para perguntas ou sugestões, entre em contato por e-mail: [suporte@rote-ia.com](mailto:julio.okuda@gmail.com.com)

