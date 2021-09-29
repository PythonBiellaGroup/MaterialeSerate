# Creazione entità "base", editor support, creazione, id automatici
# https://sqlmodel.tiangolo.com/tutorial/insert/
from typing import Optional
from sqlmodel import Field, SQLModel, Session, create_engine


class Tag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str


class ProductType(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_entities():
    tag_offerta = Tag(name="Offerta")
    tag_maionese = Tag(name="Con Maionese")
    tag_nomayo = Tag(name="No mayo")
    tipo_panino = ProductType(name="panino")
    tipo_bibita = ProductType(name="bibita")
    with Session(engine) as session:
        session.add(tag_offerta)
        session.add(tag_maionese)
        session.add(tag_nomayo)
        session.add(tipo_panino)
        session.add(tipo_bibita)
        session.commit()
        print("After committing the session")
        print("Tag 1:", tag_offerta)
        # No refresh, no print
        # https://sqlmodel.tiangolo.com/tutorial/automatic-id-none-refresh/
        print("Product Type 1:", tipo_panino)
        # Refresh automatica se accedo ad un attributo
        print("Name of product Type 1:", tipo_panino.name)
        # Refresh esplicita
        session.refresh(tipo_bibita)
        session.refresh(tag_maionese)
        print("Product Type 2:", tipo_bibita)
    print("After the session closes")
    print("Tag 2:", tag_maionese)


def main():
    create_db_and_tables()
    create_entities()


if __name__ == "__main__":
    main()
