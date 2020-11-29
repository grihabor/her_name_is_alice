# her_name_is_alice

Goal is to compare how many people were born with name Alice before 
and after the name was first used by Yandex.

## Data

https://data.mos.ru/opendata/7704111479-svedeniya-o-naibolee-populyarnyh-jenskih-imenah-sredi-novorojdennyh

## How to run

First download and extract the data. Then 

```bash
python3 -m venv venv
source venv/bin/activate
pip install .
alice data.csv | xargs xdg-open
```
