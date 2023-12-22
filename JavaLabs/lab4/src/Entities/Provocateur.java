package Entities;

import Enums.Feelings;
import Exceptions.FlyWithPropellerOff;
import Exceptions.NotEnoughMoney;
import Interfaces.Flyable;

public class Provocateur extends Character implements Flyable {
    private int moneyOnWallet = 200;
    public Propeller propeller = new Propeller();

    public Provocateur(){
        super("Карлсон");
    }

    public static class Propeller {
        private boolean isOn = false;
        public boolean isHidden = false;

        public void getStatus() {
            System.out.println("Пропеллер включен: " + isOn);
            System.out.println("Пропеллер спрятан: " + isOn);
        }

        public void pressButton() {
            class Button {
                public void press() {
                    if (!isHidden) {
                        isOn = !isOn;
                        if (isOn) {
                            System.out.println("Пропеллер включен");
                        } else {
                            System.out.println("Пропеллер выключен");
                        }
                    } else {
                        System.out.println("Нельзя включить пропеллер, когда он спрятан");
                    }
                }
            }

            Button button = new Button();
            button.press();
        }
    }

    public void buy(Fruit fruit) throws NotEnoughMoney {
        if (this.moneyOnWallet - fruit.getPrice() >= 0) {
            System.out.println(super.getName() + " купил фрукт " + fruit.getName());
            this.moneyOnWallet -= fruit.getPrice();
        } else {
            throw new NotEnoughMoney("Нельзя купить, так как недостаточно денег");
        }
    }

    public void fly(Place place) throws FlyWithPropellerOff {
        if(this.propeller.isOn) {
            super.setLocation(place);
            System.out.println(super.getName() + " прилетел в " + place.getName());
        }else{
            throw new FlyWithPropellerOff("Вы не можете летать с выключенным пропеллером");
        }
    }
}
