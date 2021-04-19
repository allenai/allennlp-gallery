While high performance has been obtained for dependency parsing of high-resource languages, performance for low-resource languages lags behind. In this paper we focus on the parsing of the low-resource language Frisian. We use a sample of code-switched, spontaneously spoken data, which proves to be a challenging setup. We propose to train a parser specifically tailored towards the target domain, by selecting instances from multiple treebanks. Specifically, we use Latent Dirichlet Allocation (LDA), with word and character N-gram features. The best single source treebank (NL ALPINO) resulted in an LAS of 54.7 whereas our data selection outperformed the single best transfer treebank and led to 55.6 LAS on the test data. Additional experiments consisted of removing diacritics from our Frisian data, creating more similar training data by cropping sentences and running our best model using XLM-R. These experiments did not lead to a better performance.

This work uses [MaChAmp](machamp), which is based on AllenNLP.