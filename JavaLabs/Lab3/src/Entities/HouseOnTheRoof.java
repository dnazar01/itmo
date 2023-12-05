package Entities;

public class HouseOnTheRoof extends House{
    public Fireplace fireplace;
    public HouseOnTheRoof(Fireplace fireplace){

        super("Домик на крыше");
        this.fireplace = fireplace;
    }

}