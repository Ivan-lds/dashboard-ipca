# Dashboard de Análise do IPCA 📊

## Descrição do Projeto 📝
Este projeto é um **dashboard interativo** desenvolvido em **Python**, utilizando bibliotecas como **Streamlit**, **Plotly** e **Pandas**. Ele fornece uma análise detalhada do **IPCA (Índice Nacional de Preços ao Consumidor Amplo)**, com dados obtidos diretamente da **API do IBGE**. O objetivo é apresentar visualizações dinâmicas e interativas para facilitar a análise do comportamento do IPCA ao longo do tempo, incluindo previsões e cenários de análise.

---

## Funcionalidades Principais 🚀
### 1. **Visualizações Gráficas** 📈
- **Gráfico de Barras:** Mostra a evolução mensal do IPCA de 2000 até 2025.
- **Gráfico de Pizza:** Representa a **distribuição porcentual acumulada** por categorias.
- **Gráfico de Barras Clusterizado:** Compara a variação mensal e acumulada por categorias.
- **Gráfico de Área:** Destaca valores positivos e negativos do IPCA com sombreamento diferenciado.
- **Gráfico de Boxplot:** Mostra a **distribuição do IPCA por ano** para identificar outliers e dispersões.
- **Análise de Cenários:** Inclui previsões de **cenários otimista, pessimista e esperado** para até 2026.
- **Animação Temporal:** Visualiza a evolução do IPCA ano a ano em um gráfico animado.

### 2. **Filtros Interativos** 🎛️
- **Filtro por Período:** Um **slider** permite selecionar um intervalo de anos específico para análise.
- **Filtro por Categorias:** Oferece um **multiselect** para filtrar visualizações com base em categorias específicas, como "Alimentação e Bebidas" e "Habitação".

### 3. **Métricas Principais** 📊
- **Média do IPCA em 2025.**
- **Variação acumulada total do IPCA de 2000 a 2025.**
- **Previsão acumulada do IPCA para 2026.**

### 4. **Resumo Estatístico** 📋
Apresenta uma tabela interativa com as seguintes estatísticas por ano:
- Média ➡️ 🧮
- Mediana ➡️ 📐
- Valor Mínimo ➡️ 📉
- Valor Máximo ➡️ 📈

---

## Tecnologias Utilizadas 💻
- **[Streamlit](https://streamlit.io/):** Framework para criar aplicações web interativas com Python.
- **[Plotly](https://plotly.com/python/):** Ferramenta para criar gráficos dinâmicos e interativos.
- **[Pandas](https://pandas.pydata.org/):** Biblioteca para manipulação e análise de dados.
- **[Statsmodels](https://www.statsmodels.org/stable/index.html):** Utilizada para criar previsões usando o modelo **Holt-Winters**.
- **[Requests](https://docs.python-requests.org/):** Para obter dados da API do IBGE.

---

## Estrutura do Código 🛠️
1. **Coleta de Dados:**
   - Dados do IPCA são baixados diretamente da API do IBGE.
   - Processamento dos dados em um DataFrame para facilitar a análise e visualização.

2. **Previsões:**
   - Previsão de valores futuros (até 2026) usando o modelo **Holt-Winters Exponential Smoothing**.

3. **Filtros Interativos:**
   - Sidebar com widgets para aplicar filtros de **período** e **categorias**.

4. **Visualizações:**
   - Gráficos dinâmicos gerados com **Plotly** (ex.: barras, pizza, boxplot, etc.).
   - Gráfico combinado para análise de cenários.

5. **Resumo Estatístico:**
   - Tabela com estatísticas como média, mediana, mínimo e máximo do IPCA por ano.

---

## Como Usar 🛡️
### Requisitos 📦
Antes de executar o projeto, você precisa ter:
- Python 3.8 ou superior instalado.
- As bibliotecas Python abaixo:
  ```bash
  pip install streamlit pandas plotly statsmodels requests
  ```

### Execução ▶️
1. Clone ou baixe este repositório.
2. Execute o comando abaixo para iniciar o Streamlit:
   ```bash
   streamlit run app.py
   ```
3. Acesse o dashboard no navegador através do endereço exibido (geralmente `http://localhost:8501`).

---

## Melhorias Futuras 🔮
- Adicionar **mapas interativos** mostrando o IPCA por estado ou região do Brasil. 🗺️
- Criar **alertas automáticos** baseados em variações significativas do IPCA. 🚨
- Incorporar novas APIs para complementar os dados (ex.: dados econômicos internacionais). 🌍
- Habilitar a exportação de gráficos e dados para arquivos CSV ou PDF. 📤

---

## Contribuição 🤝
Sinta-se à vontade para abrir **issues** ou enviar **pull requests** com melhorias e sugestões. Toda contribuição é muito bem-vinda! 🌟

---

## Contato
Criado por Ivan Lima. Caso tenha dúvidas ou feedback, entre em contato:
- **Email:** ivanlimadossantos4@gmail.com
- **LinkedIn:** https://www.linkedin.com/in/ivan-lima-a28335186/

---

Este README foi feito para que seja fácil compreender o propósito, as funcionalidades e os detalhes técnicos do projeto. 🚀📊✨
