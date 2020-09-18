# BDDQuery 🕵🏼‍♀️

BDDQuery é um cliente desenvolvido para publicação dos dados no BigQuery da Base dos Dados. O intuito do projeto é **facilitar o acesso a dados brasileiros através de tabelas públicas no BigQuery**. 

Qualquer pessoa poderá fazer queries em bases tratadas, documentadas e estáveis - uma simples consulta de SQL será o suficiente para cruzamento das bases que você precisa.

## Porque o BigQuery?

Sabemos que estruturar os dados em uma plataforma privada não é o ideal para um projeto de dados abertos. Porém o BigQuery oferece uma infraestrutura com algumas vantagens:

- É possível deixar os dados públicos, i.e., qualquer pessoa com uma conta no Google Cloud pode fazer uma query na base, quando quiser
- O usuário (quem faz a query) paga por ela. Isso deixa os custos do projeto bem baixos
- O BigQuery escala magicamente para hexabytes se necessário
- O custo é praticamente zero para usuários. São cobrados somente 5 dólares por terabyte de dados que sua query percorrer, e os primeiros 5 terabytes são gratuitos.

## Como publicar dados?
**Incentivamos que outras instituições e pessoas contribuam**. Nosso únicos requerimentos são:
- Processo de captura e tratamento dos dados deve estar público e documentado
- Inserção dos dados no BigQuery deve seguir [nossa metodologia](#Como-organizar-as-bases-no-BigQuery?)

## 1. Instale o cliente localmente

```sh
make create-env
. .bases/bin/activate
```
## 2. TODO: organizar os passos


## Como organizar as bases no BigQuery?

As bases tem que ser organizadas no BigQuery de maneira consistente, que permita uma busca fácil e intuitiva, e seja escalável.

Para isso, existem dois níveis de organização: _datasets_ e _tables_, nos quais:
- Todas as tabelas devem estar organizadas em _datasets_
- Cada tabela deve pertencer a um único _dataset_

As diretrizes para nomenclatura dos _datasets_ e tabelas são descritas abaixo:

|           | Dataset                      | Tabela                           |
|-----------|-----------------------------|----------------------------------|
| Mundial   | mundo_\<tema\>_\<instituicao\>      | \<descrição\>                        |
| Federal   | \<pais\>_\<tema\>_\<instituicao\>       | \<descrição\>                       |
| Estadual  | \<pais\>_\<estado\>                 | \<instituicao\>_\<tema\>_descrição\>       |
| Municipal | \<pais\>_\<estado\>_\<cidade\>          | \<instituicao\>_\<tema\>_descrição\>       |

- Utilizar somente letras minúsculas
- Remover acentos, pontuações e espaços

### Bases Desejadas

[Lista de bases mapeadas](https://docs.google.com/spreadsheets/d/1t9kEsiyatmmdDCy2qjaCjLqdw-oJj33P7tY5bnkR0aw/edit#gid=0) que estão no nosso mapa.


## Mundial -- Clima, Waze

### Dataset:

Usar abrangência, um tema e nome da instituição

`mundo_<tema>_<instituicao>`

### Tabela:

Usar nome descritivo e único para os dados

`<descrição>`

Exemplo: Os dados de alertas do Waze estariam no dataset `mundo_mobilidade_waze` e tabela `alertas`. Portanto, o caminho seria `mundo_mobilidade_waze`.`alertas`.

## Federal -- IBGE, IPEA, Senado, Camara, TSE

### Dataset:

Usar sigla do país, um tema e nome da instituição

`<pais>_<tema>_<instituicao>`

### Tabela:

Usar nome descritivo e único para os dados:

`<descrição>`

Exemplo: Os dados de candidatos do TSE estariam no dataset `br-eleicoes-tse` e na tabela `candidatos`.

## Estadual 

### Dataset:

Usar país e sigla do estado (UF).

`<pais>_<estado>`

### Tabela:

Usar nome da instuição estadual, tema e descrição

`<instituicao>_<tema>_<descrição>`


Exemplo: Os dados da rede de esgoto da SANASA que atende no estado de São Paulo estariam no dataset `br-sp` e tabela `sanasa-sanementobasico-redeesgoto`.

## Municipal

### Dataset:

Usar sigla do país, sigla do estado (UF), nome da cidade (sem espaço)

`<pais>_<estado>_<cidade>`

### Tabela:

Usar nome da instuição estadual, tema e descrição

`<instituicao>_<tema>_<descrição>`

Exemplo: Os dados de votações da camara municipal do rio de janeiro estariam em `br-rj-riodejaneiro` e tabela `dcmrj-legislativo-legislativo`

## Tabela de Temas e Identificadores

A referencia dos temas é do dados.gov.br, mas temas podem ser adicionados e trocados. Identificadores serão adicionados de acordo com demanda.
| Tema                                | Identificador |
|-------------------------------------|---------------|
| Legislativo                         | legislativo   |
| Saúde                               | saude         |
| Educação                            | educacao      |
| Eleições                            | eleicoes      |
| Governo e Política                  |               |
| Agricultura, extrativismo e pesca   |               |
| Economia e Finanças                 |               |
| Pessoa, Familia e Sociedade         |               |
| Equipamentos Públicos               |               |
| Plataforma de Gestão de Indicadores |               |
| Cultura, Lazer e Esporte            |               |
| Plano Plurianual                    |               |
| Trabalho                            |               |
| Transportes e Trânsito              |               |
| Comércio, Serviços e Turismo        |               |
| Defesa e Segurança                  |               |
| Meio Ambiente                       |               |
| Indústria                           |               |
| Geografia                           |               |
| Ciência, Informação e Comunição     |               |
| Fornecedores do Governo Federal     |               |
| Habitação, Saneamento e Urbanismo   |               |


# Estrutura do Github

A pasta `bases/` terá uma estrutura similar a do BigQuery.

```
    ├── bases
        ├── <nome_dataset>             Ex: br_eleicoes_tse
        ├── ...
            ├── code/                 Todo código relacionado ao dataset
            ├── <dataset_config.yaml>
            ├── <nome_tabela>.yaml    Ex: candidatos.yaml
            ├── ...
```

Os arquivos `.yaml` serão usados para documentação e configuração das tabelas e datasets.

### dataset_config.yaml

```yaml
name: br_eleicoes_tse
description: |
    Dados do Tribunal Superior Eleitoral disponíveis na url ...
labels: 
    - eleicoes
    - politica
    - candidatos
```

### <nome_tabela>.yaml

```yaml
owner: 
    name: Curio # Ou qualquer outra instituição/ pessoa
    contact: curio-issues
code: <code-that-generated-table-url>
name: candidatos
description: |
    Candidatos das eleições federais e municipais de 2010 até 2020

    Tratamentos:
     - ...
labels:
    - eleicoes
    - candidatos
    - politica
columns:
    ANO:
        description: asdfsfasf
        type: INTEGER
        treated?: False # A coluna foi modificada (exceto mudançã de tipos)?
    NOME:
        description: asdfsfasf
        type: STRING
        treated?: False # A coluna foi modificada (exceto mudançã de tipos)?
```

# Estrutura no Storage

A estrutura deve seguir a mesma lógica do BigQuery. Porém, existem pastas raízes diferentes: os dados brutos devem ser alocados em `raw` e prontos em `ready`. Ambas possuem a mesma estrutura:

```
    ├── ready|raw
        ├── <nome_dataset>        Ex: br_eleicoes_tse
        ├── ...
            ├── <nome_tabela>    Ex: candidatos
            ├── ...
                ├── <dados>      Dados particionados ou não.
```

Nem todos os dados necessitam estar na pasta `raw`. Essa pasta existe somente para aqueles que precisam de um processamento prévio. 

# Tratamento no Bigquery

O BigQuery é uma ótima ferramenta para tratar as bases. Portanto, recomenda-se
que subir os dados brutos e usar uma query para tratá-los. Seja para corrigir tipos
ou adicionar colunas úteis.

Para isso, deverá ser criado uma dataset com o mesmo nome, mas precedido de `raw_`.

Exemplo: `raw_br_eleicoes_tse`

E todas as tabelas desse dataset serão consideradas brutas e não deverão ser abertas
ao público.

# Regras de Tratamento das Bases

- Nunca editar os valores da base. Se for o caso de tratar uma coluna, adicionar uma nova coluna com os dados tratados.

- Os tipos do BigQuery devem ser usados apropriadamente.

- Códigos dos Municípios e Estados brasileiros devem seguir o padrão do IBGE.

- Não normalizar campos de texto usando maíusculas.

- O código para reproduzir o tratamento deve ser aberto.

- Valores nulos devem ser convertidos para `None`.

# Idiomas

Toda documentação estará em português (quando possível). O código e configurações estará em inglês.
