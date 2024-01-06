from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Restaurant, Review, Customer

if __name__ == '__main__':
    
    engine = create_engine('sqlite:///app.db')
    Session = sessionmaker(bind=engine)
    session = Session()


    
   
    import ipdb; ipdb.set_trace()

##continue (c)  to the tests below in the ipdb console 

### ALL POSSIBLE TESTS ###

                                        ### RESTAURANT MODEL ###


restaurant1 = session.query(Restaurant).filter_by(id=1).first()
reviews_result = restaurant1.get_reviews(session) # should return all reviews for restaurant1
print(f"get_reviews: {reviews_result}")

customers_result = restaurant1.get_customers(session) # should return all customers who have reviewed restaurant1
print(f"get_customers: {customers_result}")

all_customers_result = restaurant1.get_all_customers(session) # should return all customers regardless of if they have reviewed
print(f"get_all_customers: {all_customers_result}")

all_reviews_result = restaurant1.all_reviews(session) # should return all reviews for restaurant1 with a formatted version of the rating , customer name & restaurant reviewed
print(f"all_reviews: {all_reviews_result}")

restaurant2 = Restaurant()
fanciest_result = restaurant2.fanciest(session)# should return the most expensive restaurant
print (f"fanciest: {fanciest_result}")

cheapest_result = restaurant2.cheapest(session) # should return the cheapest restaurant
print(f"cheapest: {cheapest_result}")




                                        ### CUSTOMER MODEL ###


customer1 = session.query(Customer).first()
get_customer_reviews_result = customer1.get_customer_reviews(session) # should return all reviews left by customer1
print (f"get_customer_reviews_result: {get_customer_reviews_result}")

get_customers_restaurants_result = customer1.get_customer_restaurants(session) # should return all restaurants reviewed by customer1
print (f"get_customers_restaurants_result: {get_customers_restaurants_result}")

full_name_result = customer1.full_name() # should return the full name of customer1
print (f"full_name_result: {full_name_result}")

favourite_restaurant_result = customer1.favourite_restaurant(session) # should return the restaurant with the highest rating from customer1
print (f"favourite_restaurant_result: {favourite_restaurant_result}")


#add_review_result = customer1.add_review(session, restaurant1, 9) # should add a review to restaurant1 for customer1
#print(f"added_review ")
#before running this , comment out the delete_review method below 
#run this to add the review and comment out this and run again so that the added review is shown without adding a second review

#delete_review_result = customer1.delete_review(session, restaurant1) # should delete a review from restaurant1 for customer1
#print(f"deleted_review ")
#before running this , comment out the add_review method above
#run this to delete the review and comment out this and run again so that the deleted review is removed 


                                        ### REVIEW MODEL ###


review1 = session.query(Review).first()

get_customer_for_review_result = review1.get_customer_for_review(session) # should return the customer who left the review
print (f"get_customer_for_review: {get_customer_for_review_result}")

get_restaurant_for_review_result = review1.get_restaurant_for_review(session) # should return the restaurant that was reviewed
print (f"get_restaurant_for_review: {get_restaurant_for_review_result}")

full_review_result = review1.full_review(session) # should return a formatted version of the review
print (f"full_review: {full_review_result}")