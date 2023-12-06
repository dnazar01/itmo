import Entities.*;
import Entities.Character;
import Enums.Feelings;

public class Main {
    public static void main(String[] args) {

        Fireplace fireplace = new Fireplace();
        House houseOnTheRoof = new House("Домик на крыше");
        houseOnTheRoof.setFireplace(fireplace);

        House SvatensonHouse = new House("Дом семьи Cватенсон");
        House Shop = new House("Магазин продуктов");
        Street hetergeStreet = new Street("Улица Хетерге", new House[]{SvatensonHouse, Shop, houseOnTheRoof});

        Provocateur Carlson = new Provocateur();
        Child Malish = new Child();
        Housekeeper MissBock = new Housekeeper();

        Apple apple = new Apple();

        Carlson.seemEarnestly();
        System.out.println();

        MissBock.spendLastHoursInCalm(SvatensonHouse);
        System.out.println();

        Malish.seat(houseOnTheRoof.fireplace);
        System.out.println();

        Carlson.seat(houseOnTheRoof.fireplace);
        System.out.println();

        Carlson.fly(hetergeStreet);
        Carlson.move(hetergeStreet.Houses[1]);
        for (int i=0;i<=2;++i){
            Carlson.buy(apple);
        }

    }
}