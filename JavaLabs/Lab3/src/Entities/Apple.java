package Entities;


public class Apple extends Fruit {
    public Boolean isRot = Boolean.FALSE;

    public Apple() {
        super("Яблоко", "Зеленый", "3", 100);
    }

    public void polish() {
        System.out.println("Теперь яблоко блестит");
        super.setColor("Блестящий" + this.getColor());
    }
}
