from Load_T5_model import TextGenerationUtility



def main():
    # Test load_model Text generation.
    tokenizer, model_saved = TextGenerationUtility.load_Model()
    print(TextGenerationUtility.generate('Amy | pet |  cat ', model_saved, tokenizer))
    



if __name__ == "__main__":
    main()