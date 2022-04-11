import os
from deep_translator import DeeplTranslator, GoogleTranslator

key = ""

def translate(methodology="google", source_lang="auto", target_lang="spanish", file_name=None, string=None, api_key=None, save_file):
    """
    save_file: file to save the translation done, it always used as a default when a input file is given. If return_string==true, it will
        try to return a  string, always that the input has less than 5000 characters.
    """
    
    # Initialize the translator 
    if methodology == 'google':
        Translator = GoogleTranslator(source=source_lang, target=target_lang)
    elif methodology == "deepl":
        Translator = DeeplTranslator(source=source_lang, target=target_lang, api_key=api_key)
    else:
        print("please enter a valid methodology, choose google or deepl")
        exit(0)


    if file_name == None and string != None:
        return Translator.translate(string)

    elif file_name != None and string == None:
        if 

        file1 = open(file_name, 'r')
        Lines = file1.readlines()


    else:
        print("please enter a valid filname or string: file_name %s and string %s" % (file_name, string) )
        exit(0)


def examples():        
    to_translate = 'I want to translate this text'
    translated = translate(source_lang='auto', target_lang="de", string=to_translate)

    print("English")
    print(to_translate)

    print("\nDeutch")
    print(translated)


    print("*" * 100)
    print("Translating short poem")
    dir_data_test = os.path.dirname(os.path.realpath(__file__)) + "/../../tests/test_data/"
    file_name = "translate_test1.txt"
    file_to_translate = dir_data_test + "translate_test1.txt"

    methods = ["google", "deepl"]

    for methodology in methods[:1]:
        print(methodology)
        translated = translate(source_lang='auto', target_lang='spanish', file_name=file_to_translate, methodology=methodology)
        save_file_name = dir_data_test + os.path.splitext(file_name)[0] + "_translated_with_%s.txt" % (methodology)

        text_file = open(save_file_name , "w")
        text_file.write(translated)
        text_file.close()

    print("*" * 100)
    print("Translating complete book")

    dir_data_test = os.path.dirname(os.path.realpath(__file__)) + "/../../tests/test_data/"
    file_name = "Book 1 - The Philosopher's Stone.txt"
    file_to_translate = dir_data_test + "Book 1 - The Philosopher's Stone.txt"

    for methodology in methods[:1]:
        print(methodology)
        translated = translate(source_lang='auto', target_lang='spanish', file_name=file_to_translate, methodology=methodology)
        save_file_name = dir_data_test + os.path.splitext(file_name)[0] + "_translated_with_%s.txt" % (methodology)

        text_file = open(save_file_name , "w")
        text_file.write(translated)
        text_file.close()



if __name__ == '__main__':
    examples()