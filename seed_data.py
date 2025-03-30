"""
هذا السكريبت يقوم بإدراج بيانات نموذجية في قاعدة البيانات
"""
import os
import random
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
from app import app, db
from models import (User, Region, Attraction, Review, Restaurant, Activity, 
                   Guide, LanguagePractice, ChatGroup, ChatGroupMember, ChatMessage, 
                   TourPlan, TourPlanDestination, TourBooking, TourProgress, TourPhoto)

def create_sample_data():
    """إنشاء بيانات نموذجية لجميع الجداول"""
    print("بدء إدراج البيانات النموذجية...")
    
    # حذف البيانات الموجودة
    # print("حذف البيانات الموجودة...")
    # db.session.query(TourPhoto).delete()
    # db.session.query(TourProgress).delete()
    # db.session.query(TourBooking).delete()
    # db.session.query(TourPlanDestination).delete()
    # db.session.query(TourPlan).delete()
    # db.session.query(ChatMessage).delete()
    # db.session.query(ChatGroupMember).delete()
    # db.session.query(ChatGroup).delete()
    # db.session.query(LanguagePractice).delete()
    # db.session.query(Guide).delete()
    # db.session.query(Activity).delete()
    # db.session.query(Restaurant).delete()
    # db.session.query(Review).delete()
    # db.session.query(Attraction).delete()
    # db.session.query(Region).delete()
    # db.session.query(User).delete()
    # db.session.commit()
    # print("تم حذف البيانات الموجودة...")

    # إنشاء المستخدمين
    print("إنشاء المستخدمين...")
    admin = User(
        username="admin",
        email="admin@example.com",
        is_admin=True,
        phone="+201234567890",
        country="مصر",
        date_joined=datetime.utcnow(),
        profile_completed=True
    )
    admin.set_password("password")
    db.session.add(admin)
    
    guide1 = User(
        username="محمد_المرشد",
        email="guide1@example.com",
        is_guide=True,
        languages="العربية, الإنجليزية, الفرنسية",
        bio="مرشد سياحي بخبرة 10 سنوات في المناطق الأثرية المصرية",
        phone="+201123456789",
        country="مصر",
        governorate="القاهرة",
        city="القاهرة",
        education_level="bachelor",
        university="جامعة القاهرة",
        profile_pic="https://xsgames.co/randomusers/assets/avatars/male/1.jpg",
        date_joined=datetime.utcnow()-timedelta(days=120),
        profile_completed=True
    )
    guide1.set_password("password")
    db.session.add(guide1)
    
    guide2 = User(
        username="سارة_المرشدة",
        email="guide2@example.com",
        is_guide=True,
        languages="العربية, الإنجليزية, الإيطالية",
        bio="متخصصة في تاريخ مصر القديمة والآثار الفرعونية",
        phone="+201187654321",
        country="مصر",
        governorate="الجيزة",
        city="الجيزة",
        education_level="master",
        university="جامعة عين شمس",
        profile_pic="https://xsgames.co/randomusers/assets/avatars/female/1.jpg",
        date_joined=datetime.utcnow()-timedelta(days=90),
        profile_completed=True
    )
    guide2.set_password("password")
    db.session.add(guide2)
    
    student1 = User(
        username="أحمد_طالب",
        email="student1@example.com",
        is_student=True,
        languages="العربية, يتعلم الإنجليزية",
        bio="طالب جامعي مهتم بتعلم اللغات والثقافات المختلفة",
        phone="+201012345678",
        country="مصر",
        governorate="الإسكندرية",
        city="الإسكندرية",
        education_level="bachelor",
        university="جامعة الإسكندرية",
        profile_pic="https://xsgames.co/randomusers/assets/avatars/male/2.jpg",
        date_joined=datetime.utcnow()-timedelta(days=60),
        profile_completed=True
    )
    student1.set_password("password")
    db.session.add(student1)
    
    student2 = User(
        username="نورا_طالبة",
        email="student2@example.com",
        is_student=True,
        languages="العربية, تتعلم الإسبانية",
        bio="طالبة تبحث عن فرص لممارسة اللغات الجديدة",
        phone="+201098765432",
        country="مصر",
        governorate="القاهرة",
        city="المعادي",
        education_level="bachelor",
        university="الجامعة الأمريكية بالقاهرة",
        profile_pic="https://xsgames.co/randomusers/assets/avatars/female/2.jpg",
        date_joined=datetime.utcnow()-timedelta(days=45),
        profile_completed=True
    )
    student2.set_password("password")
    db.session.add(student2)
    
    tourist1 = User(
        username="john_tourist",
        email="tourist1@example.com",
        is_tourist=True,
        languages="الإنجليزية, الألمانية",
        bio="سائح من الولايات المتحدة مهتم بالآثار المصرية",
        phone="+12025550165",
        country="الولايات المتحدة",
        profile_pic="https://xsgames.co/randomusers/assets/avatars/male/3.jpg",
        date_joined=datetime.utcnow()-timedelta(days=20),
        profile_completed=True
    )
    tourist1.set_password("password")
    db.session.add(tourist1)
    
    tourist2 = User(
        username="elena_tourist",
        email="tourist2@example.com",
        is_tourist=True,
        languages="الإيطالية, الإنجليزية",
        bio="سائحة من إيطاليا تزور مصر للمرة الأولى",
        phone="+390612345678",
        country="إيطاليا",
        profile_pic="https://xsgames.co/randomusers/assets/avatars/female/3.jpg",
        date_joined=datetime.utcnow()-timedelta(days=15),
        profile_completed=True
    )
    tourist2.set_password("password")
    db.session.add(tourist2)
    
    db.session.commit()
    print("تم إنشاء المستخدمين بنجاح!")
    
    # إنشاء معلومات المرشدين
    print("إنشاء معلومات المرشدين...")
    guide1_id = User.query.filter_by(email="guide1@example.com").first().id
    guide2_id = User.query.filter_by(email="guide2@example.com").first().id
    
    guide1_profile = Guide(
        user_id=guide1_id,
        years_experience=10,
        specialization="الآثار الفرعونية والإسلامية",
        certification="معتمد من وزارة السياحة",
        available=True
    )
    db.session.add(guide1_profile)
    
    guide2_profile = Guide(
        user_id=guide2_id,
        years_experience=7,
        specialization="تاريخ مصر القديم",
        certification="شهادة الإرشاد السياحي الدولية",
        available=True
    )
    db.session.add(guide2_profile)
    
    db.session.commit()
    print("تم إنشاء معلومات المرشدين بنجاح!")
    
    # إنشاء المناطق
    print("إنشاء المناطق...")
    cairo = Region(
        name="القاهرة",
        name_ar="القاهرة",
        description="The capital of Egypt and a blend of ancient history and modern life",
        description_ar="عاصمة مصر ومزيج من التاريخ القديم والحياة العصرية"
    )
    db.session.add(cairo)
    
    luxor = Region(
        name="الأقصر",
        name_ar="الأقصر",
        description="Known for its ancient Egyptian temples and artifacts",
        description_ar="معروفة بمعابدها الفرعونية القديمة وآثارها"
    )
    db.session.add(luxor)
    
    aswan = Region(
        name="أسوان",
        name_ar="أسوان",
        description="Famous for its natural beauty and Nubian culture",
        description_ar="مشهورة بجمالها الطبيعي وثقافتها النوبية"
    )
    db.session.add(aswan)
    
    alexandria = Region(
        name="الإسكندرية",
        name_ar="الإسكندرية",
        description="Coastal city with a rich Greco-Roman heritage",
        description_ar="مدينة ساحلية ذات تراث يوناني روماني غني"
    )
    db.session.add(alexandria)
    
    siwa = Region(
        name="سيوة",
        name_ar="سيوة",
        description="An isolated oasis with unique traditions and landscapes",
        description_ar="واحة معزولة بتقاليد ومناظر طبيعية فريدة"
    )
    db.session.add(siwa)
    
    db.session.commit()
    print("تم إنشاء المناطق بنجاح!")
    
    # إنشاء المعالم السياحية
    print("إنشاء المعالم السياحية...")
    pyramids = Attraction(
        name="Pyramids of Giza",
        name_ar="أهرامات الجيزة",
        description="The only remaining wonder of the ancient world, the Pyramids of Giza are one of Egypt's most iconic attractions.",
        description_ar="العجيبة الوحيدة المتبقية من عجائب العالم القديم، أهرامات الجيزة هي واحدة من أكثر المعالم السياحية شهرة في مصر.",
        image_url="https://www.planetware.com/wpimages/2020/02/egypt-in-pictures-beautiful-places-to-photograph-pyramids-of-giza.jpg",
        address="Al Haram, Giza Governorate",
        latitude=29.9792,
        longitude=31.1342,
        ticket_price="240 EGP for foreigners, 60 EGP for Egyptians",
        opening_hours="8:00 AM - 5:00 PM",
        website="http://www.sca-egypt.org/",
        featured=True,
        region_id=1
    )
    db.session.add(pyramids)
    
    karnak = Attraction(
        name="Karnak Temple",
        name_ar="معبد الكرنك",
        description="A vast temple complex dedicated to the Theban triad of Amun, Mut, and Khonsu.",
        description_ar="مجمع معبد واسع مخصص للثالوث الطيبي آمون وموت وخونسو.",
        image_url="https://www.planetware.com/wpimages/2020/02/egypt-in-pictures-beautiful-places-to-photograph-karnak-temple.jpg",
        address="Karnak, Luxor Governorate",
        latitude=25.7188,
        longitude=32.6571,
        ticket_price="180 EGP for foreigners, 50 EGP for Egyptians",
        opening_hours="6:00 AM - 5:30 PM",
        website="http://www.sca-egypt.org/",
        featured=True,
        region_id=2
    )
    db.session.add(karnak)
    
    abu_simbel = Attraction(
        name="Abu Simbel Temples",
        name_ar="معابد أبو سمبل",
        description="Two massive rock temples carved out of the mountainside by King Ramesses II.",
        description_ar="معبدان ضخمان منحوتان في جانب الجبل من قبل الملك رمسيس الثاني.",
        image_url="https://www.planetware.com/wpimages/2020/02/egypt-in-pictures-beautiful-places-to-photograph-abu-simbel.jpg",
        address="Abu Simbel, Aswan Governorate",
        latitude=22.3372,
        longitude=31.6258,
        ticket_price="240 EGP for foreigners, 60 EGP for Egyptians",
        opening_hours="6:00 AM - 5:00 PM",
        website="http://www.sca-egypt.org/",
        featured=True,
        region_id=3
    )
    db.session.add(abu_simbel)
    
    library = Attraction(
        name="Bibliotheca Alexandrina",
        name_ar="مكتبة الإسكندرية",
        description="A major library and cultural center located on the shore of the Mediterranean Sea.",
        description_ar="مكتبة رئيسية ومركز ثقافي يقع على شاطئ البحر المتوسط.",
        image_url="https://www.planetware.com/wpimages/2020/02/egypt-in-pictures-beautiful-places-to-photograph-bibliotheca-alexandrina.jpg",
        address="Shatby, Alexandria Governorate",
        latitude=31.2089,
        longitude=29.9092,
        ticket_price="70 EGP for foreigners, 20 EGP for Egyptians",
        opening_hours="10:00 AM - 7:00 PM, Closed on Fridays",
        website="https://www.bibalex.org/",
        featured=True,
        region_id=4
    )
    db.session.add(library)
    
    siwa_oracle = Attraction(
        name="Temple of the Oracle",
        name_ar="معبد الوحي",
        description="An ancient temple dedicated to the god Amun, visited by Alexander the Great.",
        description_ar="معبد قديم مخصص للإله آمون، زاره الإسكندر الأكبر.",
        image_url="https://www.planetware.com/wpimages/2020/02/egypt-in-pictures-beautiful-places-to-photograph-siwa-oasis.jpg",
        address="Siwa Oasis, Matrouh Governorate",
        latitude=29.2041,
        longitude=25.5160,
        ticket_price="80 EGP for foreigners, 25 EGP for Egyptians",
        opening_hours="8:00 AM - 5:00 PM",
        website="http://www.sca-egypt.org/",
        featured=False,
        region_id=5
    )
    db.session.add(siwa_oracle)
    
    museum = Attraction(
        name="The Grand Egyptian Museum",
        name_ar="المتحف المصري الكبير",
        description="The largest archaeological museum in the world dedicated to ancient Egyptian civilization.",
        description_ar="أكبر متحف أثري في العالم مخصص للحضارة المصرية القديمة.",
        image_url="https://www.planetware.com/wpimages/2022/04/egypt-cairo-top-attractions-egyptian-museum.jpg",
        address="Al Remaya Square, Giza Governorate",
        latitude=29.9945,
        longitude=31.1165,
        ticket_price="400 EGP for foreigners, 100 EGP for Egyptians",
        opening_hours="9:00 AM - 7:00 PM",
        website="https://gem.gov.eg/",
        featured=True,
        region_id=1
    )
    db.session.add(museum)
    
    db.session.commit()
    print("تم إنشاء المعالم السياحية بنجاح!")
    
    # إنشاء المطاعم
    print("إنشاء المطاعم...")
    
    restaurant1 = Restaurant(
        name="Pyramids View Restaurant",
        name_ar="مطعم إطلالة الأهرامات",
        description="Enjoy traditional Egyptian cuisine with a spectacular view of the Pyramids.",
        description_ar="استمتع بالمأكولات المصرية التقليدية مع إطلالة رائعة على الأهرامات.",
        image_url="https://media-cdn.tripadvisor.com/media/photo-s/0d/53/95/ce/view-from-the-restaurant.jpg",
        cuisine_type="Egyptian",
        price_range="$$$",
        contact="+20 2 33773222",
        latitude=29.9773,
        longitude=31.1325,
        attraction_id=1
    )
    db.session.add(restaurant1)
    
    restaurant2 = Restaurant(
        name="Luxor Nubian Restaurant",
        name_ar="مطعم الأقصر النوبي",
        description="Authentic Nubian dishes served in a traditional setting.",
        description_ar="أطباق نوبية أصيلة تقدم في جو تقليدي.",
        image_url="https://media-cdn.tripadvisor.com/media/photo-s/1a/90/53/9a/nubian-restaurant.jpg",
        cuisine_type="Nubian",
        price_range="$$",
        contact="+20 95 2373612",
        latitude=25.7188,
        longitude=32.6550,
        attraction_id=2
    )
    db.session.add(restaurant2)
    
    restaurant3 = Restaurant(
        name="Abu Simbel Rest House",
        name_ar="استراحة أبو سمبل",
        description="Enjoy local and international cuisine after visiting the temples.",
        description_ar="استمتع بالمأكولات المحلية والعالمية بعد زيارة المعابد.",
        image_url="https://media-cdn.tripadvisor.com/media/photo-s/10/f3/40/a1/abu-simbel-rest-house.jpg",
        cuisine_type="International, Egyptian",
        price_range="$$",
        contact="+20 97 3310475",
        latitude=22.3360,
        longitude=31.6252,
        attraction_id=3
    )
    db.session.add(restaurant3)
    
    restaurant4 = Restaurant(
        name="Greek Club Alexandria",
        name_ar="النادي اليوناني بالإسكندرية",
        description="Historical restaurant offering Mediterranean cuisine with sea views.",
        description_ar="مطعم تاريخي يقدم المأكولات المتوسطية مع إطلالة على البحر.",
        image_url="https://media-cdn.tripadvisor.com/media/photo-s/11/11/4d/99/the-greek-club.jpg",
        cuisine_type="Mediterranean, Greek",
        price_range="$$$",
        contact="+20 3 4865990",
        latitude=31.2099,
        longitude=29.9060,
        attraction_id=4
    )
    db.session.add(restaurant4)
    
    restaurant5 = Restaurant(
        name="Abdu Siwa Restaurant",
        name_ar="مطعم عبده سيوة",
        description="Traditional Siwan cuisine using local ingredients and recipes.",
        description_ar="مأكولات سيوية تقليدية باستخدام المكونات والوصفات المحلية.",
        image_url="https://media-cdn.tripadvisor.com/media/photo-s/0e/85/69/6e/view-from-abdu-restaurant.jpg",
        cuisine_type="Siwan, Egyptian",
        price_range="$",
        contact="+20 46 4602688",
        latitude=29.2030,
        longitude=25.5167,
        attraction_id=5
    )
    db.session.add(restaurant5)
    
    restaurant6 = Restaurant(
        name="9 Pyramids Lounge",
        name_ar="استراحة التسع أهرامات",
        description="Modern restaurant offering Egyptian and international cuisine with panoramic views of the pyramids.",
        description_ar="مطعم عصري يقدم المأكولات المصرية والعالمية مع إطلالات بانورامية على الأهرامات.",
        image_url="https://media-cdn.tripadvisor.com/media/photo-s/1b/32/1d/c7/9-pyramids-lounge.jpg",
        cuisine_type="International, Egyptian",
        price_range="$$$$",
        contact="+20 2 33773222",
        latitude=29.9770,
        longitude=31.1290,
        attraction_id=6
    )
    db.session.add(restaurant6)
    
    db.session.commit()
    print("تم إنشاء المطاعم بنجاح!")
    
    # إنشاء الأنشطة
    print("إنشاء الأنشطة...")
    
    activity1 = Activity(
        name="Camel Ride at the Pyramids",
        name_ar="ركوب الجمال عند الأهرامات",
        description="Experience a traditional camel ride around the Giza Pyramids and Sphinx.",
        description_ar="جرب ركوب الجمال التقليدي حول أهرامات الجيزة وأبو الهول.",
        image_url="https://media-cdn.tripadvisor.com/media/photo-s/1a/64/7e/49/cairo-day-tour-visiting.jpg",
        price="300-500 EGP",
        duration="1 hour",
        attraction_id=1
    )
    db.session.add(activity1)
    
    activity2 = Activity(
        name="Sound and Light Show at Karnak",
        name_ar="عرض الصوت والضوء في الكرنك",
        description="An evening spectacle bringing ancient history to life through narration and illumination.",
        description_ar="عرض مسائي يحيي التاريخ القديم من خلال السرد والإضاءة.",
        image_url="https://media-cdn.tripadvisor.com/media/photo-s/01/f7/04/65/sound-light-show-karnak.jpg",
        price="300 EGP for foreigners, 150 EGP for Egyptians",
        duration="1.5 hours",
        attraction_id=2
    )
    db.session.add(activity2)
    
    activity3 = Activity(
        name="Lake Nasser Cruise",
        name_ar="رحلة بحرية في بحيرة ناصر",
        description="Sail on Lake Nasser to see Abu Simbel from a different perspective.",
        description_ar="أبحر في بحيرة ناصر لرؤية أبو سمبل من منظور مختلف.",
        image_url="https://media-cdn.tripadvisor.com/media/photo-s/18/8a/bd/a5/lake-nasser-cruise.jpg",
        price="800-1500 EGP",
        duration="3 hours",
        attraction_id=3
    )
    db.session.add(activity3)
    
    activity4 = Activity(
        name="Bibliotheca Alexandrina Tour",
        name_ar="جولة في مكتبة الإسكندرية",
        description="Guided tour explaining the architecture and collections of the modern library.",
        description_ar="جولة مصحوبة بمرشد تشرح العمارة ومجموعات المكتبة الحديثة.",
        image_url="https://media-cdn.tripadvisor.com/media/photo-s/06/58/0c/69/bibliotheca-alexandrina.jpg",
        price="100 EGP",
        duration="1 hour",
        attraction_id=4
    )
    db.session.add(activity4)
    
    activity5 = Activity(
        name="Siwa Sand Bath",
        name_ar="حمام الرمل السيوي",
        description="Experience the traditional Siwan therapy of being buried in hot desert sand.",
        description_ar="جرب العلاج السيوي التقليدي بالدفن في رمال الصحراء الساخنة.",
        image_url="https://media-cdn.tripadvisor.com/media/photo-s/0d/62/44/7f/sand-baths.jpg",
        price="200-300 EGP",
        duration="30 minutes",
        attraction_id=5
    )
    db.session.add(activity5)
    
    activity6 = Activity(
        name="Museum Guided Tour",
        name_ar="جولة مصحوبة بمرشد في المتحف",
        description="Expert-led tour through the highlights of the Grand Egyptian Museum collection.",
        description_ar="جولة بقيادة خبير تستعرض أهم مقتنيات المتحف المصري الكبير.",
        image_url="https://media-cdn.tripadvisor.com/media/photo-s/1a/61/f6/96/egyptian-museum.jpg",
        price="250 EGP",
        duration="2 hours",
        attraction_id=6
    )
    db.session.add(activity6)
    
    db.session.commit()
    print("تم إنشاء الأنشطة بنجاح!")
    
    # إنشاء التقييمات
    print("إنشاء التقييمات...")
    
    tourist1_id = User.query.filter_by(email="tourist1@example.com").first().id
    tourist2_id = User.query.filter_by(email="tourist2@example.com").first().id
    
    review1 = Review(
        title="Breathtaking Experience",
        content="Seeing the pyramids in person was a dream come true. The scale and precision of these ancient structures is mind-boggling. Our guide was knowledgeable and made the history come alive.",
        rating=5,
        date_posted=datetime.utcnow() - timedelta(days=10),
        user_id=tourist1_id,
        attraction_id=1
    )
    db.session.add(review1)
    
    review2 = Review(
        title="Amazing Ancient Wonder",
        content="Karnak Temple is enormous and filled with incredible carvings and hieroglyphs. I would recommend visiting early in the morning to avoid crowds and heat.",
        rating=5,
        date_posted=datetime.utcnow() - timedelta(days=8),
        user_id=tourist1_id,
        attraction_id=2
    )
    db.session.add(review2)
    
    review3 = Review(
        title="Worth the Journey",
        content="Abu Simbel is remote but absolutely worth the trip. The temple facades are impressive, and the story of how they were moved to avoid flooding adds to their significance.",
        rating=4,
        date_posted=datetime.utcnow() - timedelta(days=7),
        user_id=tourist2_id,
        attraction_id=3
    )
    db.session.add(review3)
    
    review4 = Review(
        title="Modern Architectural Marvel",
        content="The Bibliotheca Alexandrina is a beautiful modern building with fascinating exhibitions. The main reading room is gorgeous, and the views of the Mediterranean are spectacular.",
        rating=4,
        date_posted=datetime.utcnow() - timedelta(days=6),
        user_id=tourist2_id,
        attraction_id=4
    )
    db.session.add(review4)
    
    review5 = Review(
        title="Mystical Desert Temple",
        content="Visiting the Temple of the Oracle in Siwa was like stepping back in time. The remote location and desert landscape create a mystical atmosphere.",
        rating=4,
        date_posted=datetime.utcnow() - timedelta(days=5),
        user_id=tourist1_id,
        attraction_id=5
    )
    db.session.add(review5)
    
    review6 = Review(
        title="Incredible Collection",
        content="The Grand Egyptian Museum houses an incredible collection of artifacts. The Tutankhamun galleries alone are worth the visit. Plan to spend at least 3-4 hours here.",
        rating=5,
        date_posted=datetime.utcnow() - timedelta(days=3),
        user_id=tourist2_id,
        attraction_id=6
    )
    db.session.add(review6)
    
    db.session.commit()
    print("تم إنشاء التقييمات بنجاح!")
    
    # إنشاء ممارسات اللغة
    print("إنشاء ممارسات اللغة...")
    
    student1_id = User.query.filter_by(email="student1@example.com").first().id
    student2_id = User.query.filter_by(email="student2@example.com").first().id
    
    lang_practice1 = LanguagePractice(
        student_id=student1_id,
        guide_id=guide1_id,
        language="English",
        proficiency_level="Intermediate",
        availability="Weekends, evenings",
        interests="History, archaeology, culture"
    )
    db.session.add(lang_practice1)
    
    lang_practice2 = LanguagePractice(
        student_id=student2_id,
        guide_id=guide2_id,
        language="Spanish",
        proficiency_level="Beginner",
        availability="Weekday afternoons",
        interests="Art, literature, cuisine"
    )
    db.session.add(lang_practice2)
    
    db.session.commit()
    print("تم إنشاء ممارسات اللغة بنجاح!")
    
    # إنشاء مجموعات الدردشة
    print("إنشاء مجموعات الدردشة...")
    
    chat_group1 = ChatGroup(
        name="English Practice Group",
        description="Group for practicing English conversation with focus on travel vocabulary",
        created_at=datetime.utcnow() - timedelta(days=30),
        guide_id=guide1_id,
        language="English"
    )
    db.session.add(chat_group1)
    
    chat_group2 = ChatGroup(
        name="Spanish Learning Circle",
        description="A friendly group to learn Spanish basics for travel",
        created_at=datetime.utcnow() - timedelta(days=20),
        guide_id=guide2_id,
        language="Spanish"
    )
    db.session.add(chat_group2)
    
    db.session.commit()
    
    # إضافة أعضاء للمجموعات
    chat1_id = ChatGroup.query.filter_by(name="English Practice Group").first().id
    chat2_id = ChatGroup.query.filter_by(name="Spanish Learning Circle").first().id
    
    member1 = ChatGroupMember(
        user_id=student1_id,
        chat_group_id=chat1_id,
        joined_at=datetime.utcnow() - timedelta(days=29)
    )
    db.session.add(member1)
    
    member2 = ChatGroupMember(
        user_id=student2_id,
        chat_group_id=chat2_id,
        joined_at=datetime.utcnow() - timedelta(days=18)
    )
    db.session.add(member2)
    
    db.session.commit()
    
    # إنشاء رسائل الدردشة
    message1 = ChatMessage(
        content="Welcome to our English practice group! Let's introduce ourselves.",
        timestamp=datetime.utcnow() - timedelta(days=29),
        user_id=guide1_id,
        chat_group_id=chat1_id
    )
    db.session.add(message1)
    
    message2 = ChatMessage(
        content="Hello everyone, I'm Ahmed. I'm excited to improve my English!",
        timestamp=datetime.utcnow() - timedelta(days=29, hours=1),
        user_id=student1_id,
        chat_group_id=chat1_id
    )
    db.session.add(message2)
    
    message3 = ChatMessage(
        content="¡Bienvenidos al grupo de español! Vamos a aprender juntos.",
        timestamp=datetime.utcnow() - timedelta(days=18),
        user_id=guide2_id,
        chat_group_id=chat2_id
    )
    db.session.add(message3)
    
    message4 = ChatMessage(
        content="Hola, soy Nora. ¡Estoy feliz de estar aquí!",
        timestamp=datetime.utcnow() - timedelta(days=18, hours=2),
        user_id=student2_id,
        chat_group_id=chat2_id
    )
    db.session.add(message4)
    
    db.session.commit()
    print("تم إنشاء مجموعات الدردشة والرسائل بنجاح!")
    
    # إنشاء خطط الجولات
    print("إنشاء خطط الجولات...")
    
    tour_plan1 = TourPlan(
        title="Cairo Heritage Tour",
        title_ar="جولة تراث القاهرة",
        description="A 3-day exploration of Cairo's most iconic historical sites and museums.",
        description_ar="استكشاف لمدة 3 أيام لأشهر المواقع التاريخية والمتاحف في القاهرة.",
        duration=3,
        price=3000,
        created_at=datetime.utcnow() - timedelta(days=60),
        image_url="https://www.egypttoursportal.com/images/2021/06/Cairo-City-Egypt-Tours-Portal.jpg"
    )
    db.session.add(tour_plan1)
    
    tour_plan2 = TourPlan(
        title="Upper Egypt Adventure",
        title_ar="مغامرة صعيد مصر",
        description="A 5-day journey through Luxor and Aswan to discover ancient Egyptian temples and monuments.",
        description_ar="رحلة لمدة 5 أيام عبر الأقصر وأسوان لاكتشاف المعابد والآثار المصرية القديمة.",
        duration=5,
        price=5500,
        created_at=datetime.utcnow() - timedelta(days=45),
        image_url="https://www.egypttoursportal.com/images/2021/06/Aswan-City-Egypt-Tours-Portal.jpg"
    )
    db.session.add(tour_plan2)
    
    db.session.commit()
    
    # إضافة وجهات للجولات
    tour1_id = TourPlan.query.filter_by(title="Cairo Heritage Tour").first().id
    tour2_id = TourPlan.query.filter_by(title="Upper Egypt Adventure").first().id
    
    # جولة القاهرة
    tour1_dest1 = TourPlanDestination(
        tour_plan_id=tour1_id,
        attraction_id=1,  # الأهرامات
        day_number=1,
        description="Start with the iconic Pyramids of Giza and the Sphinx.",
        description_ar="ابدأ بأهرامات الجيزة الشهيرة وأبو الهول."
    )
    db.session.add(tour1_dest1)
    
    tour1_dest2 = TourPlanDestination(
        tour_plan_id=tour1_id,
        attraction_id=6,  # المتحف
        day_number=2,
        description="Explore the treasures of ancient Egypt at the Grand Egyptian Museum.",
        description_ar="استكشف كنوز مصر القديمة في المتحف المصري الكبير."
    )
    db.session.add(tour1_dest2)
    
    # جولة صعيد مصر
    tour2_dest1 = TourPlanDestination(
        tour_plan_id=tour2_id,
        attraction_id=2,  # معبد الكرنك
        day_number=1,
        description="Visit the massive Karnak Temple complex in Luxor.",
        description_ar="زيارة مجمع معبد الكرنك الضخم في الأقصر."
    )
    db.session.add(tour2_dest1)
    
    tour2_dest2 = TourPlanDestination(
        tour_plan_id=tour2_id,
        attraction_id=3,  # أبو سمبل
        day_number=3,
        description="Witness the magnificent Abu Simbel temples.",
        description_ar="شاهد معابد أبو سمبل الرائعة."
    )
    db.session.add(tour2_dest2)
    
    db.session.commit()
    print("تم إنشاء خطط الجولات بنجاح!")
    
    # إنشاء حجوزات الجولات
    print("إنشاء حجوزات الجولات...")
    
    booking1 = TourBooking(
        tourist_id=tourist1_id,
        tour_plan_id=tour1_id,
        guide_id=guide1_id,
        start_date=datetime.utcnow() + timedelta(days=15),
        end_date=datetime.utcnow() + timedelta(days=18),
        status="confirmed",
        booking_date=datetime.utcnow() - timedelta(days=5)
    )
    db.session.add(booking1)
    
    booking2 = TourBooking(
        tourist_id=tourist2_id,
        tour_plan_id=tour2_id,
        guide_id=guide2_id,
        start_date=datetime.utcnow() + timedelta(days=20),
        end_date=datetime.utcnow() + timedelta(days=25),
        status="pending",
        booking_date=datetime.utcnow() - timedelta(days=3)
    )
    db.session.add(booking2)
    
    db.session.commit()
    print("تم إنشاء حجوزات الجولات بنجاح!")
    
    # إنشاء تقدم الجولات والصور
    print("إنشاء تقدم الجولات...")
    
    # نفترض أن هناك جولة قديمة مكتملة للسائح الأول
    completed_booking = TourBooking(
        tourist_id=tourist1_id,
        tour_plan_id=tour2_id,
        guide_id=guide2_id,
        start_date=datetime.utcnow() - timedelta(days=15),
        end_date=datetime.utcnow() - timedelta(days=10),
        status="completed",
        booking_date=datetime.utcnow() - timedelta(days=30)
    )
    db.session.add(completed_booking)
    db.session.commit()
    
    # إضافة تقدم للجولة المكتملة
    progress1 = TourProgress(
        booking_id=completed_booking.id,
        destination_id=tour2_dest1.id,
        completed=True,
        completion_date=datetime.utcnow() - timedelta(days=14),
        notes="Visited the Karnak Temple. Tourist was amazed by the hypostyle hall."
    )
    db.session.add(progress1)
    
    progress2 = TourProgress(
        booking_id=completed_booking.id,
        destination_id=tour2_dest2.id,
        completed=True,
        completion_date=datetime.utcnow() - timedelta(days=12),
        notes="Successfully visited Abu Simbel. The sound and light show was particularly impressive."
    )
    db.session.add(progress2)
    
    db.session.commit()
    
    # إضافة صور للتقدم
    photo1 = TourPhoto(
        progress_id=progress1.id,
        image_url="https://www.egypttoursportal.com/images/2021/06/Karnak-Temple-Egypt-Tours-Portal.jpg",
        caption="Amazing view of the Great Hypostyle Hall at Karnak",
        uploaded_at=datetime.utcnow() - timedelta(days=14)
    )
    db.session.add(photo1)
    
    photo2 = TourPhoto(
        progress_id=progress2.id,
        image_url="https://www.egypttoursportal.com/images/2021/06/Abu-Simbel-Temples-Egypt-Tours-Portal.jpg",
        caption="Sunrise at Abu Simbel Temple",
        uploaded_at=datetime.utcnow() - timedelta(days=12)
    )
    db.session.add(photo2)
    
    db.session.commit()
    print("تم إنشاء تقدم الجولات والصور بنجاح!")
    
    print("تم إدراج جميع البيانات النموذجية بنجاح!")

if __name__ == "__main__":
    with app.app_context():
        create_sample_data()