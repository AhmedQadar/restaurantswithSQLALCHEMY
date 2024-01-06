from sqlalchemy import create_engine, func, and_
from sqlalchemy import ForeignKey, Table, Column, Integer, String, DateTime, MetaData
from sqlalchemy.orm import relationship, backref, sessionmaker, joinedload
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy

from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///app.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

############################################################################################

## ASSOCIATION TABLE


restaurant_customer = Table(
    'restaurant_customer',
    Base.metadata,
    Column('restaurant_id', ForeignKey('restaurants.id'), primary_key=True),
    Column('customer_id', ForeignKey('customers.id'), primary_key=True),
    extend_existing = True
)

############################################################################################

##  RESTAURANT MODEL
class Restaurant(Base):
    __tablename__ = 'restaurants'
    id = Column(Integer, primary_key=True)
    name = Column(String())
    price = Column(Integer())
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(),  onupdate=func.now())
   
    customers = relationship('Customer', secondary=restaurant_customer, back_populates='restaurants')
    reviews = relationship('Review', backref=backref('restaurant'))
     

    ### OBJECT RELATIONSHIP METHODS ### 
    def get_reviews(self, session):
        # changed the name to get_reviews to not clash with the relationship names 
        # collects the reviews for a restaurant but they are unformatted
        return session.query(Review).filter(Review.restaurant_id == self.id).all()

    def get_customers(self, session):
        # changed the name to get_customers to not clash with the relationship names
        return (
            #only collects customers who have reviewed
            session.query(Customer)
            .join(restaurant_customer)
            .join(Review, and_(Review.customer_id == Customer.id, Review.restaurant_id == self.id))
            .filter(restaurant_customer.c.restaurant_id == self.id)
            .all()
        )

    def get_all_customers(self, session):
        # some customers do not review , this collects all customers regardless of if they have reviewed
        return session.query(Customer).join(restaurant_customer).filter(restaurant_customer.c.restaurant_id == self.id).all()


    ###  AGGREGATE & RELATIONSIP METHODS ###
    def fanciest(self, session):
        # collects the most expensive restaurant 
        fanciest_restaurant = (
            session.query(Restaurant)
            .order_by(Restaurant.price.desc())
            .first()
        )

        return fanciest_restaurant
    
    #This is a control test for the fanciest() method 
    def cheapest(self, session):
        # collects the cheapest restaurant
        cheapest_restaurant = (
            session.query(Restaurant)
            .order_by(Restaurant.price.asc())
            .first()
        )

        return cheapest_restaurant

    def all_reviews(self, session):
        # collects all reviews for a restaurant with a formatted version of the rating , customer name & restaurant reviewed 
        reviews = (
            session.query(Review, Customer)
            .join(Customer)
            .filter(Review.restaurant_id == self.id)
            .all()
        )
        formatted_reviews = [
            f"Review for {self.name} by {customer.full_name()}: {review.star_rating} stars" for review, customer in reviews
        ] 

        return formatted_reviews

    def __repr__(self):
        return f"Restaurant {self.name}"


###################################################################################################################

## CUSTOMER MODEL
class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    first_name = Column(String())
    last_name = Column(String())
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(),  onupdate=func.now())

    restaurants = relationship('Restaurant', secondary=restaurant_customer, back_populates='customers')
    reviews = relationship('Review', backref=backref('customer'))

    
    ### OBJECT RELATIONSHIP METHODS ###
    def get_customer_reviews(self, session):
        # changed the name to get_customer_reviews to not clash with the relationship names
        # returns all reviews left by the customer 
        return session.query(Review).filter(Review.customer_id == self.id).all()

    def get_customer_restaurants(self, session):
        # changed the name to get_customer_restaurants to not clash with the relationship names
        # returns all restaurants reviewed by the customer
        return (
            session.query(Restaurant)
            .join(restaurant_customer)
            .filter(restaurant_customer.c.customer_id == self.id)
            .all()
        )
    

    ### AGGREGATE & RELATIONSHIP METHODS ###
    def full_name(self):
        # returns the full name of the customer
        return f"{self.first_name} {self.last_name}"

    def favourite_restaurant(self, session):
        # returns the restaurant with the highest rating from the customer 
        return (
            session.query(Restaurant)
            .join(restaurant_customer)
            .join(Review,  and_(Review.customer_id == self.id, Review.restaurant_id == Restaurant.id))
            .order_by(Review.star_rating.desc())
            .first()
        )

    def add_review(self, session, restaurant, rating):
        # adds a review to a restaurant for a customer
        new_review = Review(restaurant=restaurant, customer=self, star_rating=rating)
        session.add(new_review)
        session.commit()

    def delete_review(self, session, restaurant):
        # deletes a review from a restaurant for a customer
        reviews_to_delete = (
            session.query(Review)
            .filter(Review.customer_id == self.id, Review.restaurant_id == restaurant.id)
            .all()
        )

        for review in reviews_to_delete:
            session.delete(review)

        session.commit()

    


    def __repr__(self):
        # returns first name only , for the full_name() method to work easily 
        return f"Customer {self.first_name} "

########################################################################################################

## REVIEW MODEL
class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    star_rating = Column(Integer())
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(),  onupdate=func.now())


    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    customer_id = Column(Integer, ForeignKey('customers.id'))


    ### OBJECT RELATIONSHIP METHODS ###
    def get_customer_for_review(self, session):
        # returns the customer who made the review
        return session.query(Customer).filter(Customer.id == self.customer_id).first()
    
    def get_restaurant_for_review(self, session):
        # returns the restaurant that was reviewed
        return session.query(Restaurant).filter(Restaurant.id == self.restaurant_id).first()


    ### AGGREGATE & RELATIONSHIP METHODS ###
    def full_review(self, session):
        # returns a formatted version of the review
        return f"Review for {self.get_restaurant_for_review(session).name} by {self.get_customer_for_review(session).full_name()}: {self.star_rating} stars"

    def __repr__(self):
        return f"Review {self.star_rating}"

######################################

