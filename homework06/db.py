from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def fill(dictionary):
    s = session()
    news = News(
        title=dictionary["title"],
        author=dictionary["author"],
        url=dictionary["url"],
        comments=dictionary["comments"],
        points=dictionary["points"],
    )
    s.add(news)
    s.commit()


Base = declarative_base()
engine = create_engine("sqlite:///news.db")
session = sessionmaker(bind=engine)


class News(Base):  # type: ignore
    __tablename__ = "news"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    url = Column(String)
    comments = Column(Integer)
    points = Column(Integer)
    label = Column(String)


Base.metadata.create_all(bind=engine)
