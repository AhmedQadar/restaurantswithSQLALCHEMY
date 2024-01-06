from faker import Faker
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Customer, Restaurant, Review

if __name__ == '__main__':
    engine = create_engine('sqlite:///app.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(Restaurant).delete()
    session.query(Customer).delete()
    session.query(Review).delete()

    fake = Faker()

    restaurants =  []
    for _ in range(50):
        restaurant = Restaurant(
            name=fake.unique.name(),
            price=random.randint(100, 5000)
        )

        session.add(restaurant)
        session.commit()

        restaurants.append(restaurant)

    customers = []
    for _ in range(100):
        customer = Customer(
            first_name=fake.first_name(),
            last_name=fake.last_name()
        )

        session.add(customer)
        session.commit()

        customers.append(customer)


    reviews = []
    for restaurant in restaurants:
        for i in range(random.randint(1, 5)):
            customer = random.choice(customers)
            if restaurant not in customer.restaurants:
                customer.restaurants.append(restaurant)
                session.add(customer)
                session.commit()

            review = Review(
                star_rating=random.randint(0, 10),
                restaurant_id=restaurant.id,
                customer_id=customer.id 
            )

            reviews.append(review)

    session.bulk_save_objects(reviews)
    session.commit()
    session.close()

    