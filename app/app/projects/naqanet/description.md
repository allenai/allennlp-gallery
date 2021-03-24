An augmented version of QANet that adds rudimentary numerical reasoning ability, trained on DROP
(Dua et al., 2019), as published in the original DROP paper.

An augmented version of QANet model with some rudimentary numerical reasoning
abilities. The main idea here is that instead of just predicting a passage span
after doing all of the QANet modeling stuff, we add several different
'answer abilities': predicting a span from the question, predicting a count, or
predicting an arithmetic expression. Near the end of the QANet model, we have a
variable that predicts what kind of answer type we need, and each branch has
separate modeling logic to predict that answer type. We then marginalize over
all possible ways of getting to the right answer through each of these answer types.

This model is maintained by the AllenNLP team and its contributors on the AllenNLP
models repository at https://github.com/allenai/allennlp-models.

It achieves 51% F1 and 47% exact match on the DROP validation set.
