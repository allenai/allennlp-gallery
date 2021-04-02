This is an implementation of the CopyNet model from the paper [Incorporating Copying Mechanism in Sequence-to-Sequence Learning](https://api.semanticscholar.org/CorpusID:8174613).
CopyNet is an seq2seq encoder-decoder model with a decoder that is capable of copying tokens from the source sentence into the target sentence instead of generating all target tokens only from the target vocabulary.

It is very similar to a typical seq2seq model used in neural machine translation tasks, for example, except that in addition to providing a "generation" score at each timestep for the tokens in the target vocabulary, it also provides a "copy" score for each token that appears in the source sentence. In other words, you can think of CopyNet as a seq2seq model with a dynamic target vocabulary that changes based on the tokens in the source sentence, allowing it to predict tokens that are out-of-vocabulary (OOV) with respect to the actual target vocab.

This model is maintained by the AllenNLP team and its contributors on the AllenNLP models repository at [https://github.com/allenai/allennlp-models](https://github.com/allenai/allennlp-models).
