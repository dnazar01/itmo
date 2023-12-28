package moves.ralts;

import ru.ifmo.se.pokemon.*;

public class Hypnosis extends StatusMove {
    public Hypnosis(double pow, double acc) {
        super(Type.PSYCHIC, pow, acc);
    }

    @Override
    protected void applyOppEffects(Pokemon p) {
        Effect.sleep(p);
    }

    @Override
    protected String describe() {
        return "использует Hypnosis";
    }
}
