import matplotlib.pyplot as plt
from IPython import display

plt.ion()


def plot(scores, mean_scores):
    display.clear_output(wait=True)
    #display.display(plt.gcf())
    plt.clf()

    plt.title('Snake AI Model', fontsize=14, fontweight='bold')
    plt.xlabel('Number of Games', fontsize=12)
    plt.ylabel('Score', fontsize=12)

    plt.plot(scores, label='Score per Game', color='blue', linestyle='-', linewidth=2, marker='o')
    plt.plot(mean_scores, label='Mean Score', color='green', linestyle='--', linewidth=2, marker='x')

    plt.ylim(ymin=0)
    plt.xlim(xmin=0)

    plt.grid(True, which='both', linestyle='--', linewidth=0.5)

    plt.text(len(scores) - 1, scores[-1], f'{scores[-1]}', fontsize=10, ha='center', va='bottom', color='blue')
    plt.text(len(mean_scores) - 1, mean_scores[-1], f'{mean_scores[-1]:.2f}', fontsize=10, ha='center', va='bottom',
             color='green')

    plt.legend(loc='upper left', fontsize=10)

    plt.tight_layout()
    plt.show(block=False)
    plt.pause(0.1)

    if len(scores) > 10 and scores[-1] == max(scores):
        plt.annotate('New High Score!',
                     xy=(len(scores) - 1, scores[-1]),
                     xytext=(len(scores) - 10, scores[-1] + 10),
                     arrowprops=dict(facecolor='red', shrink=0.05),
                     fontsize=12, color='red')
