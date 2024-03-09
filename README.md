# Project Title: Fan Token Price Analysis

## Overview & Methodology

This project delves into the intricate relationship between fan token prices and various factors like match results, influence of the benchmark index of cryptocurrency coins BTN, CIX100, and CHZ price fluctuations and club transfers (in and out). The study spans across the football seasons 18/19, 19/20, 20/21, 21/22, 22/23.

The project adopts a comprehensive approach, utilizing data mining tools like Selenium to gather detailed information on team game results, player transfers, and fan token prices. The collected data is then processed and utilized for constructing linear regression models. The scikit-learn library is employed for implementing these models, enabling efficient analysis of the relationship between fan token prices and the identified factors. The main idea is the calculation of the expected and abnormal returns for the fan tokens and the benchmark index coins, establishmend of the binary control variables for the linear equations (which are Win in Champions League, Loss in Champions League, Win in Europa League, Loss in Champions League, Win in Domestic Match, Loss in Domestic Match and Home, which states if the team of interest played home or away) and evaluation of the linear equations coefficients to show the dependency on individual control variables.

The inspiration for the project was the paper "Are Fan Tokens Fan Tokens?" published by the authors Ender Demir, Oguz Ersan and Boris Popesko (Finance Research Letters 2022)

## Data Sources

- Player transfers: [www.transfermarkt.com](www.transfermarkt.com)
- Fan token prices: [www.finance.yahoo.com](www.finance.yahoo.com)
- Benchmark index prices: Cryptocurrency coins (BTN, CIX100, CHZ) [www.finance.yahoo.com](www.finance.yahoo.com)

## Project Structure

1. **Data Collection:**
   - Utilize Selenium for web scraping to extract team game results, player transfers, and fan token prices.
   - Assemble benchmark index prices over time.

2. **Data Manipulation:**
   - Clean and preprocess the collected data for analysis.

3. **Linear Regressions:**
   - Utilize scikit-learn to implement linear regression models for each benchmark coin.
   - Incorporate control variables such as match outcomes, player transfers, and benchmark index prices.

4. **Visualization:**
   - Generate visualizations to illustrate relationships between variables.
   - Include time-series plots for benchmark index prices and fan token prices.

5. **Results:**
   - Present findings in a structured table using the Stargazer library.
   - Summarize key insights and their implications on fan token price dynamics.

## Script Order Execution

1. match_data_manipulation.ipynb
2. data_mining_transfers
3. token_prices_data_mining.ipynb
4. token_prices_data_manipulation.ipynb
5. merging_datasets_control_var.ipynb

## Output

The project provides insightful visualizations and statistical analyses, presenting the results in a tabular format using the Stargazer library. The output includes coefficients derived from linear regressions, R^2, adjusted R^2, residual standard error, and F statistic. These metrics collectively offer a comprehensive understanding of the statistical significance of control variables, indicating their impact on fan token price fluctuations.

## Tools and Libraries

- Python
- Pandas
- NumPy
- Matplotlib
- Stargazer (for tabular output)
- Selenium (for web scraping)
- Scikit-learn (for linear regression models)