package Entities;


public class Apple extends Fruit {
    public boolean isRot = false;

    public Apple() {
        super("Яблоко", "Зеленый", "3", 100);
    }

    public void polish() {
        System.out.println("Теперь яблоко блестит");
        super.setColor("Блестящий" + this.getColor());
    }
}
