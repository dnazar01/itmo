package Entities;

public class House extends Place {
    private Fireplace fireplace;

    public House(String name) {
        super(name, 10);
    }

    public Fireplace getFireplace() {
        return fireplace;
    }

    public void setFireplace(){
        fireplace = new House.Fireplace("Камин", 5);
    }
    public class Fireplace extends Place{
        private int amountOfCoal;

        public Fireplace(String name, int chaosPoints) {
            super("Камин", 5);
        }

        public String getLocation(){
            return House.super.getName();
        }

        public void burn() {
            if (this.amountOfCoal <= 0) {
                System.out.println("В камине " + this.amountOfCoal + " углей, пополните камин");
            } else {
                this.amountOfCoal -= 1;
                System.out.println(getName() + " горит");
            }
        }

        public void addAmountOfCoal(int amount) {
            this.amountOfCoal += amount;
            System.out.println("Теперь углей в камине: " + this.amountOfCoal);
        }
    }
}