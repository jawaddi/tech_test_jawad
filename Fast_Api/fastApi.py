from fastapi import FastAPI,HTTPException,Depends
from datetime import datetime
from decimal import Decimal
from sqlalchemy.exc import SQLAlchemyError

import uvicorn
import models

from pydantic import BaseModel,Field
from uuid import UUID
# import models
from database import engine,SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

# create the database if ie doesn't exist
models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db=SessionLocal()
        yield db
    finally:
        db.close()

#/////////// crud for clients/////////////
#////////////////////////////////////////
class Client(BaseModel):
    # IdPersonne: int
    IdClasse  : int
    IdNatureIdt:int
    IdPays     :int
    NatureClient:str
    Etat        :str
    IdCategorieAvoir :int 
    RaisonSociale    :str
    Matricule        :str

Clients = []


@app.get("/")
def read_clients(db: Session=Depends(get_db)):#db:Session=Depends(get_db)
    # return db.query(models.Clients).all()
    return db.query(models.CLIENTS).all()
    # return Clients

# @app.post("/client")
# def create_new_client(client: Client,db: Session=Depends(get_db)):
#     client_model = models.CLIENTS()
#     client_model.IdClasse = client.IdClasse
#     client_model.IdNatureIdt = client.IdNatureIdt
#     client_model.IdPays = client.IdPays
#     client_model.NatureClient = client.NatureClient
#     client_model.Etat = client.Etat
#     client_model.IdCategorieAvoir = client.IdCategorieAvoir
#     client_model.RaisonSociale = client.RaisonSociale
#     client_model.Matricule = client.Matricule
#     db.add(client_model)
#     db.commit()
#     return client
@app.post("/client")
def create_new_client(client: Client, db: Session = Depends(get_db)):

        client_model = models.CLIENTS()
        client_model.IdClasse = client.IdClasse
        client_model.IdNatureIdt = client.IdNatureIdt
        client_model.IdPays = client.IdPays
        client_model.NatureClient = client.NatureClient
        client_model.Etat = client.Etat
        client_model.IdCategorieAvoir = client.IdCategorieAvoir
        client_model.RaisonSociale = client.RaisonSociale
        client_model.Matricule = client.Matricule

        db.add(client_model)
        db.commit()
        # db.refresh(client_model)  # Refresh to get the updated instance

        return "new cleint has been added"

@app.put("/{IdPersonne}")
def update_client(IdPersonne: int,client:Client,db: Session=Depends(get_db)):
    client_model = db.query(models.CLIENTS).filter(models.CLIENTS.IdPersonne==IdPersonne).first()
    if client_model is None:
            raise HTTPException(
                status_code=404,
                detail=f"The book with id {book_id} was not found"
            )
    # client_model = models.CLIENTS()
    client_model.IdClasse = client.IdClasse
    client_model.IdNatureIdt = client.IdNatureIdt
    client_model.IdPays = client.IdPays
    client_model.NatureClient = client.NatureClient
    client_model.Etat = client.Etat
    client_model.IdCategorieAvoir = client.IdCategorieAvoir
    client_model.RaisonSociale = client.RaisonSociale
    client_model.Matricule = client.Matricule
    db.add(client_model)
    db.commit()
    return f"the clinet with id {IdPersonne} has been updated"

@app.delete("/{IdPersonne}")
def delete_client(IdPersonne: int,db: Session=Depends(get_db)):
    client_model = db.query(models.CLIENTS).filter(models.CLIENTS.IdPersonne==IdPersonne).first()
    if client_model is None:
            raise HTTPException(
                status_code=404,
                detail=f"The book with id {IdPersonne} was not found"
            )

    client_model = db.query(models.CLIENTS).filter(models.CLIENTS.IdPersonne==IdPersonne).delete()
    db.commit()

    return f"the client with the number {IdPersonne} has been deleted"


#/////////// crud for ComptEspece/////////////
#/////////////////////////////////////////////
# ComptEspece Columns ['IdCompte', 'IdClient', 'IdDepositaire', 'DateCreation', 'Web', 'Etat']

class ComptEspece(BaseModel):
    # IdCompte: int=Field(gt=-1)
    IdClient  : int
    IdDepositaire:int
    DateCreation: datetime
    Web:str
    Etat:str

ComptEspeces = []


@app.get("/compteEspece")
def read_ComptEspece(db: Session=Depends(get_db)):#db:Session=Depends(get_db)
    return db.query(models.COMPTESPECES).all()
    # return ComptEspeces

@app.post("/compteEspece")
def create_new_ComptEspece(comptEspece: ComptEspece,db: Session=Depends(get_db)):
    comptEspece_model = models.COMPTESPECES()
    comptEspece_model.IdClient = comptEspece.IdClient 
    comptEspece_model.IdDepositaire = comptEspece.IdDepositaire
    comptEspece_model.DateCreation = comptEspece.DateCreation
    comptEspece_model.Web = comptEspece.Web
    comptEspece_model.Etat=comptEspece.Etat
    db.add(comptEspece_model)
    db.commit()

    return "new compteEspece has been added"

@app.put("/compteEspece/{IdCompte}")
def update_compteEspece(IdCompte: int,comptEspece: ComptEspece,db: Session=Depends(get_db)):
    # fist check if that compte we want to update is exist or not
    compteEspece_model = db.query(models.COMPTESPECES).filter(models.COMPTESPECES.IdCompte==IdCompte).first()
    if compteEspece_model is None:
        raise HTTPException(
            status_code=404,
                detail=f"The book with id {IdCompte} was not found"
        )


    # update compteEspece
    comptEspece_model = models.COMPTESPECES()
    comptEspece_model.IdClient = comptEspece.IdClient 
    comptEspece_model.IdDepositaire = comptEspece.IdDepositaire
    comptEspece_model.DateCreation = comptEspece.DateCreation
    comptEspece_model.Web = comptEspece.Web
    comptEspece_model.Etat=comptEspece.Etat

    # insert to the db
    db.add(comptEspece_model)
    db.commit()
    
    # feedback
    # return f"the imputationsEspece with id {IdCompte} has been updated"

@app.delete("/compteEspece/{IdCompte}")
def delete_compteEspece(IdCompte: int,db: Session=Depends(get_db)):
    compteEspece_model = db.query(models.COMPTESPECES).filter(models.COMPTESPECES.IdCompte==IdCompte).first()
    if compteEspece_model is None:
            raise HTTPException(
                status_code=404,
                detail=f"The book with id {IdCompte} was not found"
            )

    compteEspece_model = db.query(models.COMPTESPECES).filter(models.COMPTESPECES.IdCompte==IdCompte).delete()
    db.commit()

    return f"the compteEspece with the number {IdCompte} has been deleted"



#///////////// CRUD for  Transation //////////////
#//////////////////////////////////////////////// 
class ImputationsEspece(BaseModel):
    # IdImputation        :int=Field(gt=-1)
    IdCompteEspece      :int
    Montant             :Decimal
    Sens                :int
    DateImputation      :int
    IdDateImputation    :int
    IdSDBCompte         :int
    DateValeur          :datetime
    IdDateValeur        :int
    Nature              :str
    Etat                :int
    DateEtat            :datetime
    libelle             :str

# to collect our ImputationsEspeces
ImputationsEspeces = []
    


# read ImputationsEspeces
@app.get("/ImputationsEspece")
def read_ImputationsEspece(db:Session=Depends(get_db)):#db:Session=Depends(get_db)
    return db.query(models.IMPUTATIONSESPECES).all()
    # return ImputationsEspeces

# create ImputationsEspece
@app.post("/ImputationsEspece")
def create_new_ImputationsEspece(imputationsEspece: ImputationsEspece,db: Session=Depends(get_db)):
    imputationsEspece_model = models.IMPUTATIONSESPECES()
    # imputationsEspece_model.IdCompteEspece=imputationsEspece.IdCompteEspece
    
    imputationsEspece_model.Montant = imputationsEspece.Montant
    imputationsEspece_model.Sens    = imputationsEspece.Sens
    imputationsEspece_model.DateImputation = imputationsEspece.DateImputation
    imputationsEspece_model.IdDateImputation = imputationsEspece.IdDateImputation
    imputationsEspece_model.IdSDBCompte      =imputationsEspece.IdSDBCompte
    imputationsEspece_model.DateValeur       = imputationsEspece.DateValeur
    imputationsEspece_model.IdDateValeur     = imputationsEspece.IdDateValeur
    imputationsEspece_model.Nature           = imputationsEspece.Nature
    imputationsEspece_model.Etat             = imputationsEspece.Etat
    imputationsEspece_model.DateEtat         = imputationsEspece.DateEtat
    imputationsEspece_model.libelle          = imputationsEspece.libelle
    db.add(imputationsEspece_model)
    db.commit()

    return "new imputationsEspecethe has been added"

# update ImputationsEspece
@app.put("/ImputationsEspece/{IdImputation}")
def update_ImputationsEspece(IdImputation: int,imputationsEspece: ImputationsEspece,db: Session=Depends(get_db)):
    ImputationsEspece_model = db.query(models.IMPUTATIONSESPECES).filter(models.IMPUTATIONSESPECES.IdImputation==IdImputation).first()
    if ImputationsEspece_model is None:
            raise HTTPException(
                status_code=404,
                detail=f"The book with id {book_id} was not found"
            )
    
    imputationsEspece_model = models.IMPUTATIONSESPECES()
    # imputationsEspece_model.IdCompteEspece=imputationsEspece.IdCompteEspece
    
    imputationsEspece_model.Montant = imputationsEspece.Montant
    imputationsEspece_model.Sens    = imputationsEspece.Sens
    imputationsEspece_model.DateImputation = imputationsEspece.DateImputation
    imputationsEspece_model.IdDateImputation = imputationsEspece.IdDateImputation
    imputationsEspece_model.IdSDBCompte      =imputationsEspece.IdSDBCompte
    imputationsEspece_model.DateValeur       = imputationsEspece.DateValeur
    imputationsEspece_model.IdDateValeur     = imputationsEspece.IdDateValeur
    imputationsEspece_model.Nature           = imputationsEspece.Nature
    imputationsEspece_model.Etat             = imputationsEspece.Etat
    imputationsEspece_model.DateEtat         = imputationsEspece.DateEtat
    imputationsEspece_model.libelle          = imputationsEspece.libelle

    db.add(imputationsEspece_model)
    db.commit()
    return f"the imputationsEspece with id {IdImputation} has been updated"


# delete ImputationsEspece
@app.delete("/ImputationsEspece/{IdImputation}")
def delete_ImputationsEspece(IdImputation: int,db: Session=Depends(get_db)):
    ImputationsEspece_model = db.query(models.IMPUTATIONSESPECES).filter(models.IMPUTATIONSESPECES.IdImputation==IdImputation).first()
    if ImputationsEspece_model is None:
            raise HTTPException(
                status_code=404,
                detail=f"The book with id {IdImputation} was not found"
            )

    ImputationsEspece_model = db.query(models.IMPUTATIONSESPECES).filter(models.IMPUTATIONSESPECES.IdImputation==IdImputation).delete()
    db.commit()

    return f"the ImputationsEspece with the number {IdImputation} has been deleted"
# 
# if __name__ == "__main__":
#     uvicorn.run(app, host="localhost", port=8000, openapi_url="/docs")
