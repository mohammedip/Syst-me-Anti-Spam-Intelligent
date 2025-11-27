from pyspark.sql.functions import udf, col
from pyspark.ml import Transformer
from pyspark.ml.util import DefaultParamsReadable, DefaultParamsWritable
from pyspark.sql.types import ArrayType, StringType
from nltk.stem import PorterStemmer


class StemmerTransformer(Transformer, DefaultParamsReadable, DefaultParamsWritable):

    def __init__(self, inputCol="tokens_no_sw", outputCol="stemmed_tokens"):
        super().__init__()
        self.inputCol = inputCol
        self.outputCol = outputCol
        self.stem_udf = udf(self.stem_words, ArrayType(StringType()))

    def stem_words(self, tokens):
        if tokens is None:
            return []
        ps = PorterStemmer()
        return [ps.stem(t) for t in tokens]

    def _transform(self, dataset):
        return dataset.withColumn(self.outputCol, self.stem_udf(col(self.inputCol)))
