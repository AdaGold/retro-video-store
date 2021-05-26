# Customers, all CRUD actions
# Videos, all CRUD actions
# Video rental checkout, custom endpoint
# Video rental check in, custom endpoint
# Listing videos checked out to a customer, custom endpoint
# Listing customers who have checked out a video, custom endpoint

children = db.relationship("Child", backref="parent", lazy=True)  # only on the parent class
parent = db.relationship("Parent", backref="children", lazy=True)  # only on the child class

children = db.relationship("Child", back_populates="parent")  # on the parent class
parent = db.relationship("Parent", back_populates="children")  # on the child class