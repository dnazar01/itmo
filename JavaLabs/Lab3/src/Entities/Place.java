package Entities;

import java.util.Objects;

public abstract class Place {
    private String name;
    public Place(String name){
        this.name = name;
    }
    public int hashCode() {
        return Objects.hash(name);
    }
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Place place = (Place) o;
        return Objects.equals(place.name, this.name);
    }
    public String getName() {
        return this.name;
    }

    public String toString() {
        return this.getName();
    }
}
