"""PyBuraco is a text-based implementation of the famous brazillian card game "Buraco",
also known as Canastra.

Two decks of cards are used. There are two ways to play the game:
with two players or with two pairs of players. Each player has a hand of eleven (11)
cards dealt to them at the beginning of the game. There are two piles of cards on the table:
a face-down stack for buying cards (named BuyingStack) and a face-up group of cards (named Trash),
which can be seen at the same time Each player will try to create sequences of cards on their side
of the table.

A sequence of cards consists of a set of cards in ascending order. It must contain at
least three (3) cards to be dealt onto the table. After one of the players runs out of cards, both
players count their points and the game ends. The player with the most points wins. All Stacks of
cards, including those of the players, are indexed from bottom to top, so that the first card is on
the bottom, and the last card is on top
"""

import random
from card_logic import (
    Stack,
    Morto,
    Deck,
    Hand,
    BuyingStack,
    TrashStack,
    parse_card_name,
)


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = Hand()

    def append_card(self, card):
        self.hand.append_card(card)

    def append_cards(self, cards_list):
        self.hand.append_cards(cards_list)

    def append_stack(self, stack):
        self.append_cards(stack.pick_all_cards())

    def pick_card_by_name(self, rank, suit):
        return self.hand.pick_card_by_name(rank, suit)

    def get_cards(self):
        return self.cards


class TableSide(list):
    def add_sequence(self, sequence):
        if len(sequence) < 3:
            raise Exception("Sequence must have at least 3 cards")
        self.append(sequence)


class BuracoGame:
    def __init__(self, is_four_player):
        self.big_deck = Stack(Deck().get_cards() + Deck().get_cards(), False, False)

        self.is_four_player = is_four_player
        if self.is_four_player == False:
            self.players = [Player("Jack"), Player("Bob")]
        else:
            self.players = [
                Player("Jack"),
                Player("Bob"),
                Player("James"),
                Player("Barbara"),
            ]

        for player in self.players:
            player.append_cards(self.big_deck.deal_cards(11))

        self.mortos = [
            Morto(self.big_deck.deal_cards(11)),
            Morto(self.big_deck.deal_cards(11)),
        ]

        self.buying_stack = BuyingStack(self.big_deck.pick_all_cards())
        self.trash_stack = TrashStack()

        self.table_sides = [TableSide(), TableSide()]

        self.player_now = self.players[0]

    def play_game(self):
        # main game loop
        while True:
            for player in self.players:
                self.player_now = player

                self.situation_report()

                player_buy_decision = self.get_player_buy_decision()

                if player_buy_decision == "m":
                    self.buy_from_buying_stack()
                else:
                    self.buy_from_trash_stack()

                self.situation_report()
                self.play_turn()

                self.player_discards()

    def play_turn(self):
        player_action = self.get_player_action()
        if player_action == "a":
            cards_to_be_added = self.get_cards_to_be_added()

    def get_cards_to_be_added(self):
        cards_to_be_added = {}
        card_name_string = input(
            "Digite a carta que deseja adicionar. (Ex: '7-P' para 7 de paus) "
        )
        sequence = input(
            "Qual a sequencia de cartas na qual deseja adicionar essa carta? (Ex: '7-P' para 7 de paus) "
        )
        cards_to_be_added.append(
            self.player_now.pick_card_by_name(*parse_card_name(card_name_string))
        )

        while True:
            card_name_string = input(
                "Se quiser adicionar mais uma, só digitar. Se quiser parar, digite 'p'. "
            )
        for card in self.player_now.hand:
            if card.suit == self.player_now.suit:
                cards_to_be_added.append(card)
        return cards_to_be_added

    def get_player_action(self):
        while True:
            choice = input(
                "Você quer: baixar um jogo novo ('b'), adicionar cartas em um jogo ('a') ou só descartar ('d')?"
            )
            if choice in ["b", "a", "d"]:
                return choice
            else:
                raise Exception("Choose either 'b', 'a' or 'd'")

    def situation_report(self):
        player_now = self.player_now
        print(f"Player {player_now.name}")
        print(f"Cards in hand: {player_now.get_cards()}")
        print(f"Cards in trash: {self.trash_stack.get_cards()}")

    def get_player_buy_decision(self):
        while True:
            choice = input("Comprar do monte ('m') ou do lixo ('l')?")
            if choice in ["l", "m"]:
                return choice
            else:
                raise Exception("Choose either 'l' or 'm'")

    def buy_from_buying_stack(self):
        player_now = self.player_now
        while True:
            if self.buying_stack.get_size() > 0:
                card = self.buying_stack.buy()
                player_now.append_card(card)
                print(f"Player {player_now.name} bought {card}")
                return

            elif self.mortos_are_empty():
                self.end_game_empty()

            else:
                self.morto_becomes_buying_stack()

    def buy_from_trash_stack(self):
        player_now = self.player_now
        player_now.append_cards(self.trash_stack.buy())
        print(f"Player {player_now.name} bought from trash stack")
        return

    def mortos_are_empty(self) -> bool:
        return self.mortos[0].is_empty() and self.mortos[1].is_empty()

    def end_game_empty(self):
        print("Game over")
        print("Cards in buying stack:", self.buying_stack.get_cards())
        print("Cards in trash:", self.trash_stack.get_cards())
        print("Cards in mortos:", self.mortos)
        print("Cards in mortos:", self.mortos[0].get_cards())
        print("Cards in mortos:", self.mortos[1].get_cards())

    def end_game_batida(self):
        pass

    def morto_becomes_buying_stack(self):
        if self.mortos[0].is_empty():
            self.buying_stack.append_stack(self.mortos[1])
        else:
            self.buying_stack.append_stack(self.mortos[0])

    def give_morto(self):
        player_now = self.player_now
        if self.mortos[0].is_empty():
            player_now.append_stack(self.mortos[1])
        else:
            player_now.append_stack(self.mortos[0])
