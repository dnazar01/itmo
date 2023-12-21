import Entities.*;

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

        MissBock.spendTime(SvatensonHouse);
        System.out.println();

        Malish.seat(houseOnTheRoof.getFireplace());
        System.out.println();

        Carlson.seat(houseOnTheRoof.getFireplace());
        System.out.println();

        Carlson.fly(hetergeStreet);
        Carlson.move(Shop);
        Carlson.buy(apple);

        System.out.println();
        System.out.println("Проверка некоторых сценариев");

        System.out.println();
        System.out.println("1)Нехватка денег после покупки чего-то");
        Carlson.buy(apple);
        Carlson.buy(apple);

        System.out.println();
        System.out.println("2)Уборка в доме");
        MissBock.clean(SvatensonHouse);
        MissBock.clean(SvatensonHouse);

        System.out.println();
        System.out.println("3)Горение камина и его пополнение");
        for (int i = 0; i < 7; ++i) {
            houseOnTheRoof.getFireplace().burn();
        }
        houseOnTheRoof.getFireplace().addAmountOfCoal(4);
        houseOnTheRoof.getFireplace().burn();

        System.out.println();
        System.out.println("4)Блестящее яблоко");
        apple.polish();

        System.out.println();
        System.out.println("5)Малыш что-то изучил");
        Malish.learnSomething();
    }
}