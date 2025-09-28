import unittest
from pizza import PepperoniPizza, BBQPizza, SeafoodPizza, Pizza
from order import Order
from db import session, PizzaModel, OrderModel


def _clear_session():
    if hasattr(session, "clear_all"):
        try:
            session.clear_all()
        except Exception:
            pass

    try:
        for o in session.query(OrderModel).all():
            try:
                session.delete(o)
            except Exception:
                pass
    except Exception:
        pass

    try:
        for p in session.query(PizzaModel).all():
            try:
                session.delete(p)
            except Exception:
                pass
    except Exception:
        pass

    # commit, если есть
    if hasattr(session, "commit"):
        try:
            session.commit()
        except Exception:
            pass


class TestPizzaModel(unittest.TestCase):
    def setUp(self):
        _clear_session()

    def test_pepperoni_attributes_and_toppings(self):
        # Arrange & Act
        p = PepperoniPizza()
        # Assert
        self.assertEqual(p.name, "Pepperoni")
        self.assertEqual(p.dough, "тонкое")
        self.assertEqual(p.sauce, "томатный")
        self.assertEqual(p.cost, 10)

    def test_pizza_equality_and_addition(self):
        # Arrange
        p1 = PepperoniPizza()
        p2 = PepperoniPizza()
        p3 = BBQPizza()
        # Act & Assert
        self.assertEqual(p1, p2)
        self.assertNotEqual(p1, p3)
        # Act
        summed = p1 + p3
        # Assert
        self.assertIsInstance(summed, Pizza)
        self.assertEqual(summed.cost, p1.cost + p3.cost)


class TestOrderModel(unittest.TestCase):
    def setUp(self):
        _clear_session()

    def test_order_add_and_calculate_total_edge(self):
        # Arrange
        order = Order()
        # Act
        order.add_pizza(PepperoniPizza, 3)
        # Assert
        pizzas = order.get_pizzas()
        self.assertEqual(len(pizzas), 3)
        self.assertEqual(order.calculate_total(), 3 * 10)

    def test_order_save_clears(self):
        # Arrange
        order = Order()
        order.add_pizza(SeafoodPizza, 2)
        # Act
        order.save()
        # Assert
        self.assertEqual(len(order.get_pizzas()), 0)

    def test_order_clear_deletes_pizzas(self):
        # Arrange
        order = Order()
        order.add_pizza(PepperoniPizza, 1)
        # Act
        order.clear()
        # Assert
        try:
            cnt = session.query(PizzaModel).count()
        except Exception:
            try:
                cnt = len(session.query(PizzaModel).all())
            except Exception:
                cnt = None
        self.assertEqual(cnt, 0)


if __name__ == "__main__":
    unittest.main()
