# PROBLEMA: in docs non si vede lo schema
# 02 AGGIUNGIAMO I "RESPONSE MODEL"
# https://sqlmodel.tiangolo.com/tutorial/fastapi/response-model/
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
    products: List["Product"] =\
        Relationship(back_populates="tags", link_model=TagProductLink)


class ProductType(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str


class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    product_type: Optional[int] =\
        Field(default=None, foreign_key="producttype.id")
    tags: List["Tag"] =\
        Relationship(back_populates="products", link_model=TagProductLink)


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/tags/", response_model=Tag)
def create_tag(tag: Tag):
    with Session(engine) as session:
        session.add(tag)
        session.commit()
        session.refresh(tag)
        return tag


@app.post("/product_types/", response_model=ProductType)
def create_product_type(product_type: ProductType):
    with Session(engine) as session:
        session.add(product_type)
        session.commit()
        session.refresh(product_type)
        return product_type


@app.post("/products/", response_model=Product)
def create_product(product: Product):
    with Session(engine) as session:
        session.add(product)
        session.commit()
        session.refresh(product)
        return product


# Ora le API docs UI conoscono lo schema
@app.get("/tags/", response_model=List[Tag])
def read_tags():
    with Session(engine) as session:
        tags = session.exec(select(Tag)).all()
        return tags


@app.get("/product_types/", response_model=List[ProductType])
def read_product_types():
    with Session(engine) as session:
        product_types = session.exec(select(ProductType)).all()
        return product_types


@app.get("/products/", response_model=List[Product])
def read_products():
    with Session(engine) as session:
        products = session.exec(select(Product)).all()
        return products


if __name__ == '__main__':
    uvicorn.run(app, port=8000, host='127.0.0.1')
# In dev, può essere comodo lanciare con
# uvicorn main:app --reload
