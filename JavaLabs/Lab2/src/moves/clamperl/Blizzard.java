package moves.clamperl;

import ru.ifmo.se.pokemon.*;

public class Blizzard extends SpecialMove {
    public Blizzard(double pow, double acc) {
        super(Type.ICE, pow, acc);
    }

    @Override
    protected void applyOppEffects(Pokemon p) {
//        for (Pokemon poke : ps){
//            super.applyOppEffects(poke); //атаку нельзя реализовать полноценно, так как ты взаимодействуешь только с атакующим и защищающимся покемоном
//
//        }
        if(0.1>Math.random()){
            Effect.freeze(p);
        }

    }

    @Override
    protected String describe() {
        return "использует Blizzard ";
    }
}
