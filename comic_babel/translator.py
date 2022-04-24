import os
from typing import Optional

from deep_translator import DeeplTranslator, GoogleTranslator


def translate(
        text: str, source_lang: str = "auto", target_lang: str = "spanish",
        translator: str = "google", api_key: Optional[str] = None,
) -> str:
    if translator == "google":
        translator = GoogleTranslator(source=source_lang, target=target_lang)
    elif translator == "deepl":
        translator = DeeplTranslator(source=source_lang, target=target_lang, api_key=api_key)
    else:
        raise ValueError("Specify a valid translator")

    return translator.translate(text) or text


def translate_from_file(
        filename: str, source_lang: str = "auto", target_lang: str = "spanish",
        translator: str = "google", api_key: Optional[str] = None,
        separator: Optional[str] = None,
) -> None:
    if translator == "google":
        translator = GoogleTranslator(source=source_lang, target=target_lang)
    elif translator == "deepl":
        translator = DeeplTranslator(source=source_lang, target=target_lang, api_key=api_key)
    else:
        raise ValueError("Specify a valid translator")

    with open(filename) as file:
        lines = file.readlines()

    new_name = os.path.splitext(filename)[0] + "_translated_with_%s.txt" % (translator)
    with open(new_name, "w") as file:
        chunk_to_translate = ""
        n_characters = 0
        for line in lines:

            if n_characters < 4500 and separator and not (line == separator):
                chunk_to_translate += line
                n_characters += len(line)

            else:
                # save left over readed and put next in blank for next leftover
                if (line == "\n"):
                    chunk_to_translate = chunk_to_translate.replace("\n", " ")

                chunk_tranlated = translator.translate(chunk_to_translate)
                chunk_tranlated = chunk_tranlated or ""
                if type(chunk_tranlated) == str:
                    chunk_tranlated += "\n\n"

                file.write(chunk_tranlated)
                chunk_to_translate = line
                n_characters = len(line)


if __name__ == '__main__':
    pass
