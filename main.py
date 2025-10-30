from pipeline.pipeline import Pipeline


if __name__ == "__main__":
    try:
        my_pipeline = Pipeline()
        my_pipeline.run()
    except Exception as e:
        print(f"An error occured: {e}")
