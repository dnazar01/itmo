package Entities;

import Enums.Feelings;
import Interfaces.Movable;

import java.util.Objects;

public abstract class Character implements Movable {
    private String name;
    private Feelings state;
    private Place location;

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
        return Objects.hash(name, state, location);
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
        System.out.println(this.getName() + " чувствует себя " + feeling.getTranslation());
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

    // Перегруженный метод для объекта House.Fireplace
    public void seat(House.Fireplace fireplace) {
        this.setLocation(fireplace);
        System.out.println(this.getName() + " сидит у " + fireplace.getName() + " в " + fireplace.getLocation());
        boolean housekeeperNearby = false;

        for (Character guest : fireplace.guests) {
            if (guest instanceof Housekeeper) {
                this.setState(Feelings.SAD);
                System.out.println("Потому что рядом есть " + guest.getName());
                housekeeperNearby = true;
                break;
            }
        }

        if (!housekeeperNearby) {
            this.setState(Feelings.CALM);
            System.out.println("Потому что рядом нет Фрекен Бок");
        }
    }
}


