package Entities;

import Enums.Feelings;
import Interfaces.*;
public class Provocateur extends Character implements Flyable {
    private int moneyOnWallet = 10000000;

    public Provocateur() {
        super("Карлсон");
    }

    public void buy(Fruit fruit) {
        if (this.moneyOnWallet - fruit.getPrice() >= 0) {
            System.out.println(super.getName() + " купил фрукт " + fruit.getName());
            this.moneyOnWallet -= fruit.getPrice();
        } else {
            System.out.println("У " + this.getName() + " недостаточно средств");
        }
    }

    public void seemEarnestly() {
        System.out.println(super.getName() + "у показалось это убедительно");
        this.setState(Feelings.SOLID);
    }

    public void fly(Place place) {
        super.setLocation(place);
        System.out.println(super.getName() + " прилетел в " + place.getName());
    }

    @Override
    public void seat(Place place) {
        this.setLocation(place);
        if (place.getClass() == Fireplace.class) {
            System.out.println(super.getName() + " сидит у камина в Домике на крыше");
            this.setState(Feelings.GOOD);
            this.setState(Feelings.COSY);
            this.setState(Feelings.CALM);
        } else {
            System.out.println(super.getName() + " сидит в " + place.getName());
        }
    }
}
