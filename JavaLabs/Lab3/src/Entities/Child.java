package Entities;

import Enums.Feelings;

public class Child extends Character {
    public Child() {
        super("Малыш");
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

    public void learnSomething() {
        System.out.println(super.getName() + " изучил что-то");
        super.setState(Feelings.CLEVER);
    }
}
