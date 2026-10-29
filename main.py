from processor import Processor

def main():
    processor = Processor("var1.csv")
    df = processor.process()

    if df is not None:
        print(f"Кол-во строк: {len(df)}")

if __name__ == "__main__":
    main()
