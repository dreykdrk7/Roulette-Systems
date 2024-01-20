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
    else:
        return numbers


def compute_next_bet(current_bet, win):

    if win:
        return round_up(max(current_bet - unit_step, minimum_bet), decimals=2)
    else:
        return round_up((current_bet + unit_step), decimals=2)


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
            if verbose:
                print(f"Alcanzado el límite de beneficios para el juego actual. Balance: {balance}.\nNos vamos de la mesa.")
            break
        
        if stop_loss > 0 and balance < initial_balance * stop_loss:
            if verbose:
                print(f"Alcanzado el límite de perdidas asumible para el juego actual. Balance: {balance}.\nNos vamos de la mesa.")
            break

        bet = round_up(len(betting_set) * current_bet, decimals=2)
        if bet > balance:
            if verbose:
                print(f"Se considera que hemos entrado en bancarrota. Balance: {balance} - Apuesta por número: {current_bet} - Apuesta total: {bet}")
            break

        current_throw = spin_true_random_roulette()
        balance = round_up((balance - bet), decimals=2)
        win = current_throw in betting_set

        if win:
            win_amount = round_up(current_bet * 35, decimals=2)
            balance += win_amount

            first_half = not first_half
            betting_set = get_bet_numbers("reset", first_half)

            if verbose:
                print_verbose(current_throw, bet, current_bet, balance, win_amount)

        else:
            betting_set = get_bet_numbers("add_zero", False, betting_set)

            if verbose:
                print_verbose(current_throw, bet, current_bet, balance)

        current_bet = compute_next_bet(current_bet, win)

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

    plays = 100000
    initial_balance = 300
    rounds_by_play = 35     # 1 ROUND ~= 50 SECONDS, 72 ROUNDS ~= 1 HOUR SESSION
    minimum_bet = 1.5
    unit_step = 0.5
    profit_limit = 1.1      # X TIMES INITIAL BALANCE -> IF INITIAL_BALANCE == 100 AND PROFIT_LIMIT == 2 -> END CURRENT SESSION WHEN BALANCE >= 200 
    stop_loss = 0         # SHOULD BE > 0 // IF INITIAL_BALANCE == 100 AND STOP_LOSS == 0.8 -> END CURRENT SESSION WHEN BALANCE < 80
    results = []

    for i in range(plays):
        new_result = roulette()

        if verbose:
            print(f"Jugada n_ {i+1} - Resultado: {new_result}")
        
        results.append(new_result)

    print(f"D'Alembert System -- Tests completed.")
    print(f"Initial Balance: {initial_balance}")
    print(f"Rounds by play: {rounds_by_play}")
    print(f"Minimum bet: {minimum_bet}")
    print(f"Unit Step: {unit_step}")
    print(f"Take Profit and Run Away: {profit_limit}")
    print(f"Stop Loss: {stop_loss}" if stop_loss > 0 else "")

    summary(results, initial_balance, plays)
