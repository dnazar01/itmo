package Entities;

import Enums.Feelings;

public class Child extends Character {
    public Child() {
        super("Малыш");
    }

    public void learnSomething() {
        System.out.println(super.getName() + " изучил что-то");
        super.setState(Feelings.CLEVER);
    }
}
