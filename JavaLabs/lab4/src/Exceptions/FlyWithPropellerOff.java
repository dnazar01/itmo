package Exceptions;

public class FlyWithPropellerOff extends RuntimeException {
    public FlyWithPropellerOff() {
        super("Ошибка: вы не можете летать с выключенным пропеллером");
    }
}
