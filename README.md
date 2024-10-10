## **Project structure:**
1. Structuring based on File-Type
2. **References**:
* https://fastapi.tiangolo.com/tutorial/bigger-applications/
* https://medium.com/@amirm.lavasani/how-to-structure-your-fastapi-projects-0219a6600a8f


    ├── app  # Contains the main application files.
    │   ├── __init__.py   # this file makes "app" a "Python package"
    │   ├── main.py       # Initializes the FastAPI application.
    │   ├── dependencies.py # Defines dependencies used by the routers
    │   ├── routers
    │   │   ├── __init__.py
    │   │   ├── items.py  # Defines routes and endpoints related to items.
    │   │   ├── book.py  # Defines routes and endpoints related to books.
    │   │   └── author.py  # Defines routes and endpoints related to authors.
    │   ├── crud
    │   │   ├── __init__.py
    │   │   ├── book.py  # Defines CRUD operations for books.
    │   │   └──  author.py  # Defines CRUD operations for authors.
    │   ├── schemas
    │   │   ├── __init__.py
    │   │   ├── book.py  # Defines schemas for books.
    │   │   └──  author.py  # Defines schemas for authors.
    │   ├── models
    │   │   ├── __init__.py
    │   │   ├── book.py  # Defines database models for books.
    │   │   └──  author.py  # Defines database models for authors.
    │   ├── external_services
    │   │   ├── __init__.py
    │   │   └──  aws.py          # Defines functions for s3_service.
    │   └── utils
    │       ├── __init__.py
    │       └── book_enum.py  # Defines functions for authentication.
    ├── tests
    │   ├── __init__.py
    │   ├── test_books.py  # Tests for the books module.
    │   └── test_authors.py  # Tests for the authors module.
    ├── requirements.txt
    ├── .gitignore
    └── README.md


## **Knowledge**

**Schema design patterns:**
* The Inheritance Pattern
* The Computed Pattern
* The Approximation Pattern
* The Extended Reference Pattern
* The Schema Versioning Pattern
* The Single Collection Pattern
* The Subset Pattern
* The Bucket Pattern
* The Outlier Pattern
* The Archive Pattern

**Indexing Strategies:**
* Use the ESR (Equality, Sort, Range) Rule
* Create Indexes to Support Your Queries
* Use Indexes to Sort Query Results


**References:**
1. https://python-dependency-injector.ets-labs.org/introduction/index.html
2. https://fastapi.tiangolo.com/learn/
3. https://github.com/teamhide/fastapi-boilerplate
4. https://learn.mongodb.com/learn/learning-path/data-modeling-for-mongodb
5. https://github.com/zhanymkanov/fastapi-best-practices
6. https://www.mongodb.com/docs/manual/applications/indexes/

**Key requirements:**
* Use MongoDB as the database
* Define a data schema and access patterns, including index strategies
* Use the FastAPI framework
* Utilize the Dependency Injector library
* A flexible project structure, designed to be easily scalable
* Optionally, integration with AWS services such as S3 for file upload APIs

## Note

1. We don't use `id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")` with
`allow_population_by_field_name = True` when creating model because we saw an problem here:
https://stackoverflow.com/questions/61491358/pyinstaller-and-fastapi-maximum-recursion-depth-exceeded


2. Besides, you need to config AWS credentials file to push logs to S3
`[default]`
`aws_region=ap-southeast-1`
`aws_access_key_id=xxx`
`aws_secret_access_key=xxx`


3. Moreover, my project is not apply all knowledge in README.