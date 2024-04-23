# vera_project

## Github repo
https://github.com/hgao62/vera_project.git
### Task 1
* 1. create main.py, extract_data.py, load_data.py
* 2. create requirments.txt file that has contents below
```
SQLAlchemy==1.4.52
yfinance==0.2.37
pandas>=1.3.0
```
* 3. run pip install -r requirements.txt
* 4. create two functions in extrac_data.py see below

```python
def get_stock_history(stock):
    '''this function should pull stock history given a stock input,
       please follow this link to get example on how to use yahoo finance api
       https://github.com/ranaroussi/yfinance
    '''


```
it should return a data frame like this below

<!-- ![stock history](stock_history_output.png) -->
<img alt="stock history" src="./stock_history_output.png" width="1000">

```python
def get_stock_financials(stock):
    '''this function should get share holders of a stock given a stock input,
       please follow this link to get example on how to use yahoo finance api
       https://github.com/ranaroussi/yfinance
    '''

```
it should return a data frame like this below

<img alt="stock financial" src="./stock_financial.png" width="1500">


When creating functions, please add type hinting and doc string like below

<img alt="stock financial" src="./type_hinting.png" width="1000">


### Task 2
```python
1. add function below to extract_data.py
def get_exchange_rate(stock, period, interval, to_currency):
    # 1 get currency code of the stock
    ticker = yf.Ticker(stock)
    currency_code = ticker.fast_info["currency"]
    fx_rate_ticker = f'{currency_code}{to_currency}=X'
    fx_rates = yf.download(fx_rate_ticker,period=period, interval=interval)


get_exchange_rate("AAPL", period="5d", interval="1d", "GBP")

```
and output should look like below

<img alt="stock financial" src="./exchange_rate.png" width="1000">

```python
2. add function below to extract_data.py
def get_news(stock):
```
and output should look like below

<img alt="stock financial" src="./news.png" width="1000">



## How to set up airflow
#### 1. build image and create a container based on the image just  created
```docker
  docker-compose up --build
````



### Useful docker  commands
1. list all local images
```docker
docker image ls

````


### Useful Airflow  commands
1. start airflow scheduler
```
airflow scheduler

````
2. list all dags
```
airflow dags list
```