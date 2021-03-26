The basic outline of this model is to get an embedded representation of each span in the document. These span representations are scored and used to prune away spans that are unlikely to occur in a coreference cluster. For the remaining spans, the model decides which antecedent span (if any) they are coreferent with. The resulting coreference links, after applying transitivity, imply a clustering of the spans in the document. The GloVe embeddings in the original paper have been substituted with SpanBERT embeddings.

This model is maintained by the AllenNLP team and its contributors on the AllenNLP
models repository at [https://github.com/allenai/allennlp-models](https://github.com/allenai/allennlp-models).
