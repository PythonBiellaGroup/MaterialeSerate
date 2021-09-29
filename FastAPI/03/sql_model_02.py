# Lettura dati con SQLModel, all, first, one; update; delete
# https://sqlmodel.tiangolo.com/tutorial/select/ e seguito
from typing import Optional
from sqlmodel import Field, SQLModel, Session, create_engine, select


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
    tipo_panino = ProductType(name="panino")
    tipo_bibita = ProductType(name="bibita")
    with Session(engine) as session:
        session.add(tag_offerta)
        session.add(tag_maionese)
        session.add(tipo_panino)
        session.add(tipo_bibita)
        session.commit()
        print("After committing the session")
        print("Tag 1:", tag_offerta)
        # No refresh, no print
        print("Product Type 1:", tipo_panino)
        # Refresh automatica
        print("Product Type 1:", tipo_panino.name)
        # Refresh esplicita
        session.refresh(tipo_bibita)
        session.refresh(tag_maionese)
        print("Product Type 2:", tipo_bibita)
    print("After the session closes")
    print("Tag 2:", tag_maionese)


def select_product_types():
    with Session(engine) as session:
        statement = select(ProductType)
        results = session.exec(statement)
        for product_type in results:
            print("product_type:", product_type)


def select_product_type_panino():
    with Session(engine) as session:
        statement = select(ProductType).where(ProductType.name == 'panino')
        results = session.exec(statement)
        for product_type in results:
            print("panino:", product_type)


def select_first_row_tag():
    with Session(engine) as session:
        statement = select(Tag).where(Tag.name == 'Offerta')
        results = session.exec(statement)
        tag = results.first()
        print("first:", tag)


def select_all_tags():
    with Session(engine) as session:
        statement = select(Tag)
        results = session.exec(statement)
        tags = results.all()
        print(tags)


def select_four_tags():
    with Session(engine) as session:
        statement = select(Tag).limit(4)
        results = session.exec(statement)
        tags = results.all()
        print(tags)


def select_next_four_tags():
    with Session(engine) as session:
        statement = select(Tag).offset(4).limit(4)
        results = session.exec(statement)
        tags = results.all()
        print(tags)


def update_tag():
    with Session(engine) as session:
        statement = select(Tag).where(Tag.name == "Con Maionese")
        results = session.exec(statement)
        # mayo = results.one()
        mayo = results.first()
        print("Tag:", mayo)
        mayo.name = "Senza Maionese"
        session.add(mayo)
        session.commit()
        session.refresh(mayo)
        print(mayo)


def delete_tag():
    with Session(engine) as session:
        statement = select(Tag).where(Tag.name == "Senza Maionese")
        results = session.exec(statement)
        no_mayo = results.first()
        print("no_mayo: ", no_mayo)
        session.delete(no_mayo)
        session.commit()
        print("Deleted:", no_mayo)
        statement = select(Tag).where(Tag.name == "Senza Maionese")
        results = session.exec(statement)
        no_mayo = results.first()
        if no_mayo is None:
            print("There's no no_mayo")


def main():
    create_db_and_tables()
    create_entities()
    # select_product_types()
    # select_product_type_panino()
    # select_first_row_tag()
    # select_all_tags()
    # select_four_tags()
    # select_next_four_tags()
    # update_tag()
    delete_tag()


if __name__ == "__main__":
    main()
