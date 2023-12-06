package Entities;

public class House extends Place{
    public Fireplace fireplace = null;
    public House(String name){
        super(name, 10);
    }
    public void setFireplace(Fireplace fireplace) {
        this.fireplace = fireplace;
    }
}