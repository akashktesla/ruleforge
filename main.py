import pandas as pd


def clean_with_policy(df,policy):
    print(f"policy: {policy}")


if __name__ == "__main__":
    df = pd.read_csv("datasets/spaceship-titanic/train.csv");
    print(df.head())
    policy = [{
                  "column":"akash",
              },]



