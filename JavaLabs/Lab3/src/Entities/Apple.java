package Entities;


public class Apple extends Fruit{
    Boolean isRot = Boolean.FALSE;
    public Apple() {
        super("Яблоко", "Зеленый", "3");
    }
    public void polish(){
        System.out.println("Теперь яблоко блестит");
    }
}
