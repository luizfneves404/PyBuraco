"""This module contains the card logic for the PyBuraco game.

It includes classes for the cards, as well as for the base Stack class and its children. It also
includes the parse_card_name function, as well as some card-logic exceptions.

"""

import random


def parse_card_name(card_name: str) -> tuple:
    """Receives a card_name in the format "rank-suit" and returns a tuple of rank and suit."""

    # split card_name into rank and suit
    rank, suit = card_name.split("-")
    # convert rank to int
    rank = int(rank)
    return rank, suit


class SpreadOutError(ValueError):
    """Raised when an operation in which card position matters is being tried on a spread_out stack"""


class EmptyStackError(ValueError):
    """Raised when an operation in which card position matters is being tried on a spread_out stack"""


class Card:
    def __init__(self, rank: int, suit: str) -> None:

        if rank < 1 or rank > 13:
            raise ValueError("Rank must be between 1 and 13")

        if suit not in ["C", "E", "P", "O"]:
            raise ValueError("Suit must be one of C, E, P, O")

        self.rank = rank
        self.suit = suit

    def __str__(self) -> str:
        return self.suit + str(self.rank)


class Stack:
    def __init__(
        self, cards_list: list[Card], is_face_up: bool, is_spread_out: bool
    ) -> None:
        self.cards = cards_list
        self.is_face_up = is_face_up
        self.is_spread_out = is_spread_out

    def __str__(self) -> str:
        return str(self.cards)

    def shuffle(self) -> None:
        random.shuffle(self.cards)

    def add_card_on_top(self, card: Card) -> None:
        self.cards.append(card)

    def add_cards_on_top(self, card_list: list[Card]) -> None:
        self.cards += card_list

    def add_card_on_bottom(self, card: Card) -> None:
        self.cards.insert(0, card)

    def add_cards_on_bottom(self, card_list: list[Card]) -> None:
        # iterando ao inverso para que as cartas fiquem na ordem certa
        for card in card_list[::-1]:
            self.add_card_on_bottom(card)

    def add_stack_on_top(self, stack: "Stack") -> None:
        self.add_cards_on_top(stack.take_all_cards())

    def add_stack_on_bottom(self, stack: "Stack") -> None:
        # iterando ao inverso para que as cartas fiquem na ordem certa
        for card in stack.take_all_cards()[::-1]:
            self.add_card_on_bottom(card)

    def take_card_by_name(self, rank: int, suit: str) -> Card | None:
        for card in self.cards:
            if card.rank == rank and card.suit == suit:
                self.cards.remove(card)
                return card

        return None

    def take_top_card(self) -> Card:
        # if the Stack is spread out, this command does not make sense, raise error
        if self.is_spread_out:
            raise SpreadOutError("Cannot pick top card from a spread out stack")

        # the cards in the cards_list are from bottom to top, so the last card is on top
        try:
            return self.cards.pop()
        except IndexError as e:
            raise ValueError("Cannot take top card from empty stack") from e

    def take_top_cards(self, quantity: int) -> list[Card]:
        if self.is_spread_out:
            raise SpreadOutError("Cannot deal cards from a spread out stack")

        try:
            if quantity < 1:
                raise ValueError("Quantity must be greater than 0")
        except TypeError:
            print("Quantity must be an integer")

        return self.cards[-quantity:]

    def take_all_cards(self) -> list[Card]:
        cards = self.cards
        self.cards = []
        return cards

    def is_empty(self) -> bool:
        return len(self.cards) == 0

    def get_size(self) -> int:
        return len(self.cards)

    def get_top_card(self) -> Card:
        return self.cards[-1]

    def get_bottom_card(self) -> Card:
        return self.cards[0]


class Deck(Stack):
    def __init__(self):
        cards = []
        for suit in ["C", "O", "P", "E"]:
            cards.extend(Card(rank, suit) for rank in range(1, 14))  # 1-13

        super().__init__(self, cards, False, False)
        self.shuffle()


class Hand(Stack):
    def __init__(self):
        super().__init__(self, [], False, False)


class BuyingStack(Stack):
    def __init__(self, cards_list: list[Card]):
        super().__init__(self, cards_list, False, False)

    def buy(self) -> Card:
        if self.is_empty():
            raise EmptyStackError("Buying stack is empty")
        else:
            return self.take_top_card()


class TrashStack(Stack):
    def __init__(self):
        super().__init__(self, [], True, True)

    # if buying from trash, you have to get all the cards in the trash
    def buy(self) -> list[Card]:
        if self.is_empty():
            raise EmptyStackError("Trash stack is empty")
        else:
            return self.take_all_cards()


class Morto(Stack):
    def __init__(self, cards_list: list[Card]):
        super().__init__(self, cards_list, False, False)

    def take(self) -> list[Card]:
        if self.is_empty():
            raise EmptyStackError("Morto stack is empty")
        else:
            return self.take_all_cards()


class Sequence(Stack):
    def __init__(self, cards_list: list[Card]):
        # sourcery skip: remove-pass-body, remove-redundant-pass, swap-if-else-branches
        if len(cards_list) < 3:
            raise ValueError("Sequence must have at least 3 cards")

        super().__init__(self, cards_list, True, False)

        # TODO check_if_can_be_sequence()

        if cards_list[0].suit != cards_list[1].suit:  # tem coringa de outro naipe
            # TODO descobrir naipe do jogo nesse caso
            pass

        else:  # duas primeiras cartas são do mesmo naipe, então posso definir o naipe do jogo como o naipe da primeira carta
            self.suit = cards_list[0].suit

    def add_card(self, card: Card) -> None:
        suit = card.suit
        if self.suit == suit:
            rank = card.rank
            if self.get_bottom_card().rank - 1 == rank:
                self.add_card_on_bottom(card)
            elif self.get_top_card().rank + 1 == rank:
                self.append_card(card)
            else:
                raise ValueError("Card cannot enter this sequence")
