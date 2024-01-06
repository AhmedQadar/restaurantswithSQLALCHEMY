# restaurantswithSQLALCHEMY

## ASSOCIATION TABLE 
  1-  restaurant_customer = Table('restaurant_customer', Base.metadata, ...):
    
  2-  This line defines a new table called restaurant_customer using the Table class from SQLAlchemy.
      The table is associated with the Base.metadata object, which represents the overall metadata for the database.
      The table will have columns defined in the subsequent lines.
      Column('restaurant_id', ForeignKey('restaurants.id'), primary_key=True),:
    
  3-  This line defines a column named restaurant_id in the restaurant_customer table.
      The column is of type ForeignKey and references the id column in the restaurants table.
      The primary_key=True parameter indicates that this column is part of the primary key of the restaurant_customer table.
      Column('customer_id', ForeignKey('customers.id'), primary_key=True),:
    
  4-  This line defines a column named customer_id in the restaurant_customer table.
      The column is of type ForeignKey and references the id column in the customers table.
      The primary_key=True parameter indicates that this column is part of the primary key of the restaurant_customer table.
      extend_existing=True:
    
  5-  This line sets the extend_existing parameter of the Table class to True.
      It allows the table to extend an existing table if it already exists in the database schema.
      This is useful when working with migrations or making changes to an existing database schema.

## RESTAURANT MODEL
   1- class Restaurant(Base)::
      This line defines a new class called Restaurant that inherits from the Base class.
      The Base class is typically a SQLAlchemy base class that provides the basic functionality for interacting with the database.
    
   2- __tablename__ = 'restaurants':
      This line sets the name of the database table associated with the Restaurant model to 'restaurants'.
      It specifies the table name that will be used when creating the table in the database.
    
   3- id = Column(Integer, primary_key=True):
      This line defines a column named id in the restaurants table.
      The column is of type Integer and serves as the primary key for the table.
    
   4- name = Column(String()):
      This line defines a column named name in the restaurants table.
      The column is of type String and stores the name of the restaurant.
  
   5- price = Column(Integer()):
      This line defines a column named price in the restaurants table.
      The column is of type Integer and stores the price of the restaurant.
    
   6- created_at = Column(DateTime(), server_default=func.now()):
      This line defines a column named created_at in the restaurants table.
      The column is of type DateTime and stores the timestamp of when the restaurant was created.
      The server_default=func.now() parameter sets the default value of the column to the current timestamp when a new row is inserted.
    
   7- updated_at = Column(DateTime(), onupdate=func.now()):
      This line defines a column named updated_at in the restaurants table.
      The column is of type DateTime and stores the timestamp of when the restaurant was last updated.
      The onupdate=func.now() parameter automatically updates the column with the current timestamp whenever the row is updated.
    
   8- customers = relationship('Customer', secondary=restaurant_customer, back_populates='restaurants'):
      This line defines a relationship between the Restaurant model and the Customer model.
      It specifies that the Restaurant model has a many-to-many relationship with the Customer model.
      The relationship is defined through the restaurant_customer table, which acts as an intermediary table between the two models.
      The back_populates='restaurants' parameter specifies that the Restaurant model has a back-reference to the restaurants attribute in the Customer model.
    
   9- reviews = relationship('Review', backref=backref('restaurant')):
      This line defines a relationship between the Restaurant model and the Review model.
      It specifies that the Restaurant model has a one-to-many relationship with the Review model.
      The relationship is defined through the restaurant attribute in the Review model.
      The backref='restaurant' parameter creates a back-reference from the Review model to the Restaurant model.

  10- The __repr__ method returns a string representation of the Restaurant object, which is used when printing or displaying the object.

  11- get_reviews(self, session):
      This method retrieves all the reviews for a specific restaurant.
      It takes a session object as a parameter, which is the SQLAlchemy session used for database operations.
      The method executes a query to filter the reviews based on the restaurant_id column matching the id of the current Restaurant instance.
      It returns a list of Review objects.
  
  12- get_customers(self, session):
      This method retrieves the customers who have reviewed the restaurant.
      It takes a session object as a parameter.
      The method executes a query to join the Customer and Review tables with the restaurant_customer table.
      Only the customers who have reviewed the restaurant are returned.
      It returns a list of Customer objects.
  
  13- get_all_customers(self, session):
      This method retrieves all the customers associated with the restaurant, regardless of whether they have reviewed it or not.
      It takes a session object as a parameter.
      The method executes a query to join the Customer table with the restaurant_customer table.
      It returns a list of Customer objects.
  
  14- fanciest(self, session):
      This method retrieves the restaurant with the highest price (fanciest) from the database.
      It takes a session object as a parameter.
      The method executes a query to order the Restaurant objects by price in descending order and retrieves the first result.
      It returns the fanciest Restaurant object.
  
  15- cheapest(self, session):
      This method retrieves the restaurant with the lowest price (cheapest) from the database.
      It takes a session object as a parameter.
      The method executes a query to order the Restaurant objects by price in ascending order and retrieves the first result.
      It returns the cheapest Restaurant object.
  
  16- all_reviews(self, session):
      This method retrieves all the reviews for the restaurant, along with formatted information about the rating, customer name, and restaurant name.
      It takes a session object as a parameter.
      The method executes a query to join the Review and Customer tables, filtering based on the restaurant_id column matching the id of the current Restaurant instance.
      It retrieves all the reviews and associated customers in a list of tuples.
      The method then formats the review information using a list comprehension.
      It returns a list of formatted review strings.

## CUSTOMER MODEL
  1- class Customer(Base):
     This line defines a new class called Customer that inherits from the Base class. It represents a customer entity in the database.
  
  
  2- __tablename__ = 'customers'
     This line sets the name of the database table associated with the Customer model to 'customers'. It specifies the table name that will be used when creating the table in the database.
  
  
  3- id = Column(Integer, primary_key=True)
     This line defines a column named id in the customers table. The column is of type Integer and serves as the primary key for the table.
  
  
  4- first_name = Column(String())
     last_name = Column(String())
     These lines define columns named first_name and last_name in the customers table. The columns are of type String and store the first name and last name of the customer, respectively.
  
  
  5- created_at = Column(DateTime(), server_default=func.now())
     This line defines a column named created_at in the customers table. The column is of type DateTime and stores the timestamp of when the customer was created. The server_default=func.now() parameter sets the default value of the 
     column 
     to the current timestamp when a new row is inserted.
  
  6- updated_at = Column(DateTime(), onupdate=func.now())
     This line defines a column named updated_at in the customers table. The column is of type DateTime and stores the timestamp of when the customer was last updated. The onupdate=func.now() parameter automatically updates the column 
     with 
     the current timestamp whenever the row is updated.
  
  
  7- restaurants = relationship('Restaurant', secondary=restaurant_customer, back_populates='customers')
     reviews = relationship('Review', backref=backref('restaurant'))
     These lines define relationships between the Customer model and the Restaurant and Review models. The restaurants attribute represents a many-to-many relationship with the Restaurant model through the restaurant_customer table. The 
     reviews attribute represents a one-to-many relationship with the Review model.
  
  8- def get_customer_reviews(self, session):
     This method takes a session parameter and returns all the reviews associated with the customer. It performs a query on the Review table, filtering the results based on the customer_id of the current Customer object 
  
  9- def get_customer_restaurants(self, session):
     This method takes a session parameter and returns all the restaurants associated with the customer. It performs a query on the Restaurant table, joining it with the restaurant_customer table and filtering the results based on the 
     customer_id of the current Customer object.
  
  
  10- def full_name(self):
      This method returns the full name of the customer by concatenating the first_name and last_name attributes of the current Customer object.
  
  
  
  11- def favourite_restaurant(self, session):
      This method takes a session parameter and returns the customer's favorite restaurant. It performs a query on the Restaurant table, joining it with the restaurant_customer and Review tables. It filters the results based on the 
      customer_id and restaurant_id, orders the results by the star_rating in descending order, and returns the first result.
  
  
  
  12- def add_review(self, session, restaurant, rating):
      This method takes a session, restaurant, and rating parameter. It creates a new Review object using the provided restaurant, current Customer, and rating values. It adds the new review to the session and commits the changes to the 
      database.
  
  
  13- def delete_review(self, session, restaurant):
      This method takes a session and restaurant parameter. It deletes a review from the database based on the customer_id and restaurant_id of the current Customer object and the provided restaurant object. It then commits the changes 
      to 
      the database.
  
  
  14- def __repr__(self):
      This special method provides a string representation of the Customer object. It returns a formatted string that includes the first_name attribute of the current Customer object.


## REVIEW MODEL 
  1- class Review(Base):
     This line defines a new class called Review that inherits from the Base class. It represents a review entity in the database.
  
  
  2- __tablename__ = 'reviews'
     This line sets the name of the database table associated with the Review model to 'reviews'. It specifies the table name that will be used when creating the table in the database.
  
  
  3- id = Column(Integer, primary_key=True)
     star_rating = Column(Integer())
     created_at = Column(DateTime(), server_default=func.now())
     updated_at = Column(DateTime(),  onupdate=func.now())
     These lines define columns in the reviews table. The id column is of type Integer and serves as the primary key. The star_rating column is of type Integer and stores the rating for the review. The created_at and updated_at columns 
     are 
     of type DateTime and store the timestamps for when the review was created and last updated, respectively.
  
  
  4- restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
     customer_id = Column(Integer, ForeignKey('customers.id'))
     These lines define foreign key columns in the reviews table. The restaurant_id column references the primary key of the restaurants table, and the customer_id column references the primary key of the customers table. These foreign 
     key 
     columns establish the relationship between the Review model and the Restaurant and Customer models.
  
  
  5- def get_customer_for_review(self, session):
     This method takes a session parameter and returns the customer who made the review. It performs a query on the Customer table, filtering the results based on the customer_id of the current Review object.
  
  
  6- def get_restaurant_for_review(self, session):
     This method takes a session parameter and returns the restaurant that was reviewed. It performs a query on the Restaurant table, filtering the results based on the restaurant_id of the current Review object.
  
  
  7- def full_review(self, session):
     This method takes a session parameter and returns a formatted version of the review. It calls the get_restaurant_for_review and get_customer_for_review methods to retrieve the associated restaurant and customer, respectively. It 
     then 
     constructs and returns a formatted string containing the restaurant name, customer full name, and star rating.
  
  
  8- def __repr__(self):
     This special method provides a string representation of the Review object. It returns a formatted string that includes the star_rating attribute of the current Review object.
