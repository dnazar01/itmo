import Entities.Apple;
import Entities.House;
import Entities.Provocateur;
import Entities.Street;
import Exceptions.FlyWithPropellerOff;
import Exceptions.NotEnoughMoney;

public class Main {
    public static void main(String[] args) {

        House houseOnTheRoof = new House("Домик на крыше");
        houseOnTheRoof.setFireplace();


        House SvatensonHouse = new House("Дом семьи Cватенсон");
        SvatensonHouse.setFireplace();

        House Shop = new House("Магазин продуктов");
        Street hetergeStreet = new Street("Улица Хетерге", new House[]{SvatensonHouse, Shop, houseOnTheRoof});
        Provocateur Carlson = new Provocateur();
        Carlson.propeller.pressButton();
        Carlson.fly(SvatensonHouse);


        Apple apple = new Apple();
        try {
            for (int i = 0; i <= 10; ++i) {
                Carlson.buy(apple);
            }
        } catch (NotEnoughMoney e) {
            System.out.println("Ошибка: " + e.getMessage());
        }


    }
}