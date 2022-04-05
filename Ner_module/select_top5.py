from collections import Counter 

def select_top(lst):
    #lst will be in format List[List[]]
    flatList = [el for sublist in lst for el in sublist]
    word_counts = Counter(flatList)
    top_five = word_counts.most_common(5)
    return top_five
              

lst =  [
      [
        "cool",
        "dog",
        "breeds",
        "cat",
        "owners",
        "5",
        "easy",
        "train",
        "pups",
        "hello"
      ],
      [
        "10",
        "cutest",
        "dog",
        "breeds"
      ],
      [
        "10",
        "cutest",
        "dog",
        "breeds",
        "2022",
        "love",
        "goldens"
      ],
      [
        "15",
        "cute",
        "dog",
        "breeds",
        "cool",
        "cutest",
        "able",
        "resist",
        "southern",
        "living"
      ]
    ]
print(select_top(lst))