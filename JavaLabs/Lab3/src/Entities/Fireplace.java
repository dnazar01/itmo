package Entities;

public class Fireplace extends Place {
    private int amountOfCoal = 10;

    public Fireplace() {
        super("Камин", 0);
    }
    public String getHouseName(House house) {
        return house.getName(); // Получаем имя House из объекта House
    }

    public void burn() {
        System.out.println(this.getName() + " горит");
        this.amountOfCoal -= 1;
        if (this.amountOfCoal == 0) {
            System.out.println("Уголь закончился, пополните камин");
        }
    }

    public void addAmountOfCoal(int amount) {
        this.amountOfCoal += amount;
        System.out.println("Теперь углей в камине: " + this.amountOfCoal);
    }
}
