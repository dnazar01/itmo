package Entities;

import Enums.Feelings;
import Interfaces.Movable;

public class Child extends Character {
    public Child() {
        super("Малыш");
    }

    @Override
    public void seat(Place place) {
        this.setLocation(place);
        if (place.getClass() == Fireplace.class) {
            System.out.println(super.getName() + " сидит у камина в Домике на крыше");
            Boolean flag = Boolean.TRUE;
            if (!place.guests.isEmpty()) {
                for (Character guest : place.guests) {
                    if (guest.getClass() == Housekeeper.class) {
                        this.setState(Feelings.SAD);
                        System.out.println("Потому что рядом есть " + guest.getName());
                        flag = Boolean.FALSE;
                    }
                }
            }
            if (flag){
                this.setState(Feelings.GOOD);
                this.setState(Feelings.COSY);
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
