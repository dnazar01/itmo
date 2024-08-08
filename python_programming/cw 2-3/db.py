from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

# Create a declarative base
Base = declarative_base()


# Define your database schema
class PizzaModel(Base):
    __tablename__ = 'pizzas'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    dough = Column(String)
    sauce = Column(String)
    cost = Column(Float)
    orders = relationship("OrderModel", secondary="order_pizzas", back_populates="pizzas")


class OrderModel(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    pizzas = relationship("PizzaModel", secondary="order_pizzas", back_populates="orders")

    def add_pizza(self, pizza):
        self.pizzas.append(pizza)


class OrderPizza(Base):
    __tablename__ = 'order_pizzas'

    order_id = Column(Integer, ForeignKey('orders.id'), primary_key=True)
    pizza_id = Column(Integer, ForeignKey('pizzas.id'), primary_key=True)


# Create the engine with echo turned off
engine = create_engine('sqlite:///pizza_order.db', echo=False)
# Create the tables
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

