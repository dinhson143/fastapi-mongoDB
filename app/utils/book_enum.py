from enum import Enum


class BookTypeEnum(str, Enum):
    EBOOK = 'ebook'
    PAPERBACK = 'paperback'
    AUDIOBOOK = 'audiobook'


class Genre(str, Enum):
    FICTION = "Fiction"
    NON_FICTION = "Non-Fiction"
    FANTASY = "Fantasy"
    BIOGRAPHY = "Biography"
    SCIENCE_FICTION = "Science Fiction"
    MYSTERY = "Mystery"
    THRILLER = "Thriller"
    ROMANCE = "Romance"
    OTHER = "Other"
