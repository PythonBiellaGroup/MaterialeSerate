# Problema: aggiungere limite e paginazione (read_product_types)
# https://sqlmodel.tiangolo.com/tutorial/fastapi/limit-and-offset/
# Update
# https://sqlmodel.tiangolo.com/tutorial/fastapi/update/
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Query
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


class ProductTypeBase(SQLModel):
    name: str


class ProductType(ProductTypeBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class ProductTypeCreate(ProductTypeBase):
    pass


class ProductTypeRead(ProductTypeBase):
    id: int


# Nel modello update tutti gli attributi devono essere opzionali
class ProductTypeUpdate(SQLModel):
    name: Optional[str] = None


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
def create_tags(tag: Tag):
    with Session(engine) as session:
        session.add(tag)
        session.commit()
        session.refresh(tag)
        return tag


@app.post("/product_types/", response_model=ProductTypeRead)
def create_product_type(product_type: ProductTypeCreate):
    with Session(engine) as session:
        db_pt = ProductType.from_orm(product_type)
        session.add(db_pt)
        session.commit()
        session.refresh(db_pt)
        return db_pt


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
# lte -> less than or equal
def read_product_types(offset: int = 0,
                       limit: int = Query(default=100, lte=100)):
    with Session(engine) as session:
        product_types = session.exec(
            select(ProductType).offset(offset).limit(limit)).all()
        return product_types


@app.get("/product_types/{producttype_id}", response_model=ProductTypeRead)
def read_product_type(producttype_id: int):
    with Session(engine) as session:
        pt = session.get(ProductType, producttype_id)
        if not pt:
            raise HTTPException(
                status_code=404,
                detail="Product type not found"
                )
        return pt


@app.patch("/product_types/{producttype_id}", response_model=ProductTypeRead)
def update_hero(producttype_id: int, pt: ProductTypeUpdate):
    with Session(engine) as session:
        db_pt = session.get(ProductType, producttype_id)
        if not db_pt:
            raise HTTPException(status_code=404, detail="Product type found")
        # exclude_unset=True: it would only include the values
        # that were sent by the client
        pt_data = pt.dict(exclude_unset=True)
        for key, value in pt_data.items():
            setattr(db_pt, key, value)
        session.add(db_pt)
        session.commit()
        session.refresh(db_pt)
        return db_pt


@app.delete("/product_types/{producttype_id}")
def delete_product_type(producttype_id: int):
    with Session(engine) as session:
        pt = session.get(ProductType, producttype_id)
        if not pt:
            raise HTTPException(
                status_code=404,
                detail="Product type not found"
                )
        session.delete(pt)
        session.commit()
        return {"ok": True}


@app.get("/products/", response_model=List[Product])
def read_products():
    with Session(engine) as session:
        products = session.exec(select(Product)).all()
        return products


if __name__ == '__main__':
    uvicorn.run(app, port=8000, host='127.0.0.1')
# In dev, può essere comodo lanciare con
# uvicorn main:app --reload
