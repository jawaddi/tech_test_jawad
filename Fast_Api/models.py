from sqlalchemy import Column,Integer,String
from database import Base
from datetime import datetime
from decimal import Decimal



class CLIENTS(Base):
    __tablename__= 'Clients'

    IdPersonne = Column(Integer,primary_key=True,index=True)
    IdClasse  = Column(Integer)
    IdNatureIdt=Column(Integer)
    IdPays     =Column(Integer)
    NatureClient=Column(String)
    Etat        =Column(String)
    IdCategorieAvoir =Column(Integer)
    RaisonSociale    =Column(String)
    Matricule        =Column(String)

class COMPTESPECES(Base):
    __tablename__= 'ComptesEspece'
    IdCompte= Column(Integer,primary_key=True,index=True)
    IdClient  =Column(Integer)
    IdDepositaire=Column(Integer)
    DateCreation     : datetime
    Web=Column(String)
    Etat=Column(String)

class IMPUTATIONSESPECES(Base):
    __tablename__ = 'ImputationsEspeces'
    IdImputation        = Column(Integer,primary_key=True,index=True)
    IdCompteEspece      =Column(Integer)
    Montant             =Decimal
    Sens                =Column(Integer)
    DateImputation      =Column(Integer)
    IdDateImputation    =Column(Integer)
    IdSDBCompte         =Column(Integer)
    DateValeur          :datetime
    IdDateValeur        =Column(Integer)
    Nature              =Column(String)
    Etat                =Column(String)
    DateEtat            :datetime
    libelle             =Column(String)