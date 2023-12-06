package Entities;

public class Street extends Place{
    public House[] Houses;
    public Street(String name, House[] Houses){
        super(name, 0);
        this.Houses = Houses;
    }

}
