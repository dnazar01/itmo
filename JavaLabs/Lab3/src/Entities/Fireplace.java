package Entities;

public class Fireplace extends Place {
    private int amountOfCoal = 5;

    public Fireplace() {
        super("Камин", 0);
    }

    public void burn() {
        if (this.amountOfCoal <= 0) {
            System.out.println("В камине " + this.amountOfCoal + " углей, пополните камин");
        } else {
            this.amountOfCoal -= 1;
            System.out.println(this.getName() + " горит");
        }
    }

    public void addAmountOfCoal(int amount) {
        this.amountOfCoal += amount;
        System.out.println("Теперь углей в камине: " + this.amountOfCoal);
    }
}
