package Exceptions;

public class NotEnoughMoney extends RuntimeException{
    public NotEnoughMoney(String message){
        super(message);
    }
}
