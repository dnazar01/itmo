import Entities.*;
import Entities.Character;
import Enums.Feelings;

public class Main {
    public static void main(String[] args) {

        Fireplace fireplace = new Fireplace("Камин");
        HouseOnTheRoof houseOnTheRoof = new HouseOnTheRoof(fireplace);
        House SvatensonHouse = new House("Дом семьи Cватенсон");
        House Shop = new House("Магазин продуктов");

        Street hetergeStreet = new Street("Улица Хетерге", new House[]{SvatensonHouse, Shop});

        Provocateur Carlson = new Provocateur();
        Child Malish = new Child();
        Housekeeper MissBock = new Housekeeper();
        Apple apple = new Apple();

        Carlson.seemEarnestly();
        System.out.println();

        MissBock.spendLastHoursInCalm(SvatensonHouse);
        System.out.println();

        Malish.seat(houseOnTheRoof.fireplace);
        Carlson.seat(houseOnTheRoof.fireplace);
        System.out.println();

        Malish.setState(Feelings.GOOD);
        Malish.setState(Feelings.COSY);
        Malish.setState(Feelings.CALM);
        System.out.println();

        Carlson.setState(Feelings.GOOD);
        Carlson.setState(Feelings.COSY);
        Carlson.setState(Feelings.CALM);
        System.out.println();

        Carlson.fly(hetergeStreet);
        Carlson.move(hetergeStreet.Houses[1]);
        Carlson.buy(new Apple());
    }
}