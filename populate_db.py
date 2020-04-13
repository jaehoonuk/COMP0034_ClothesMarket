# Author: Jaehoon Lim

from app.models import User, Item
from app import db

#Populating DB with test data
def populate_db():
    if not User.query.first():
        db.session.add_all([User(userId=123, fullName='Bart', password='123', email='bart@fox.com'),
                            User(userId=404, fullName="Ralph", password='123', email="ralph@fox.com"),
                            User(userId=456, fullName="Milhouse", password='123', email="milhouse@fox.com"),
                            User(userId=888, fullName="Lisa", password='123', email="lisa@fox.com")])

    if not Item.query.first():
        db.session.add_all([Item(itemId=1000, userId=123, manufacturer='Versace', productName='Pop Animalier Print Sweatshirt', imageUrl="https://www.versace.com/dw/image/v2/ABAO_PRD/on/demandware.static/-/Sites-ver-master-catalog/default/dw89b1ff00/original/90_A85583-A233958_A7804_10_PopAnimalierPrintSweatshirt-Sweatshirts-versace-online-store_0_1.jpg", category="Shirt", quantity=1, price=1200, estimatedPrice=1100),
                            Item(itemId=1001, userId=404, manufacturer='H&M', productName="Chino Shorts Slim Fit", imageUrl="https://lp2.hm.com/hmgoepprod?set=quality[79],source[/69/fc/69fc082a8534d301d598e8c3ba3a113d1dcb387a.jpg],origin[dam],category[],type[DESCRIPTIVESTILLLIFE],hmver[1]&call=url[file:/product/main]", category="Trousers", quantity=10, price=40, estimatedPrice=40),
                            Item(itemId=1002, userId=456, manufacturer='Adidas', productName="Aero 3S Shorts", imageUrl="https://images.sportsdirect.com/images/products/47305502_l_a7.jpg", category="Trousers", quantity=5, price=30, estimatedPrice=25),
                            Item(itemId=1003, userId=888, manufacturer='Under Armour', productName="Men's Charged Cotton Tank", imageUrl="https://images-na.ssl-images-amazon.com/images/I/81miqsCbErL._AC_UX342_.jpg", category="Shirt", quantity=1, price=300, estimatedPrice=315),
                            Item(itemId=1004, userId=888, manufacturer='Zara', productName="Short Hat", imageUrl="https://static.zara.cn/photos///2020/V/0/2/p/9065/410/800/2/w/560/9065410800_1_1_1.jpg?ts=1578657866011", category="Accessories", quantity=3, price=190, estimatedPrice=150),
                            Item(itemId=1005, userId=404, manufacturer='Zara', productName="Compact Premium T-Shirt", imageUrl="https://static.zara.net/photos///2020/V/0/2/p/9240/420/538/3/w/560/9240420538_6_1_1.jpg?ts=1583333576457", category="Shirt", quantity=10, price=300, estimatedPrice=300),
                            Item(itemId=1006, userId=123, manufacturer='Zara', productName="Linen Blazer", imageUrl="https://i.pinimg.com/originals/1e/50/89/1e5089592c4850dfb3bc5e4f79428234.jpg", category="Shirt", quantity=5, price=250, estimatedPrice=250),
                            Item(itemId=1007, userId=456, manufacturer='Nike', productName="Air Jordan 1 Retro", imageUrl="https://kickstw.com.au/wp-content/uploads/2019/08/Air-Jordan-1-Retro-High-Satin-Black-Toe-W-1.jpg", category="Shoes", quantity=2, price=700, estimatedPrice=750)])

    db.session.commit()