import pandas as pd
import weaviate.classes.config as wc
import weaviate.classes as wvc
from connection import connectDB
from weaviate.util import generate_uuid5


vectorizer_model = "sentence-transformers/all-MiniLM-L6-v2"

try:
    client = connectDB()

    df = pd.read_csv("book_data.csv")

    col_drop = [
        "bookId",
        "series",
        "isbn",
        "characters",
        "bookFormat",
        "edition",
        "pages",
        "publisher",
        "publishDate",
        "firstPublishDate",
        "awards",
        "numRatings",
        "ratingsByStars",
        "likedPercent",
        "setting",
        "coverImg",
        "bbeScore",
        "bbeVotes",
        "price",
    ]
    df = df.drop(col_drop, axis=1)

    print("Remaining columns:\n", df.columns)

    client.collections.create(
        name="Book_Data",
        vectorizer_config=wc.Configure.Vectorizer.text2vec_huggingface(
            model=vectorizer_model
        ),
        properties=[
            wc.Property(name="title", data_type=wc.DataType.TEXT),
            wc.Property(name="author", data_type=wc.DataType.TEXT),
            wc.Property(name="rating", data_type=wc.DataType.NUMBER),
            wc.Property(name="language", data_type=wc.DataType.TEXT),
            wc.Property(name="genre", data_type=wc.DataType.TEXT),
            wc.Property(name="description", data_type=wc.DataType.TEXT),
        ],
    )
    print("Collection Created...")

    collection = client.collections.get("Book_Data")
    data_objs = []

    for i, row in df.iterrows():
        try:
            props = {
                "title": row["title"],
                "author": row["author"],
                "rating": row["rating"],
                "genre": row["genres"],
                "language": row["language"],
                "description": row["description"],
            }

            book_uuid = generate_uuid5(row["title"] + str(i))
            data_object = wvc.data.DataObject(properties=props, uuid=book_uuid)
            data_objs.append(data_object)

        except Exception as row_error:
            print(f"Error at row {i+1}: {str(row_error)}")
            continue

    if data_objs:
        collection.data.insert_many(data_objs)
        print("All Data Inserted...")

except Exception as e:
    print(f"Fatal Error: {str(e)}")

finally:
    client.close()
    print("Closing Connection...")
