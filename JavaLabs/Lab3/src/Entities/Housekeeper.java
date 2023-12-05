package Entities;

import Enums.Feelings;
import Interfaces.Movable;

public class Housekeeper extends Character implements Movable {
    public Housekeeper(){
        super("Фрекен Бок");
    }
    public void move(Place place){
        super.setLocation(place);
        System.out.println(super.getName() + " переместилась в " + place.getName());
    }
    public void seat(Place place){
        super.setLocation(place);
        System.out.println(super.getName() + " сидит в " + place.getName());
    }

    public void relaxAfterWork(Place place){
        super.setLocation(place);
        super.setState(Feelings.CALM);
        System.out.println(super.getName() + " отдохнула после работы в " + place.getName()+ " и чувствует себя " + super.getState());
    }
    public void spendLastHoursInCalm(Place place){
        System.out.println(super.getName() + " проводит последние часы в " + place.getName());
        setState(Feelings.CALM);
    }
    public void kickOut(Provocateur provocateur){
        System.out.println(super.getName() + " выгоняет " + provocateur.getName());
    }
    public void doHousework(){
        System.out.println(super.getName() + " сделала работу по дому");
    }

    public void clean(Place place){
        System.out.println(super.getName() + " убралась в " + place.getName());
    }
    public void cook(){
        System.out.println(super.getName() + " приготовила что-то на кухне");
    }
}

