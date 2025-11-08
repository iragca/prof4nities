from prof4nities.models import Character, Characters

text = "example fuc k text"


letters = [Character(letter=char, index=i) for i, char in enumerate(text)]


no_spaces = Characters(letter for letter in letters if not letter.is_space)

found_letters = no_spaces.find_substring("fuck")
start_index = found_letters[0].index if found_letters else -1
end_index = found_letters[-1].index if found_letters else -1

print(
    f"{text[:start_index]}{(end_index - start_index + 1) * '*'}{text[end_index + 1 :]}"
)
