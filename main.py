# Imports
from data_structures import Game, Bot

over = False

while not over:
    game = Game()
    bot = Bot(game.player2, game)
    winner = None
    while game.player1.count() > 0:
        print("The briscola is the {:s} of {:s}".format(game.briscola.rank, game.briscola.suit))
        print("Cards remaining in the deck: {:d}".format(game.deck.count()))
        print()
        if winner == game.player1 or winner == None:
            game.player1.print_hand()
            print()
            prompt = "Select a card (1"
            for i in range(2, game.player1.count()+1):
                prompt += ", " + str(i)
            prompt += ", or 0 to quit): "
            handIndex = int(input(prompt))
            if handIndex == 0:
                exit()
            print()
            card1 = game.player1.play_card(handIndex-1)
            card2 = game.player2.play_card(bot.make_move(card1))
            print("Player 1 plays the {:s} of {:s}".format(card1.rank, card1.suit))
            print("Player 2 plays the {:s} of {:s}".format(card2.rank, card2.suit))
            print()
            winner = game.card_cmp(card1, card2)
            if winner == 1:
                print("Player 1 wins")
                game.player1.score += card1.value + card2.value
                winner = game.player1
                if game.deck.count() > 0:
                    game.deal_card(game.player1, game.player2)
            else:
                print("Player 2 wins")
                game.player2.score += card1.value + card2.value
                winner = game.player2
                if game.deck.count() > 0:
                    game.deal_card(game.player2, game.player1)
        else:
            card2 = game.player2.play_card(bot.make_move())
            print("Player 2 plays the {:s} of {:s}".format(card2.rank, card2.suit))
            print()
            game.player1.print_hand()
            print()
            prompt = "Select a card (1"
            for i in range(2, game.player1.count()+1):
                prompt += ", " + str(i)
            prompt += ", or 0 to quit): "
            handIndex = int(input(prompt))
            if handIndex == 0:
                exit()
            print()
            card1 = game.player1.play_card(handIndex-1)
            print("Player 1 plays the {:s} of {:s}".format(card1.rank, card1.suit))
            print()
            winner = game.card_cmp(card2, card1)
            if winner == 2:
                print("Player 1 wins")
                game.player1.score += card1.value + card2.value
                winner = game.player1
                if game.deck.count() > 0:
                    game.deal_card(game.player1, game.player2)
            else:
                print("Player 2 wins")
                game.player2.score += card1.value + card2.value
                winner = game.player2
                if game.deck.count() > 0:
                    game.deal_card(game.player2, game.player1)
        bot.memory_insert(card1)
        if bot.player.count() > 0:
            bot.memory_insert(bot.player.hand[-1])
        print()

    print("Score:")
    print("Player 1: {:d}".format(game.player1.score))
    print("Player 2: {:d}".format(game.player2.score))
    print()
    answer = input("Play again? (y/n): ")
    if answer != 'y':
        over = True
        