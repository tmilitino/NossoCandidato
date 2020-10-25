import postgresql
import configparser
import pandas as pd
import os


config = configparser.ConfigParser()
file = config.read("CONFIG/GERAL.CFG")

user = config["DEFAULT"]["user"]
senha = config["DEFAULT"]["pass"]
host = config["DEFAULT"]["host"]
port = config["DEFAULT"]["port"]
database = config["DEFAULT"]["database"]

path="base/consulta_legendas_2014"
data = list()

t = os.listdir(path)


db = postgresql.open(f'pq://{user}:{senha}@{host}:{port}/{database}')

ListaLegendas = [f for f in os.listdir(path) if os.path.isfile(f"{path}/{f}")]

for arquivo in ListaLegendas:
    with open(f"{path}/{arquivo}",'r') as myfile:
        arq = myfile.readlines()
        head = arq[0].replace("\n","").replace('"',"").split(";")
        for line in arq[1:]:
          data.append(line.replace("\n","").replace('"',"").split(";"))


df = pd.DataFrame(data, columns=head)

dfLegenda = df[["NR_PARTIDO","SG_PARTIDO","NM_PARTIDO"]].drop_duplicates().reset_index()

insertLegenda = db.prepare('INSERT INTO partidos (legenda, nome_partido, sigla) VALUES($1,$2,$3)')

dfLegenda.apply( lambda x: insertLegenda(int(x["NR_PARTIDO"]),x["NM_PARTIDO"],x["SG_PARTIDO"]),axis=1)

