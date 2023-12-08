import json
import pyrebase


class DBhandler:
    def __init__(self):
        with open('./authentication/firebase_auth.json') as f:
            config = json.load(f)

        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()

    # User

    def insert_user(self, data, password):
        phone = data.get('phone', None)

        user_info = {
            "id": data['id'],
            "password": password,
            "email": data['email'],
            "phone": phone  # "phone" 키가 없으면 None으로 설정
        }

        self.db.child("user").push(user_info)
        print(data)

    def user_duplicate_check(self, id_string):
        users = self.db.child("user").get()
        print("users###", users.val())

        for res in users.each():
            value = res.val()

            if value['id'] == id_string: #중복 아이디 있으면 false
                return False

        return True #중복 아이디 없으면 true

    def find_user(self, id_, pw_):
        users = self.db.child("user").get() 
        target_value=[]
        for res in users.each():
            value = res.val()
            
            if value['id'] == id_ and value['password'] == pw_:
                return True 
            
        return False

    
    def get_user_info(self, id_):
        users = self.db.child("user").get()
        for res in users.each():
            value = res.val()
            if value['id'] == id_:
                user_info = {
                    "id": value['id'],
                    "email": value['email'],
                    "phone": value['phone']
                }
                print(user_info)
                return user_info
        
        return False

    # Item
    
    def insert_item(self, name, data):
        item_info ={
            "sellerId": data['seller-id'],
            "productName": data['product-name'],
            "productPrice": data['product-price'],
            "product-status": data['product-status'],
            "description": data['product-description'],
            "product-image": data['img_path']
        }
        self.db.child("item").child(name).set(item_info)
        print(data)
        return True
       
    def get_all_items(self):
        items = self.db.child("item").get()
        result = []

        if items.val():
            for item in items.each():
                result.append(item.val())

        return result
    
    def get_item_byname(self, name): 
        items = self.db.child("item").get() 
        target_value="" 
        print("###########",name)
        for res in items.each(): 
            key_value = res.key()
            if key_value == name: 
                target_value=res.val()
        return target_value
    
    def get_heart_byname(self, uid, name):
        hearts = self.db.child("heart").child(uid).get()
        target_value=""
        if hearts.val() == None:
            return target_value

        for res in hearts.each():
            key_value = res.key()

        if key_value == name:
            target_value=res.val()
        return target_value
    
    def update_heart(self, user_id, isHeart, item):
        heart_info ={
             "interested": isHeart
        }
        self.db.child("heart").child(user_id).child(item).set(heart_info)
        return True

    
    # Review
    
    def reg_review(self, data):
        review_info = {
            "productName": data['productName'],
            "title": data['title'],
            "point": data['point'],
            "content": data['content'],
            "img_path": data['img_path'],
            "authorId": data['authorId']
        }
        self.db.child("review").child(data['productName']).set(review_info)
        return True
      
    def get_all_reviews(self ):
        reviews = self.db.child("review").get().val()
        return reviews
    
    def get_review_byname(self, name): 
        reviews = self.db.child("review").get() 
        target_value="" 
        print("###########",name)
        for res in reviews.each():
            key_value = res.key()
            if key_value == name: 
                target_value=res.val()
                break

        return target_value
    
    def get_users_registered_item(self, seller):
        items = self.db.child("item").get()
        result = []
        length = 0
        print("###########", seller)
        for item in items.each(): 
            sellerId = item.sellerId
            if sellerId == seller: 
                result.append(item.val())
                length += 1
            if length >= 3:
                break
        return result
    
    # def get_users_registered_item(self, seller):
    #     print("###########", seller)
    #     result = self.db.child("item").order_by_child("sellerId").equal_to(seller).get()
    #     return result
    
    
    # 회원탈퇴
    def withdraw_user(self, id_):
        user = self.db.child("user").order_by_child("id").equal_to(id_).get()
        print("user:", user)
        user.remove()
        return True
    # heart
    def get_top_2_hearts_byname(self, uid):
        hearts = self.db.child("heart").child(uid).get()
        target_values = []

        if hearts.val() is None:
            return target_values
        # Create a list of tuples containing key-value pairs
        heart_list = [(res.key(), res.val()) for res in hearts.each()]
        # Sort the list based on the values in descending order
        sorted_hearts = sorted(heart_list, key=lambda x: x[1], reverse=True)
        # Extract the top 2 values
        top_2_hearts = sorted_hearts[:2]
        # Check if the requested name is in the top 2 hearts
        for key, value in top_2_hearts:
            target_values.append(value)
        return target_values
