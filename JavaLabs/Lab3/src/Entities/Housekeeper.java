package Entities;

import Enums.Feelings;
import Interfaces.Movable;

public class Housekeeper extends Character implements Movable {
    public Housekeeper(){
        super("Фрекен Бок");
    }
    public void spendLastHoursInCalm(Place place){
        System.out.println(super.getName() + " проводит последние часы в " + place.getName());
        if (place.guests.isEmpty()){
            setState(Feelings.CALM);
            System.out.println("Потому что в этом месте никого нет");
        }
        else{
            setState(Feelings.ANNOYED);
        }
    }

    public void clean(Place place){
        place.removeChaosPoints(5);
        System.out.println(super.getName() + " прибралась в " + place.getName());
    }
}

