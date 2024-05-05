from random_word import RandomWords
from pyleetspeak import LeetSpeaker
import sys

def main():
    count = int(sys.argv[1]) if len(sys.argv)== 2 else 10

    leeter = LeetSpeaker.LeetSpeaker(
        change_prb=0.8,
        change_frq=0.5,
        mode="basic",
        verbose=False)

    r = RandomWords()
    words = [r.get_random_word() for _ in range(count)]
    for word in words:
        print(f"{word:20s}: {leeter.text2leet(word)}")

if __name__ == "__main__":
    main()
