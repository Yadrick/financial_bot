from for_test.for_test import sum_word


def test_sum_word():
    word_1 = "hello"
    word_2 = "jandos"
    correct_answer = "hellojandos"

    answer = sum_word(word_1, word_2)

    assert answer == correct_answer
