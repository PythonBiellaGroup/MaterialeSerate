# 01 SQL MODEL E FASTAPI
# https://sqlmodel.tiangolo.com/tutorial/fastapi/simple-hero-api/
from typing import Optional, List
from fastapi import FastAPI
from sqlmodel import Field, SQLModel, Session, Relationship,\
                     create_engine, select
import uvicorn


# Tabella di associazione n:n tra Tag e Product
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
    products: List["Product"] = Relationship(
        back_populates="tags",
        link_model=TagProductLink
        )


class ProductType(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str


class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    product_type: Optional[int] = Field(
        default=None,
        foreign_key="producttype.id"
        )
    tags: List["Tag"] = Relationship(
        back_populates="products",
        link_model=TagProductLink
        )


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/tags/")
def create_tag(tag: Tag):
    with Session(engine) as session:
        session.add(tag)
        session.commit()
        session.refresh(tag)
        return tag


@app.post("/product_types/")
def create_product_type(product_type: ProductType):
    with Session(engine) as session:
        session.add(product_type)
        session.commit()
        session.refresh(product_type)
        return product_type


@app.post("/products/")
def create_product(product: Product):
    with Session(engine) as session:
        session.add(product)
        session.commit()
        session.refresh(product)
        return product


# Le API docs UI non conoscono lo schema
@app.get("/products/")
def read_products():
    with Session(engine) as session:
        products = session.exec(select(Product)).all()
        return products


if __name__ == '__main__':
    uvicorn.run(app, port=8000, host='127.0.0.1')
# In dev, può essere comodo lanciare con
# uvicorn main:app --reload
