import secrets, math


def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n * multiplier + 0.9999) / multiplier


def spin_true_random_roulette():
    return secrets.randbelow(37)


def get_bet_numbers(mode, first_half=False, numbers=None):

    if mode == "reset":
        return set(range(1,19)) if not first_half else set(range(19, 37))
    elif mode == "add_zero":
        try:
            numbers.add(0)
            return numbers
        except:
            return set(range(1,19)) if not first_half else set(range(19, 37))
    elif mode == "misdirection":
        # INCLUDES A RANDOM BET SYSTEM, GENERATES A RANDOM NUMBER BETWEEN 0-9999
        # IF IT IS EVEN IT RETURN BLACK NUMBERS, IF IT IS ODD IT RETURN RED NUMBERS
        random_num = secrets.randbelow(10000)
        return "blacks" if random_num % 2 == 0 else "reds"
    else:
        return numbers


def compute_next_bet(current_bet):
    if reset_threshold == 0:
        return current_bet * multiplier

    threshold = minimum_bet * multiplier * reset_threshold
    if (aggro_mode and current_bet > threshold) or (not aggro_mode and current_bet >= threshold):
        return minimum_bet

    return current_bet * multiplier


def print_verbose(throw, bet, current_bet, balance, win_amount=0):
    outcome = "GANA - FUCK YEAH" if win_amount > 0 else "PIERDE - FUCKING SHIT"
    print(f"{outcome} - Lanzamiento: {throw} - Apuesta por numero: {current_bet} - Apuesta total: {bet} - {'Beneficio:' if win_amount > 0 else 'Balance actual:'} {balance if win_amount == 0 else win_amount}")


def roulette():

    first_half = False
    balance = initial_balance
    current_bet = minimum_bet
    betting_set = get_bet_numbers("reset", first_half)

    for _ in range(rounds_by_play):
        
        if profit_limit > 1 and balance >= initial_balance * profit_limit:
            print(f"Alcanzado el límite de beneficios para el juego actual. Balance: {balance}.\nNos vamos de la mesa.")
            break

        bet = round_up(len(betting_set) * current_bet, decimals=2)
        if bet > balance:
            print(f"Se considera que hemos entrado en bancarrota. Balance: {balance} - Apuesta por número: {current_bet} - Apuesta total: {bet}")
            break

        current_throw = spin_true_random_roulette()
        balance = round_up((balance - bet), decimals=2)

        if current_throw in betting_set:
            win_amount = round_up(current_bet * 35, decimals=2)
            balance += win_amount

            if verbose:
                print_verbose(current_throw, bet, current_bet, balance, win_amount)

        else:
            if verbose:
                print_verbose(current_throw, bet, current_bet, balance)

            betting_set = get_bet_numbers("add_zero", False, betting_set)
            current_bet = compute_next_bet(current_bet)
        
            if verbose and current_bet == minimum_bet:
                print(f"Alcanzada la máxima racha de perdidas permitida: {reset_threshold} - Reiniciando el monto de apuestas y la secuencia.")

        if current_bet == minimum_bet or current_throw in betting_set:
            first_half = not first_half
            betting_set = get_bet_numbers("reset", first_half)
            current_bet = minimum_bet

    return round_up(balance, decimals=2)


def summary(results, balance, plays):
    total_invested = balance * plays
    final_balance = sum(results)
    result = final_balance - total_invested

    stats = {
        "losses": sum(result < balance for result in results),
        "wins": sum(result > balance for result in results),
        "ties": sum(result == balance for result in results)
    }

    loss_percentage = round_up((stats["losses"] / plays) * 100, 2)
    win_percentage = round_up((stats["wins"] / plays) * 100, 2)

    summary_messages = [
        f"Plays: {plays}",
        f"Losses: {stats['losses']} ({loss_percentage}%)",
        f"Wins: {stats['wins']} ({win_percentage}%)",
        f"Ties: {stats['ties']}",
        f"Invested: {total_invested}",
        f"Final Balance: {final_balance}",
        f"Outcome: {'Favorable' if result > 0 else 'Unfavorable' if result < 0 else 'Neutral'} ({result})"
    ]

    for message in summary_messages:
        print(message)


if __name__ == '__main__':

    verbose = False
    aggro_mode = False       # ENABLE (True) TO REACH THE MAXIMUM RESTART LIMIT, DISABLE (False) TO LIMIT LOSSES

    plays = 100000
    initial_balance = 1000
    rounds_by_play = 10     # 1 ROUND ~= 50 SECONDS, 72 ROUNDS ~= 1 HOUR SESSION
    minimum_bet = 0.2
    multiplier = 2
    reset_threshold = 6     # 0 FOR NONE // CONSECUTIVE LOSING STREAK TO RESET
    profit_limit = 1.3     # X TIMES INITIAL BALANCE -> IF INITIAL_BALANCE == 100 AND PROFIT_LIMIT == 2 -> END CURRENT SESSION WHEN BALANCE >= 200 
    
    results = []

    for i in range(plays):
        new_result = roulette()

        if verbose:
            print(f"Jugada n_ {i+1} - Resultado: {new_result}")
        
        results.append(new_result)

    print(f"Tests completed.")
    print(f"Initial Balance: {initial_balance}")
    print(f"Rounds by play: {rounds_by_play}")
    print(f"Minimum bet: {minimum_bet}")
    print(f"Multiplier Factor: {multiplier}")
    print(f"Reset threshold: {reset_threshold}")
    print(f"Take Profit and Run Away: {profit_limit}")

    summary(results, initial_balance, plays)
