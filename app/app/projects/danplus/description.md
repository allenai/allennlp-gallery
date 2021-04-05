This paper introduces DAN+, a new multi-domain corpus and annotation guidelines for Danish nested named entities (NEs) and lexical normalization to support research on cross-lingual cross-domain learning for a less-resourced language. We empirically assess three strategies to model the two-layer Named Entity Recognition (NER) task. We compare transfer capabilities from German versus in-language annotation from scratch. We examine language-specific versus multilingual BERT, and study the effect of lexical normalization on NER. Our results show that

1. the most robust strategy is multi-task learning which is rivaled by multi-label decoding,
2. BERT-based NER models are sensitive to domain shifts, and
3. in-language BERT and lexical normalization are the most beneficial on the least canonical data.
   
Our results also show that an out-of-domain setup remains challenging, while performance on news plateaus quickly. This highlights the importance of cross-domain evaluation of cross-lingual transfer.

This work uses [MaChAmp](machamp), which is based on AllenNLP.
