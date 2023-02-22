# PyBuraco

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

PyBuraco is a text-based implementation of the famous card game "Buraco", also known as Canastra.

Currently, nothing really works. A lot of code still has to be added. In the end, this is not supposed to be an attractive and interesting game, it's more of a Python programming exercise. In the future, a GUI version may be developed to inject some actual fun into the game.

## How to play the game in real life (in case you didn't know)

The following is a description of how to play the Buraco Aberto variation, as i like to play it (and as i hope to implement on this project).

Two decks of cards are used. There are two ways to play the game: with two players or with two pairs of players. Each player has a hand of eleven (11) cards dealt to them at the beginning of the game. There are four stacks of cards on the table on the beginning of the game: a face-down stack for buying cards (named BuyingStack), a face-up and spread out group of cards for buying discarded cards (named TrashStack) and the two "mortos", which can be acquired later in the game.

In their turn, a player will (1) buy a card from the BuyingStack or choose instead to buy all cards in the TrashStack, (2) optionally place down a new sequence or add cards to their sequences and (3) discard one card (unless they manage to get rid of all their cards by placing them in sequences). When discarded, a card goes to the TrashStack.

Players can create sequences of cards and place them on their side of the table. A sequence of cards consists of a set of cards of the same suit in ascending order. It must contain at least three (3) cards to be dealt onto the table. When playing with four, the sequences belong to the pair, not the individual players, so either of the two can add cards to the pair's sequences.

The primary objective of the game is to form sequences of 7 cards, which are called "canastras". Adding more cards to a canastra doesn't change the fact that it is a canastra. However, it can be a dirty (has a joker or a 2 of any suit as a placeholder for a missing card) or a clean canastra (no jokers or 2s being used as placeholders. Note that a 2 can be used in its normal position while still keeping the canastra clean).

After one of the players manages to run out of cards, that person gets the first morto and it becomes their hand. After that same player (or the same pair of players, if playing with four) runs out of cards again, the game immediately ends. If one player (or pair) gets the first morto, then the other player (or the other pair) gets the second morto, the game continues until another player runs out of cards for the third time in the game, or until the BuyingStack runs out of cards. If the BuyingStack runs out of cards and at least one of the mortos is still on the table, the morto becomes the BuyingStack.

When the game ends, players count their points. Canastras yield points just for being canastras, as well as for the cards they contain. Clean canastras are worth more than dirty canastras. Sequences only yield the sum of each card's points.
