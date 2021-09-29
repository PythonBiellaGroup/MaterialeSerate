# Creare connessioni tra tabelle M:N (many to many): Product e Tags
# https://sqlmodel.tiangolo.com/tutorial/many-to-many/
# e seguito
from typing import Optional, List
from sqlmodel import Field, SQLModel, Session,\
                     Relationship, create_engine, select


# Tabella di associazione tra Tag e Product
class TagProductLink(SQLModel, table=True):
    tag_id: Optional[int] = Field(
        default=None, foreign_key="tag.id", primary_key=True
    )
    product_id: Optional[int] = Field(
        default=None, foreign_key="product.id", primary_key=True
    )


class Tag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    # Relazione many con Product
    products: List["Product"] =\
        Relationship(back_populates="tags", link_model=TagProductLink)


class ProductType(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str


class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    product_type: Optional[int] = Field(default=None,
                                        foreign_key="producttype.id")
    # Relazione many con Tag
    tags: List["Tag"] =\
        Relationship(back_populates="products", link_model=TagProductLink)


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_entities():
    tag_offerta = Tag(name="Offerta")
    tag_maionese = Tag(name="Con Maionese")
    tag_no_maionese = Tag(name="Senza Maionese")
    tipo_panino = ProductType(name="panino")
    tipo_bibita = ProductType(name="bibita")
    with Session(engine) as session:
        session.add(tag_offerta)
        session.add(tag_maionese)
        session.add(tag_no_maionese)
        session.add(tipo_panino)
        session.add(tipo_bibita)
        session.commit()
        session.refresh(tag_offerta)
        session.refresh(tag_maionese)
        session.refresh(tag_no_maionese)
        session.refresh(tipo_panino)
        session.refresh(tipo_bibita)
        hamburger = Product(
            name="hamburger",
            product_type=tipo_panino.id,
            tags=[tag_offerta, tag_maionese]
        )
        coke = Product(
            name="Coca Cola",
            product_type=tipo_bibita.id,
            tags=[tag_offerta]
        )
        session.add(hamburger)
        session.add(coke)
        session.commit()
        session.refresh(hamburger)
        session.refresh(coke)
        print("Created :", hamburger)
        print("Created :", coke)


def update_burger():
    with Session(engine) as session:
        tag_no_maionese = session.exec(
            select(Tag).where(Tag.name == "Senza Maionese")
        ).one()
        tag_maionese = session.exec(
            select(Tag).where(Tag.name == "Con Maionese")
        ).one()
        hamburger = session.exec(
            select(Product).where(Product.name == "hamburger")
        ).one()
        hamburger.tags.append(tag_no_maionese)
        hamburger.tags.remove(tag_maionese)
        session.add(hamburger)
        session.commit()
        print("Updated hamburger:", hamburger.tags)
        print("Updated tags:", tag_maionese.products, tag_no_maionese.products)


def select_products():
    with Session(engine) as session:
        statement = select(Product, ProductType).\
            where(Product.product_type == ProductType.id)
        results = session.exec(statement)
        for product, product_type in results:
            print("product:", product, "product_type:",
                  product_type, "tags:", product.tags)


def main():
    create_db_and_tables()
    create_entities()
    update_burger()
    # select_products()


if __name__ == "__main__":
    main()
