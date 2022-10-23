from typing import List

import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')
plt.style.use('ggplot')


def get_title(history_len, env) -> str:
    return f"Learning mode : {env['LEARNING_TYPE']}\n" \
           f"α={env['AGENT_LEARNING_RATE']}, γ={env['AGENT_GAMMA']}\n" \
           f"Visible lines above: {env['AGENT_VISIBLE_LINES_ABOVE']}, " \
           f"visible columns arround: {env['AGENT_VISIBLE_COLS_ARROUND']}\n" \
           f"Total iterations: {history_len * env['QTABLE_HISTORY_PACKETS']}"


def extract_history(history_file_path: str, env):
    complete_history = []
    print(f"Reading history from {history_file_path}")
    with open(history_file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if len(line) > 0:
                complete_history.append(float(line))
    print(f"History read, {len(complete_history)} values")

    fragment_count = len(complete_history) // 500
    if fragment_count > 0:
        history = []
        for i in range(0, len(complete_history), fragment_count):
            history.append(complete_history[i:i + fragment_count])

        plt.plot(list(map(avg, history)), label="Score average")
        plt.xlabel(f"Iteration (x{env['QTABLE_HISTORY_PACKETS'] * fragment_count})")
        plt.ylabel("Score average")
        plt.title(get_title(len(complete_history), env))
        plt.gcf().set_size_inches(20, 11)
        plt.tight_layout()

        filename = find_available_filename(history_file_path)
        plt.savefig(filename, dpi=300, pil_kwargs={'quality': 100})
        plt.close()
        print(f"History saved to {filename}")


def avg(l: List[float]) -> float:
    return sum(l) / len(l)


def find_available_filename(filename: str) -> str:
    return filename + ".png"
    # if not os.path.exists(filename + ".png"):
    #     pass
    # i = 1
    # while os.path.exists(filename + f" ({i}).png"):
    #     i += 1
    # return filename + f" ({i}).png"


def rate(history: List[float]):
    return len(list(filter(lambda x: x > 0, history))) / len(history) * 100
