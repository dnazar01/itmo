package Entities;

import Enums.Feelings;
import Interfaces.Movable;
public class Child extends Character{
    public Child(){
        super("Малыш");
    }

    @Override
    public void seat(Place place){
        super.setLocation(place);
        if (place.getClass() == House.class && ((House) place).fireplace!=null){
            System.out.println(super.getName() + " сидит у камина в Домике на крыше");
            this.setState(Feelings.GOOD);
            this.setState(Feelings.COSY);
            this.setState(Feelings.CALM);
        }
        else {
            System.out.println(super.getName() + " сидит в " + place.getName());
        }
    }

    public void learnSomething(){
        System.out.println(super.getName() + " изучил что-то");
        super.setState(Feelings.CLEVER);
    }
}
