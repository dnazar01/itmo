package Entities;

import Enums.Feelings;
import Interfaces.Movable;

public class Child extends Character implements Movable {
    public Child(){
        super("Малыш");
    }
    public void move(Place place){
        super.setLocation(place);
        System.out.println(super.getName() + " переместился в " + place.getName());
    }
    public void seat(Place place){
        super.setLocation(place);
        System.out.println(super.getName() + " сидит в " + place.getName());
    }

    public void lieSomeone(Character character){
        super.setState(Feelings.SAD);
        System.out.println(super.getName() + " солгал " + character.getName());
    }
    public void doHomework(){
        System.out.println(super.getName() + " сделал домашку");
    }
    public void watchCartoons(){
        System.out.println(super.getName() + " посмотрел мультики");
    }

    public void learnSomething(){
        System.out.println(super.getName() + " изучил что-то");
    }
}
