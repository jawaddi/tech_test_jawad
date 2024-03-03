from fastapi import FastAPI,HTTPException,Depends
from datetime import datetime
from decimal import Decimal
import uvicorn

from pydantic import BaseModel,Field
from uuid import UUID
# import models
# from database import engine,SessionLocal,Base
# from sqlalchemy.orm import Session

app = FastAPI()

# Base.metadata.create_all(bind=engine)

# def get_db():
#     try:
#         db = SessionLocal()
#         yield db

#     finally:
#         db.close()

#/////////// crud for clients/////////////
#////////////////////////////////////////
class Client(BaseModel):
    IdPersonne: int
    IdClasse  : int=Field(gt=-1)
    IdNatureIdt:int=Field(gt=-1)
    IdPays     :int=Field(gt=-1)
    NatureClient:str=Field(min_lenght=1)
    Etat        :str=Field(min_lenght=1)
    IdCategorieAvoir :int = Field(gt=-1)
    RaisonSociale    :str=Field(min_lenght=4)
    Matricule        :str=Field(min_lenght=4)

Clients = []


@app.get("/")
def read_clients():#db:Session=Depends(get_db)
    # return db.query(models.Clients).all()
    return Clients

@app.post("/client")
def create_new_client(client: Client):
    Clients.append(client)
    return client

@app.put("/{IdPersonne}")
def update_client(IdPersonne: int,client:Client):
    counter = 0

    for cln in Clients:
        counter+=1
        if cln.IdPersonne == client.IdPersonne:
            Clients[counter-1] = client 
            return Clients[counter-1]
    raise HTTPException(
        status_code =404,
        detail = f"IdPersonne {IdPersonne} :does not exist"
    ) 

@app.delete("/{IdPersonne}")
def delete_client(IdPersonne: UUID):
    counter = 0
    for cln in Clients:
        counter+=1
        if cln.IdPersonne == IdPersonne:
            del Clients[counter-1]
            return f"IdPersonne:{ cln.IdPersonne} deleted"


    raise HTTPException(
        status_code =404,
        detail = f"IdPersonne {IdPersonne} :does not exist"
    )


#/////////// crud for ComptEspece/////////////
#/////////////////////////////////////////////
# ComptEspece Columns ['IdCompte', 'IdClient', 'IdDepositaire', 'DateCreation', 'Web', 'Etat']

class ComptEspece(BaseModel):
    IdCompte: int=Field(gt=-1)
    IdClient  : int=Field(gt=-1)
    IdDepositaire:int=Field(gt=-1)
    DateCreation     : datetime
    Web:str=Field(min_lenght=1)
    Etat        :str=Field(min_lenght=1)

ComptEspeces = []


@app.get("/compteEspece")
def read_ComptEspece():#db:Session=Depends(get_db)
    # return db.query(models.Clients).all()
    return ComptEspeces

@app.post("/compteEspece")
def create_new_ComptEspece(comptEspece: ComptEspece):
    ComptEspeces.append(comptEspece)
    return comptEspece

@app.put("/compteEspece/{IdCompte}")
def update_compteEspece(IdCompte: int,comptEspece: ComptEspece):
    counter = 0

    for cte in ComptEspeces:
        counter+=1
        if cte.IdCompte == comptEspece.IdCompte:
            ComptEspeces[counter-1] = comptEspece 
            return ComptEspeces[counter-1]
    raise HTTPException(
        status_code =404,
        detail = f"IdPersonne {IdCompte} :does not exist"
    ) 

@app.delete("/compteEspece/{IdCompte}")
def delete_compteEspece(IdCompte: int):
    counter = 0
    for cte in ComptEspeces:
        counter+=1
        if cte.IdCompte == IdCompte:
            del ComptEspeces[counter-1]
            return f"IdCompte:{ cte.IdCompte} deleted"


    raise HTTPException(
        status_code =404,
        detail = f"IdCompte {IdCompte} :does not exist"
    )




#///////////// CRUD for  Transation //////////////
#//////////////////////////////////////////////// 
class ImputationsEspece(BaseModel):
    IdImputation        :int=Field(gt=-1)
    IdCompteEspece      :int=Field(gt=-1)
    Montant             :Decimal=Field(gt=0)
    Sens                :int=Field(gt=-1)
    DateImputation      :int=Field(gt=-1)
    IdDateImputation    :int=Field(gt=-1)
    IdSDBCompte         :int=Field(gt=-1)
    DateValeur          :datetime
    IdDateValeur        :int=Field(gt=-1)
    Nature              :str=Field(min_lenght=1)
    Etat                :int=Field(gt=-1)
    DateEtat            :datetime
    libelle             :str=Field(min_lenght=4)

# to collect our ImputationsEspeces
ImputationsEspeces = []
    


# read ImputationsEspeces
@app.get("/ImputationsEspece")
def read_ImputationsEspece():#db:Session=Depends(get_db)
    # return db.query(models.Clients).all()
    return ImputationsEspeces

# create ImputationsEspece
@app.post("/ImputationsEspece")
def create_new_ImputationsEspece(imputationsEspece: ImputationsEspece):
    ImputationsEspeces.append(imputationsEspece)
    return imputationsEspece


# update ImputationsEspece
@app.put("/ImputationsEspece/{IdImputation}")
def update_ImputationsEspece(IdImputation: int,imputationsEspece: ImputationsEspece):
    counter = 0

    for IEs in ImputationsEspeces:
        counter+=1
        if IEs.IdImputation == imputationsEspece.IdImputation:
            ImputationsEspeces[counter-1] = imputationsEspece 
            return ImputationsEspeces[counter-1]
    raise HTTPException(
        status_code =404,
        detail = f"IdImputation {IdImputation} :does not exist"
    ) 

# delete ImputationsEspece
@app.delete("/ImputationsEspece/{IdImputation}")
def delete_ImputationsEspece(IdImputation: int):
    counter = 0
    
    for IEs in ImputationsEspeces:
        counter+=1
        if IEs.IdImputation == IdImputation:
            del ImputationsEspeces[counter-1]
            return f"IdImputation:{ IEs.IdImputation} deleted"


    raise HTTPException(
        status_code =404,
        detail = f"IdImputation {IdImputation} :does not exist"
    )


# 
# if __name__ == "__main__":
#     uvicorn.run(app, host="localhost", port=8000, openapi_url="/docs")
