import Entities.Apple;
import Entities.House;
import Entities.Provocateur;
import Entities.Street;
import Enums.Feelings;
import Exceptions.FlameThrow;
import Exceptions.FlyWithPropellerOff;
import Exceptions.NotEnoughMoney;
import Interfaces.HousePredicate;

public class Main {
    public static void main(String[] args) {

        House houseOnTheRoof = new House("Домик на крыше");
        houseOnTheRoof.setFireplace();
        House SvatensonHouse = new House("Дом семьи Cватенсон");
        SvatensonHouse.setFireplace();
        House Shop = new House("Магазин продуктов");
        Street hetergeStreet = new Street("Улица Хетерге", new House[]{SvatensonHouse, Shop, houseOnTheRoof});
        Provocateur Carlson = new Provocateur();


        //1 блок проверки, пробуем взлететь
        try {
            Carlson.fly(SvatensonHouse);
        } catch (FlyWithPropellerOff e) {
            System.out.println(e.getMessage());
        }
        Carlson.setState(Feelings.GOOD);


        //2 блок проверки, пробуем купить яблок
        Apple apple = new Apple();
        try {
            for (int i = 0; i <= 10; ++i) {
                Carlson.buy(apple);
            }
        } catch (NotEnoughMoney e) {
            System.out.println("Ошибка: " + e.getMessage());
        }


        //3 блок - камин
        SvatensonHouse.getFireplace().addAmountOfCoal(100);
        try {
            int burnTimes = 0;
            for (int i = 0; i < 10; ++i) {
                burnTimes += 1;
                if (burnTimes > 4) {
                    throw new FlameThrow();
                }
            }
        } catch (FlameThrow e) {
            System.out.println(e.getMessage());
        }


        //4 блок, просто анонимный класс nameFilter и его использование
        HousePredicate nameFilter = new HousePredicate() {
            @Override
            public boolean test(House house) {
                return house.getName().contains("Cватенсон");
            }
        };

        if (nameFilter.test(SvatensonHouse)) {
            System.out.println("Этот дом относится к семье Cватенсон.");
        } else {
            System.out.println("Этот дом не относится к семье Cватенсон.");
        }

    }
}