package Entities;

import Enums.Feelings;

import java.util.Objects;

public abstract class Fruit {
    private String name;
    private String color;
    private String grade;
    public Fruit(String name, String color, String grade){
        this.name = name;
        this.color = color;
        this.grade =  grade;
    }

    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Fruit fruit = (Fruit) o;
        return Objects.equals(name, fruit.name) && Objects.equals(color, fruit.color) && Objects.equals(grade, fruit.grade);
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
    public void setName(String newName){
        this.name = newName;
    }
    public void setColor(String newColor){
        this.color = newColor;
    }

    public void setGrade(String newGrade){
        this.grade = newGrade;
    }
}
