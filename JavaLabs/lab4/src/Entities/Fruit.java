package Entities;

import java.util.Objects;

public abstract class Fruit {
    private String name;
    private String color;
    private String grade;
    private int price;

    public Fruit(String name, String color, String grade, int price) {
        this.name = name;
        this.color = color;
        this.grade = grade;
        this.price = price;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Fruit fruit = (Fruit) o;
        return Objects.equals(name, fruit.name) && Objects.equals(color, fruit.color) && Objects.equals(grade, fruit.grade);
    }

    @Override
    public int hashCode() {
        return Objects.hash(name, color, grade, price);
    }

    public String getName() {
        return this.name;
    }

    @Override
    public String toString() {
        return this.getName();
    }

    public String getColor() {
        return this.color;
    }

    public void setColor(String newColor) {
        this.color = newColor;
    }

    public int getPrice() {
        return this.price;
    }

}
