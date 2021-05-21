# Hints

## Many to Many relationships in Flask

If you recall from the SQL lessons, a many to many relationship in a database is usually represented with a join table.  There are several ways to represent joins with Flask and SQLAlchemy.  Imagine you had the following models:

```python

class Foo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

class Bar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

class FooBarJoin(db.Model):
    foo_id = db.Column(db.Integer, db.ForeignKey('foo.id'), primary_key=True)
    bar_id = db.Column(db.Integer, db.ForeignKey('bar.id'), primary_key=True)

```

And you want to get all of the Bars associated with Foo at id X.  The join query syntax is as follows:

```python
    results = db.session.query(Foo, Bar, FooBarJoin).join(Foo, Foo.id==FooBarJoin.foo_id)\
            .join(Bar, Bar.id==FooBarJoin.bar_id).filter(Foo.id == X).all()
```

For the above statement, result will be an array of tuples.  Each tuple will hold a Foo instance, a Bar instance and a FooBarJoin instance (in the order they are listed in the query).  [Additional documentation on building advanced queries](https://docs.sqlalchemy.org/en/14/orm/query.html)