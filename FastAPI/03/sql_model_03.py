# Creare connessioni tra tabelle 1:N Product e ProductType
# Lettura dati connessi
# https://sqlmodel.tiangolo.com/tutorial/connect/create-connected-tables/
# e seguito
from typing import Optional
from sqlmodel import Field, SQLModel, Session, create_engine, select


class Tag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str


class ProductType(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str


class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    product_type: Optional[int] = Field(default=None,
                                        foreign_key="producttype.id")


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_entities():
    tag_offerta = Tag(name="Offerta")
    tag_maionese = Tag(name="Con Maionese")
    tipo_panino = ProductType(name="panino")
    tipo_bibita = ProductType(name="bibita")
    with Session(engine) as session:
        session.add(tag_offerta)
        session.add(tag_maionese)
        session.add(tipo_panino)
        session.add(tipo_bibita)
        session.commit()
        session.refresh(tipo_panino)
        session.refresh(tipo_bibita)
        hamburger = Product(
            name="hamburger",
            product_type=tipo_panino.id,
        )
        coke = Product(
            name="Coca Cola",
            product_type=tipo_bibita.id,
        )
        session.add(hamburger)
        session.add(coke)
        session.commit()
        session.refresh(hamburger)
        session.refresh(coke)
        print("Created :", hamburger)
        print("Created :", coke)


def select_products():
    with Session(engine) as session:
        statement = select(Product, ProductType).\
            where(Product.product_type == ProductType.id)
        results = session.exec(statement)
        for product, product_type in results:
            print("product:", product, "product_type:", product_type)


def main():
    create_db_and_tables()
    create_entities()
    select_products()


if __name__ == "__main__":
    main()
