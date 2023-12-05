package Entities;

import Enums.Feelings;
import Interfaces.*;

public class Provocateur extends Character implements Flyable, Movable{
    public Provocateur(){
        super("Карлсон");
    }
    public void buy(Fruit fruit){
        System.out.println(super.getName() + " купил фрукт " + fruit.getName());
    }
    public void seemEarnestly(){
        System.out.println(super.getName() + "у показалось это убедительно");
        this.setState(Feelings.SOLID);
    }
    public void provocate(Child child){
        System.out.println(super.getName() + " провоцирует " + child.getName());
    }
    public void fly(Place place){
        super.setLocation(place);
        System.out.println(super.getName() + " прилетел в " + place.getName());
    }

    public void move(Place place){
        super.setLocation(place);
        System.out.println(super.getName() + " переместился в " + place.getName());
    }
    public void seat(Place place){
        super.setLocation(place);
        System.out.println(super.getName() + " сидит в " + place.getName());
    }
}
