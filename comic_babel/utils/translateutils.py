import os

from googletrans import Translator

from deep_translator import DeeplTranslator, GoogleTranslator

key = ""

def translate(methodology="google", source_lang="auto", target_lang="spanish", file_name=None, string=None):
    # Initialize the translator 
    if methodology == 'google':
        Translator = GoogleTranslator()
    else:
        Translator = DeeplTranslator()


    if file_name != None and string == None:
        return Translator(source='auto', target='spanish').translate(string)

    elif file_name == None and string != None:  
        pass

    else:
        print("please enter a valid filname or string")
        exit(0)


def examples():        
    to_translate = 'I want to translate this text'
    translated = GoogleTranslator(source='auto', target='de').translate(to_translate)

    print("English")
    print(to_translate)

    print("\nDeutch")
    print(translated)

    dir_data_test = os.path.dirname(os.path.realpath(__file__)) + "/../tests/test_data/"
    file_name = "translate_test1.txt"
    file_to_translate = dir_data_test + "translate_test1.txt"

    translate_classes = [GoogleTranslator, DeeplTranslator]

    for Translator in translate_classes:
        print(Translator.__name__)
        translated = Translator(source='auto', target='spanish').translate_file(file_to_translate)
        save_file_name = dir_data_test + os.path.splitext(file_name)[0] + "_translated_with_%s.txt" % (Translator.__name__)

        text_file = open(save_file_name , "w")
        text_file.write(translated)
        text_file.close()
