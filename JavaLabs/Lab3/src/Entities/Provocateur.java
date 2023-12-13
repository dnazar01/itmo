package Entities;

import Enums.Feelings;
import Interfaces.Flyable;

public class Provocateur extends Character implements Flyable {
    private int moneyOnWallet = 200;

    public Provocateur() {
        super("Карлсон");
    }

    public void buy(Fruit fruit) {
        if (this.moneyOnWallet - fruit.getPrice() >= 0) {
            System.out.println(super.getName() + " купил фрукт " + fruit.getName());
            this.moneyOnWallet -= fruit.getPrice();
        } else {
            System.out.println(super.getName() + " не может купить фрукт " + fruit.getName() + ", так как у " + super.getName() + " недостаточно средств");
        }
    }

    public void seemEarnestly() {
        System.out.println(super.getName() + " показалось это убедительно");
        this.setState(Feelings.SOLID);
    }

    public void fly(Place place) {
        super.setLocation(place);
        System.out.println(super.getName() + " прилетел в " + place.getName());
    }

    @Override
    public void seat(Place place) {
        this.setLocation(place);
        if (place instanceof Fireplace) {
            System.out.println(super.getName() + " сидит у камина в Домике на крыше");
            boolean flag = true;
            if (!place.guests.isEmpty()) {
                for (Character guest : place.guests) {
                    if (guest instanceof Housekeeper) {
                        this.setState(Feelings.SAD);
                        System.out.println("Потому что рядом есть " + guest.getName());
                        flag = false;
                    }
                }
            }
            if (flag) {
                this.setState(Feelings.CALM);
                System.out.println("Потому что рядом нет Фрекен Бок");
            }
        } else {
            System.out.println(super.getName() + " сидит в " + place.getName());
        }
    }
}
