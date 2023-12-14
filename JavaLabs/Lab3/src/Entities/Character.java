package Entities;

import Enums.Feelings;
import Interfaces.Movable;

import java.util.Objects;

public abstract class Character implements Movable {
    private String name;
    private Feelings state = null;
    private Place location = null;

    public Character(String name) {
        this.name = name;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Character character = (Character) o;
        return Objects.equals(name, character.name) && Objects.equals(state, character.state) && Objects.equals(location, character.location);
    }

    @Override
    public int hashCode() {
        return Objects.hash(name);
    }

    public String getName() {
        return this.name;
    }

    @Override
    public String toString() {
        return this.getName();
    }

    public Feelings getState() {
        return this.state;
    }

    public void setState(Feelings feeling) {
        this.state = feeling;
        switch (feeling) {
            case GOOD:
                System.out.println(this.getName() + " чувствует себя " + "хорошо");
                break;
            case CALM:
                System.out.println(this.getName() + " чувствует себя " + "спокойно");
                break;
            case SAD:
                System.out.println(this.getName() + " чувствует себя " + "грустно");
                break;
            case SOLID:
                System.out.println(this.getName() + " чувствует себя " + "убедительно");
                break;
            case COMFORT:
                System.out.println(this.getName() + " чувствует себя " + "комфортно");
                break;
            case CONFUSED:
                System.out.println(this.getName() + " чувствует себя " + "растерянно");
                break;
            case COSY:
                System.out.println(this.getName() + " чувствует себя " + "уютно");
                break;
            case CLEVER:
                System.out.println(this.getName() + " чувствует себя " + "умным");
                break;
            case ANNOYED:
                System.out.println(this.getName() + " чувствует себя " + "раздраженно");
                break;
        }

    }

    public void setLocation(Place place) {
        if (this.location != null) {
            this.location.removeGuest(this);
        }
        this.location = place;
        place.guests.add(this);
    }

    public void move(Place place) {
        this.setLocation(place);
        System.out.println(this.name + " переместился в " + place.getName());
    }

    public void seat(Place place) {
        this.setLocation(place);
        System.out.println(this.name + " сидит в " + place.getName());
    }

}


