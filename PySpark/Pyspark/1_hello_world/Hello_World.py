import os
os.environ['PYSPARK_PYTHON'] = 'python'
os.environ['HADOOP_HOME'] = "C:\\hadoop"


from pyspark.sql import SparkSession

spark = (SparkSession.builder
         .appName("Datacamp Pyspark Tutorial")
         .master("local[*]")
         .config("spark.driver.host","10g")
         .config("spark.memory.offHeap.size","10g")
         .getOrCreate())

iris_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
df = spark.read.csv(iris_url, 
                    header=False, 
                    inferSchema=True)
df.show()

