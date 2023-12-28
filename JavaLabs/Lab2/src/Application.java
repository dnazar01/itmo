import pokemons.*;
import ru.ifmo.se.pokemon.Battle;
import ru.ifmo.se.pokemon.Pokemon;
public class Application {
    //https://pokemondb.net/pokedex/audino
    //https://pokemondb.net/pokedex/clamperl
    //https://pokemondb.net/pokedex/gorebyss
    //https://pokemondb.net/pokedex/ralts
    //https://pokemondb.net/pokedex/kirlia
    //https://pokemondb.net/pokedex/gardevoir
    public static void main(String[] args) {
        Battle b = new Battle();
        b.addAlly(new Audino("Audino", 1));
        b.addFoe(new Clamperl("Clamperl",1));
        b.addAlly(new Gorebyss("Gorebyss", 1));
        b.addFoe(new Ralts("Ralts", 1));
        b.addAlly(new Kirlia("Kirlia", 1));
        b.addFoe(new Gardevoir("Gardevoir", 1));

        b.go();
    }
}
