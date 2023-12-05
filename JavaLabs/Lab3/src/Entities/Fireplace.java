package Entities;

public class Fireplace extends Place{
    public Fireplace(String name){
        super(name);
    }
    public void burn(){
        System.out.println(this.getName() + " горит");
    }
}
