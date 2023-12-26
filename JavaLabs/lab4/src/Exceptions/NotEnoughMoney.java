package Exceptions;

public class NotEnoughMoney extends RuntimeException {
    public NotEnoughMoney() {
        super("Ошибка: недостаточно денег");
    }
}
