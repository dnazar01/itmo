package Entities;

import Enums.Feelings;

import java.util.Objects;

public abstract class Character {
    private String name;
    private Feelings state;
    private Place location;

    public Character(String name) {
        this.name = name;
    }

    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Character character = (Character) o;
        return Objects.equals(name, character.name) && Objects.equals(state, character.state) && Objects.equals(location, character.location);
    }

    public int hashCode() {
        return Objects.hash(name);
    }

    public String getName() {
        return this.name;
    }

    public String toString() {
        return this.getName();
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
                System.out.println(this.getName() + " чувствует себя " + "уверенно/убедительно");
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
        }

    }

    public Feelings getState() {
        return this.state;
    }

    public void setLocation(Place place) {
        this.location = place;
    }

}
