package Entities;

import Enums.Feelings;

public class Housekeeper extends Character {
    public Housekeeper() {
        super("Фрекен Бок");
    }

    public void spendTime(Place place) {
        System.out.println(super.getName() + " проводит последние часы в " + place.getName());
        if (place.guests.isEmpty()) {
            setState(Feelings.CALM);
            System.out.println("Потому что в этом месте никого нет");
        } else {
            setState(Feelings.ANNOYED);
        }
    }

    public void clean(Place place) {
        System.out.println(super.getName() + " прибралась в " + place.getName());
        place.removeChaosPoints(5);
    }
}

