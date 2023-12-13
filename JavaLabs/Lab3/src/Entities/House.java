package Entities;

public class House extends Place {
    private Fireplace fireplace = null;

    public House(String name) {
        super(name, 10);
    }

    public Fireplace getFireplace() {
        return fireplace;
    }

    public void setFireplace(Fireplace fireplace) {
        this.fireplace = fireplace;
    }
}