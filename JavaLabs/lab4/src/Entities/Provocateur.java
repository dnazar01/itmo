package Entities;

import Exceptions.FlyWithPropellerOff;
import Exceptions.NotEnoughMoney;
import Interfaces.Flyable;

public class Provocateur extends Character implements Flyable {
    public Propeller propeller = new Propeller();
    private int moneyOnWallet = 200;

    public Provocateur() {
        super("Карлсон");
    }

    public void buy(Fruit fruit) throws NotEnoughMoney {
        if (this.moneyOnWallet - fruit.getPrice() >= 0) {
            System.out.println(super.getName() + " купил фрукт " + fruit.getName());
            this.moneyOnWallet -= fruit.getPrice();
        } else {
            throw new NotEnoughMoney();
        }
    }

    public void fly(Place place) throws FlyWithPropellerOff {
        if (this.propeller.isOn) {
            super.setLocation(place);
            System.out.println(super.getName() + " прилетел в " + place.getName());
        } else {
            throw new FlyWithPropellerOff();
        }
    }

    public static class Propeller {
        public boolean isHidden = false;
        private boolean isOn = false;

        public void getStatus() {
            System.out.println("Пропеллер включен: " + isOn);
            System.out.println("Пропеллер спрятан: " + isOn);
        }

        public void hidePropeller() {
            isHidden = true;
            System.out.println("Теперь пропеллер спрятан");
        }

        public void pressButton() { //1 нажатие - это вкл/выкл, зависит от предыдущего состояния пропеллера
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
}
