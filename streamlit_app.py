import streamlit as st
from pyspark.sql import SparkSession
from pyspark.sql.functions import lit
from pyspark.ml import PipelineModel
from StemmerTransformer import StemmerTransformer


@st.cache_resource
def load_spark():
    spark = SparkSession.builder \
        .appName("SpamDetectorApp") \
        .config("spark.sql.shuffle.partitions", "4") \
        .getOrCreate()
    return spark

spark = load_spark()

@st.cache_resource
def load_model():
    model = PipelineModel.load("/app/models/best_lr_pipeline")
    return model

model = load_model()

st.title("📧 Intelligent Spam Email Detector")
st.write("Enter an email below and the trained Spark model will classify it as Spam or Not Spam.")

email_text = st.text_area("✉️ Write or paste your email here:", height=250)

if st.button("🔍 Detect"):
    if email_text.strip() == "":
        st.warning("Please enter an email.")
    else:
        df = spark.createDataFrame([(email_text,)], ["text"])

        preds = model.transform(df).select("text", "prediction").collect()[0]
        prediction = preds["prediction"]

        if prediction == 1:
            st.error("🚨 **SPAM detected!**")
        else:
            st.success("✅ **This email is safe (HAM)**")
