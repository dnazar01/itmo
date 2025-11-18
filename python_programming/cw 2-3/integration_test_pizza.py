import pytest
from unittest.mock import Mock, patch
from pizza import PepperoniPizza, BBQPizza, SeafoodPizza
from order import Order


class TestPizzaOrderIntegration:

    def setup_method(self):
        self.order = Order()

    def test_1_gui_to_order_integration(self):
        with patch('tkinter.messagebox.showinfo') as mock_msg:
            pizza_types = {
                "Пепперони": PepperoniPizza,
                "Барбекю": BBQPizza,
                "Дары моря": SeafoodPizza
            }

            for pizza_name, pizza_class in pizza_types.items():
                initial_count = len(self.order.pizzas)

                self.order.add_pizza(pizza_class, 1)

                assert len(self.order.pizzas) == initial_count + 1
                assert self.order.pizzas[-1].name == pizza_class().name

    def test_2_order_to_database_integration(self):
        with patch('order.session') as mock_session:
            with patch('pizza.session') as mock_pizza_session:
                mock_session.add = Mock()
                mock_session.commit = Mock()
                mock_session.delete = Mock()
                mock_pizza_session.add = Mock()
                mock_pizza_session.commit = Mock()

                self.order.add_pizza(PepperoniPizza, 2)

                self.order.save()

                assert mock_session.add.called
                assert mock_session.commit.called
                assert len(self.order.pizzas) == 0

    def test_3_pizza_creation_and_cooking_integration(self):
        with patch('pizza.session') as mock_session:
            mock_session.add = Mock()
            mock_session.commit = Mock()

            pizza = PepperoniPizza()

            assert pizza.name == "Pepperoni"
            assert pizza.dough == "тонкое"
            assert pizza.sauce == "томатный"
            assert pizza.cost == 10
            assert "пепперони" in pizza._toppings

            with patch.object(pizza, 'log') as mock_log:
                pizza.make_pizza()

                assert mock_log.call_count >= 6

    def test_4_order_total_calculation_integration(self):
        with patch('pizza.session') as mock_session:
            mock_session.add = Mock()
            mock_session.commit = Mock()

            self.order.add_pizza(PepperoniPizza, 1)  # 10
            self.order.add_pizza(BBQPizza, 2)  # 20 * 2 = 40
            self.order.add_pizza(SeafoodPizza, 1)  # 40

            total = self.order.calculate_total()
            expected_total = 10 + 40 + 40  # 90
            assert total == expected_total

    def test_5_pizza_equality_and_addition_integration(self):
        with patch('pizza.session') as mock_session:
            mock_session.add = Mock()
            mock_session.commit = Mock()

            pizza1 = PepperoniPizza()
            pizza2 = PepperoniPizza()

            assert pizza1 == pizza2

            combined_pizza = pizza1 + pizza2
            assert combined_pizza.cost == pizza1.cost + pizza2.cost

            bbq_pizza = BBQPizza()
            assert pizza1 != bbq_pizza

    def test_6_order_clear_functionality_integration(self):
        with patch('order.session') as mock_session:
            with patch('pizza.session') as mock_pizza_session:
                mock_session.delete = Mock()
                mock_session.commit = Mock()
                mock_pizza_session.add = Mock()
                mock_pizza_session.commit = Mock()

                self.order.add_pizza(PepperoniPizza, 2)
                initial_count = len(self.order.pizzas)
                assert initial_count == 2

                self.order.clear()

                assert mock_session.delete.call_count == 2
                assert mock_session.commit.called
                assert len(self.order.pizzas) == 0


class TestEdgeCase:

    def test_empty_order_total(self):
        order = Order()
        assert order.calculate_total() == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])