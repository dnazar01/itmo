package Interfaces;

import Entities.House;

import java.util.function.Predicate;

public interface HousePredicate extends Predicate<House> {
    boolean test(House house);
}
