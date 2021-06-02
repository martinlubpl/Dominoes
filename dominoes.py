# Write your code here
import random


# generate dominoes
def generate_deck():
    deck = []
    for n in range(7):
        for m in range(n, 7):
            domino = [n, m]
            deck.append(domino)
    random.shuffle(deck)
    return deck


def generate_pieces():
    global full_deck
    c_deck = full_deck[:7]
    del full_deck[:7]
    return c_deck


def player_move():
    print("\nIt's your turn to make a move. Enter your command.")
    while True:
        try:
            move = int(input())
            if abs(move) > len(player_deck):
                print("Invalid input. Please try again.")
                continue
            # check if legal, 0 is always legal
            if not is_legal(move, player_deck):
                print("Illegal move. Please try again.")
                continue
            if move < 0:
                moved_domino = correct_orientation(player_deck.pop(abs(move) - 1), side="left")
                snake.insert(0, moved_domino)
            elif move == 0:
                if len(full_deck):
                    player_deck.append(full_deck.pop())
            else:  # move>0
                moved_domino = correct_orientation(player_deck.pop(move - 1), side="right")
                snake.append(moved_domino)
            break
        except ValueError:
            print("Invalid input. Please try again.")
            continue


def computer_move():
    print("\nStatus: Computer is about to make a move. Press Enter to continue...")
    input()
    computer_size = len(computer_deck)
    while True:
        move = ai_move()
        if not is_legal(move, computer_deck):
            # print("Illegal move. Please try again.")
            continue
        if move < 0:
            moved_domino = correct_orientation(computer_deck.pop(abs(move) - 1), side="left")
            snake.insert(0, moved_domino)
        elif move == 0:
            if len(full_deck):
                computer_deck.append(full_deck.pop())
        else:
            moved_domino = correct_orientation(computer_deck.pop(move - 1), side="right")
            snake.append(moved_domino)
        break


def ai_move():
    # count points for 0-6
    points = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    for item in snake:
        points[item[0]] += 1
        points[item[1]] += 1
    for item in computer_deck:
        points[item[0]] += 1
        points[item[1]] += 1
    # print(points)

    # score dominoes
    scores_for_dominoes = {}
    for number, item in enumerate(computer_deck):
        scores_for_dominoes[number] = points[item[0]] + points[item[1]]
    # print("scores for dominoes: ", scores_for_dominoes)
    sorted_scores = dict(sorted(scores_for_dominoes.items(), key=lambda it: it[1], reverse=True))
    # print("sorted scores ", sorted_scores)
    for key, value in sorted_scores.items():
        if is_legal(key + 1, computer_deck):
            # print("legal", key+1)
            return key + 1
        if is_legal(-key - 1, computer_deck):
            # print(f"legal -{key+1}")
            return -(key + 1)
    return 0


def correct_orientation(domino, side):
    if side == "left" and domino[1] != snake[0][0]:
        return [domino[1], domino[0]]
    elif side == "right" and domino[0] != snake[-1][1]:
        return [domino[1], domino[0]]
    return domino


def is_legal(move, deck):
    if move > 0:
        return snake[-1][1] in deck[move - 1] or snake[-1][1] in deck[move - 1]
    elif move == 0:
        # always legal
        return True
    else:
        return snake[0][0] in deck[abs(move) - 1] or snake[0][0] in deck[abs(move) - 1]


def print_table():
    print("======================================================================")
    print(f"Stock size: {len(full_deck)}")
    print(f"Computer pieces: {len(computer_deck)}\n")
    # print(f"Computer pieces: {computer_deck}\n")
    snake_printed = ""
    if len(snake) < 7:
        for item in snake:
            snake_printed += str(item)
    else:
        for item in snake[:3]:
            snake_printed += str(item)
        snake_printed += "..."
        for item in snake[-3:]:
            snake_printed += str(item)

    print(snake_printed)
    print("\nYour pieces:")
    for count, domino in enumerate(player_deck):
        print(f"{count + 1}: {domino}")


def check_game():
    if len(player_deck) == 0:
        print_table()
        print("Status: The game is over. You won!")
        return False
    elif len(computer_deck) == 0:
        print_table()
        print("\nStatus: The game is over. The computer won!")
        return False
    elif game_draw():
        print("\nStatus: The game is over. It's a draw!")
        return False
    return True


def game_draw():
    """returns True when The numbers on the ends of the snake are identical and appear within the snake 8 times"""
    if snake[0][0] == snake[-1][1]:
        count = 0
        for item in snake:
            if item[0] == snake[0][0]:
                count += 1
            if item[1] == snake[0][0]:
                count += 1
        if count == 8:
            return True
    return False


# deal until comp/user has snake top
snake_top = -1
while snake_top == -1:
    full_deck = generate_deck()
    computer_deck = generate_pieces()
    player_deck = generate_pieces()

    # search through 2 players and 7 pieces
    both_players = [computer_deck, player_deck]

    for i in range(2):
        for j in range(7):
            if both_players[i][j][0] == both_players[i][j][1] and snake_top < both_players[i][j][0]:
                snake_top = both_players[i][j][0]
                snake_player = i
                snake_index = j

# print(f"{snake_top} {snake_player} {snake_index}")

if snake_player == 0:
    snake = [computer_deck.pop(snake_index)]
    status = "player"
else:
    snake = [player_deck.pop(snake_index)]
    status = "computer"

game_on = True

while game_on:
    print_table()
    if status == "player":
        player_move()
        status = "computer"
    else:
        computer_move()
        status = "player"

    game_on = check_game()
