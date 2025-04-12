
from app import app
from extensions import db
from models import Attraction, Region, TourPlan, TourPlanDestination

def add_attractions():
    print("بدء إضافة الأماكن السياحية الجديدة...")
    
    # التحقق من المناطق الموجودة
    upper_egypt = Region.query.filter_by(name="Upper Egypt").first()
    lower_egypt = Region.query.filter_by(name="Lower Egypt").first()
    cairo = Region.query.filter_by(name="Cairo").first()
    alexandria = Region.query.filter_by(name="Alexandria").first()
    
    if not cairo:
        cairo = Region(
            name="Cairo",
            name_ar="القاهرة",
            description="Egypt's capital and largest city, home to the Pyramids of Giza and many historical landmarks.",
            description_ar="عاصمة مصر وأكبر مدنها، موطن أهرامات الجيزة والعديد من المعالم التاريخية."
        )
        db.session.add(cairo)
    
    if not alexandria:
        alexandria = Region(
            name="Alexandria",
            name_ar="الإسكندرية",
            description="Egypt's second-largest city and a major Mediterranean port with a rich history.",
            description_ar="ثاني أكبر مدينة في مصر وميناء رئيسي على البحر المتوسط ذو تاريخ عريق."
        )
        db.session.add(alexandria)
    
    if not lower_egypt:
        lower_egypt = Region(
            name="Lower Egypt",
            name_ar="مصر السفلى",
            description="The northern region of Egypt, including the Nile Delta.",
            description_ar="المنطقة الشمالية من مصر، بما في ذلك دلتا النيل."
        )
        db.session.add(lower_egypt)
    
    if not upper_egypt:
        upper_egypt = Region(
            name="Upper Egypt",
            name_ar="مصر العليا",
            description="The southern region of Egypt, home to many ancient Egyptian sites.",
            description_ar="المنطقة الجنوبية من مصر، موطن للعديد من المواقع المصرية القديمة."
        )
        db.session.add(upper_egypt)
    
    db.session.commit()
    
    # إضافة الأماكن السياحية
    attractions_data = [
        {
            "name": "Karnak Temple",
            "name_ar": "معبد الكرنك",
            "description": "The Karnak Temple Complex is a vast mix of temples, chapels, pylons, and other buildings. Construction at the complex began during the reign of Senusret I and continued into the Ptolemaic period.",
            "description_ar": "مجمع معبد الكرنك هو مزيج واسع من المعابد والكنائس والأبراج والمباني الأخرى. بدأ البناء في المجمع خلال فترة حكم سنوسرت الأول واستمر في العصر البطلمي.",
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Karnak_Temple_Egypt.jpg/800px-Karnak_Temple_Egypt.jpg",
            "region_id": upper_egypt.id,
            "featured": True,
            "latitude": 25.7188,
            "longitude": 32.6572,
            "ticket_price": "240 EGP",
            "opening_hours": "6:00 AM - 5:30 PM"
        },
        {
            "name": "Valley of the Kings",
            "name_ar": "وادي الملوك",
            "description": "The Valley of the Kings is a valley where, for a period of nearly 500 years, rock-cut tombs were excavated for the pharaohs and powerful nobles of the New Kingdom.",
            "description_ar": "وادي الملوك هو وادٍ حيث تم حفر مقابر منحوتة في الصخر لمدة تقارب 500 عام للفراعنة والنبلاء الأقوياء في المملكة الحديثة.",
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/Valley_of_the_Kings_panorama.jpg/800px-Valley_of_the_Kings_panorama.jpg",
            "region_id": upper_egypt.id,
            "featured": True,
            "latitude": 25.7402,
            "longitude": 32.6014,
            "ticket_price": "240 EGP",
            "opening_hours": "6:00 AM - 4:00 PM"
        },
        {
            "name": "Abu Simbel",
            "name_ar": "أبو سمبل",
            "description": "Abu Simbel is an archaeological site comprising two massive rock-cut temples built by Pharaoh Ramesses II in the 13th century BC.",
            "description_ar": "أبو سمبل هو موقع أثري يتكون من معبدين ضخمين منحوتين في الصخر بناهما الفرعون رمسيس الثاني في القرن الثالث عشر قبل الميلاد.",
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Abu_Simbel_Temple_Egypt.jpg/800px-Abu_Simbel_Temple_Egypt.jpg",
            "region_id": upper_egypt.id,
            "featured": True,
            "latitude": 22.3372,
            "longitude": 31.6258,
            "ticket_price": "240 EGP",
            "opening_hours": "5:00 AM - 6:00 PM"
        },
        {
            "name": "Philae Temple",
            "name_ar": "معبد فيلة",
            "description": "The Philae Temple is an ancient Egyptian temple complex on Philae island. The principal deity of the temple complex was Isis, but other temples and shrines were dedicated to her son Horus and husband Osiris.",
            "description_ar": "معبد فيلة هو مجمع معبد مصري قديم في جزيرة فيلة. كانت الإلهة الرئيسية للمجمع المعبد هي إيزيس، ولكن كانت هناك معابد ومزارات أخرى مخصصة لابنها حورس وزوجها أوزوريس.",
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2b/Philae_Temple_Egypt.jpg/800px-Philae_Temple_Egypt.jpg",
            "region_id": upper_egypt.id,
            "featured": False,
            "latitude": 24.0134,
            "longitude": 32.8878,
            "ticket_price": "180 EGP",
            "opening_hours": "7:00 AM - 4:00 PM"
        },
        {
            "name": "Bibliotheca Alexandrina",
            "name_ar": "مكتبة الإسكندرية",
            "description": "The Bibliotheca Alexandrina is a major library and cultural center located on the Mediterranean Sea in Alexandria, Egypt. It is a commemoration of the Library of Alexandria that was lost in antiquity.",
            "description_ar": "مكتبة الإسكندرية هي مكتبة رئيسية ومركز ثقافي يقع على البحر المتوسط في الإسكندرية، مصر. وهي تخليد لمكتبة الإسكندرية التي فقدت في العصور القديمة.",
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/Bibliotheca_Alexandrina_002.jpg/800px-Bibliotheca_Alexandrina_002.jpg",
            "region_id": alexandria.id,
            "featured": False,
            "latitude": 31.2089,
            "longitude": 29.9092,
            "ticket_price": "70 EGP",
            "opening_hours": "10:00 AM - 7:00 PM"
        },
        {
            "name": "Montaza Palace",
            "name_ar": "قصر المنتزه",
            "description": "Montaza Palace is a palatial complex built on a high hill overlooking the Mediterranean Sea in Alexandria. It was built in 1892 by Abbas II of Egypt.",
            "description_ar": "قصر المنتزه هو مجمع قصور بني على تل مرتفع يطل على البحر المتوسط في الإسكندرية. تم بناؤه عام 1892 من قبل عباس الثاني من مصر.",
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Montaza_Palace.jpg/800px-Montaza_Palace.jpg",
            "region_id": alexandria.id,
            "featured": False,
            "latitude": 31.2892,
            "longitude": 30.0088,
            "ticket_price": "50 EGP",
            "opening_hours": "9:00 AM - 5:00 PM"
        },
        {
            "name": "Egyptian Museum",
            "name_ar": "المتحف المصري",
            "description": "The Egyptian Museum is home to an extensive collection of ancient Egyptian antiquities. It has 120,000 items, with a representative amount on display.",
            "description_ar": "المتحف المصري هو موطن لمجموعة واسعة من الآثار المصرية القديمة. يحتوي على 120,000 قطعة، مع كمية تمثيلية معروضة.",
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Cairo_-_Egyptian_Museum_-_Central_Hall.JPG/800px-Cairo_-_Egyptian_Museum_-_Central_Hall.JPG",
            "region_id": cairo.id,
            "featured": True,
            "latitude": 30.0478,
            "longitude": 31.2336,
            "ticket_price": "200 EGP",
            "opening_hours": "9:00 AM - 5:00 PM"
        },
        {
            "name": "Khan el-Khalili",
            "name_ar": "خان الخليلي",
            "description": "Khan el-Khalili is a major souk in the historic center of Islamic Cairo. The bazaar district is one of Cairo's main attractions for tourists and Egyptians alike.",
            "description_ar": "خان الخليلي هو سوق كبير في المركز التاريخي للقاهرة الإسلامية. حي البازار هو واحد من أهم مناطق الجذب في القاهرة للسياح والمصريين على حد سواء.",
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/El_Fishawi_Cafe.jpg/800px-El_Fishawi_Cafe.jpg",
            "region_id": cairo.id,
            "featured": False,
            "latitude": 30.0471,
            "longitude": 31.2625,
            "ticket_price": "Free",
            "opening_hours": "10:00 AM - 11:00 PM"
        },
        {
            "name": "Luxor Temple",
            "name_ar": "معبد الأقصر",
            "description": "Luxor Temple is a large Ancient Egyptian temple complex located on the east bank of the Nile River in the city today known as Luxor (ancient Thebes).",
            "description_ar": "معبد الأقصر هو مجمع معبد مصري قديم كبير يقع على الضفة الشرقية لنهر النيل في المدينة المعروفة اليوم باسم الأقصر (طيبة القديمة).",
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Luxor_Temple_Egypt.jpg/800px-Luxor_Temple_Egypt.jpg",
            "region_id": upper_egypt.id,
            "featured": True,
            "latitude": 25.6985,
            "longitude": 32.6383,
            "ticket_price": "160 EGP",
            "opening_hours": "6:00 AM - 10:00 PM"
        },
        {
            "name": "Pyramid of Djoser",
            "name_ar": "هرم زوسر",
            "description": "The Pyramid of Djoser, or Step Pyramid, is an archaeological site in the Saqqara necropolis, Egypt, northwest of the city of Memphis. The 6-tier, 4-sided structure was built during the 27th century BC.",
            "description_ar": "هرم زوسر، أو الهرم المدرج، هو موقع أثري في جبانة سقارة، مصر، شمال غرب مدينة ممفيس. تم بناء الهيكل المكون من 6 طبقات و 4 جوانب خلال القرن 27 قبل الميلاد.",
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/All_Gizah_Pyramids.jpg/800px-All_Gizah_Pyramids.jpg",
            "region_id": lower_egypt.id,
            "featured": False,
            "latitude": 29.8712,
            "longitude": 31.2149,
            "ticket_price": "180 EGP",
            "opening_hours": "8:00 AM - 5:00 PM"
        }
    ]
    
    for attraction_data in attractions_data:
        # تحقق مما إذا كان المكان موجوداً بالفعل
        existing_attraction = Attraction.query.filter_by(name=attraction_data["name"]).first()
        if not existing_attraction:
            attraction = Attraction(**attraction_data)
            db.session.add(attraction)
    
    db.session.commit()
    print(f"تمت إضافة {len(attractions_data)} من الأماكن السياحية بنجاح!")


def add_tour_plans():
    print("بدء إضافة خطط الرحلات السياحية...")
    
    # إضافة خطط الرحلات
    tour_plans_data = [
        {
            "title": "Luxor & Aswan Exploration",
            "title_ar": "استكشاف الأقصر وأسوان",
            "description": "A 5-day journey through the historical wonders of Upper Egypt, exploring the ancient temples and tombs of Luxor and Aswan.",
            "description_ar": "رحلة لمدة 5 أيام عبر عجائب مصر العليا التاريخية، استكشاف المعابد والمقابر القديمة في الأقصر وأسوان.",
            "duration": 5,
            "price": 6500,
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/Aswan%2C_Elephantine_Island%2C_Nile_01.JPG/800px-Aswan%2C_Elephantine_Island%2C_Nile_01.JPG"
        },
        {
            "title": "Cairo & Pyramids Tour",
            "title_ar": "جولة القاهرة والأهرامات",
            "description": "Discover the famous Pyramids of Giza, the Great Sphinx, and the treasures of the Egyptian Museum in this 3-day tour of Cairo.",
            "description_ar": "اكتشف أهرامات الجيزة الشهيرة وأبو الهول العظيم وكنوز المتحف المصري في هذه الجولة التي تستغرق 3 أيام في القاهرة.",
            "duration": 3,
            "price": 4200,
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Kheops-Pyramid.jpg/800px-Kheops-Pyramid.jpg"
        },
        {
            "title": "Alexandria Coastal Journey",
            "title_ar": "رحلة ساحل الإسكندرية",
            "description": "Explore the Mediterranean gem of Egypt with visits to the Bibliotheca Alexandrina, Montaza Palace, and the Catacombs of Kom El Shoqafa.",
            "description_ar": "استكشف جوهرة البحر المتوسط في مصر مع زيارات إلى مكتبة الإسكندرية وقصر المنتزه ومقابر كوم الشقافة.",
            "duration": 2,
            "price": 3000,
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Citadel_of_Qaitbay_R01.jpg/800px-Citadel_of_Qaitbay_R01.jpg"
        },
        {
            "title": "Nile Cruise Adventure",
            "title_ar": "مغامرة رحلة النيل",
            "description": "Cruise down the Nile River from Luxor to Aswan, stopping at ancient temples along the way, including Edfu and Kom Ombo.",
            "description_ar": "رحلة نهرية على طول نهر النيل من الأقصر إلى أسوان، مع التوقف عند المعابد القديمة على طول الطريق، بما في ذلك إدفو وكوم أمبو.",
            "duration": 4,
            "price": 5800,
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Nile_Cruise_ships_in_Luxor.jpg/800px-Nile_Cruise_ships_in_Luxor.jpg"
        },
        {
            "title": "Red Sea Diving Experience",
            "title_ar": "تجربة الغوص في البحر الأحمر",
            "description": "Enjoy the crystal-clear waters of the Red Sea with a diving tour in Hurghada, exploring the colorful coral reefs and marine life.",
            "description_ar": "استمتع بالمياه الصافية للبحر الأحمر مع جولة غوص في الغردقة، واستكشاف الشعاب المرجانية الملونة والحياة البحرية.",
            "duration": 3,
            "price": 4500,
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/72/Hurghada_beach.jpg/800px-Hurghada_beach.jpg"
        }
    ]
    
    for plan_data in tour_plans_data:
        # تحقق مما إذا كانت الخطة موجودة بالفعل
        existing_plan = TourPlan.query.filter_by(title=plan_data["title"]).first()
        if not existing_plan:
            tour_plan = TourPlan(**plan_data)
            db.session.add(tour_plan)
    
    db.session.commit()
    print(f"تمت إضافة {len(tour_plans_data)} من خطط الرحلات بنجاح!")
    
    # إضافة وجهات للرحلات
    add_tour_destinations()


def add_tour_destinations():
    print("بدء إضافة وجهات للرحلات...")
    
    # الحصول على الرحلات
    luxor_aswan = TourPlan.query.filter_by(title="Luxor & Aswan Exploration").first()
    cairo_pyramids = TourPlan.query.filter_by(title="Cairo & Pyramids Tour").first()
    alexandria = TourPlan.query.filter_by(title="Alexandria Coastal Journey").first()
    nile_cruise = TourPlan.query.filter_by(title="Nile Cruise Adventure").first()
    
    # الحصول على الأماكن السياحية
    luxor_temple = Attraction.query.filter_by(name="Luxor Temple").first()
    karnak_temple = Attraction.query.filter_by(name="Karnak Temple").first()
    valley_kings = Attraction.query.filter_by(name="Valley of the Kings").first()
    philae_temple = Attraction.query.filter_by(name="Philae Temple").first()
    abu_simbel = Attraction.query.filter_by(name="Abu Simbel").first()
    egyptian_museum = Attraction.query.filter_by(name="Egyptian Museum").first()
    khan_khalili = Attraction.query.filter_by(name="Khan el-Khalili").first()
    bibliotheca = Attraction.query.filter_by(name="Bibliotheca Alexandrina").first()
    montaza = Attraction.query.filter_by(name="Montaza Palace").first()
    
    # إضافة الوجهات للرحلات
    if luxor_aswan:
        destinations_data = [
            {
                "tour_plan_id": luxor_aswan.id,
                "attraction_id": luxor_temple.id if luxor_temple else None,
                "day_number": 1,
                "description": "Visit the magnificent Luxor Temple and explore its ancient columns and statues.",
                "description_ar": "زيارة معبد الأقصر الرائع واستكشاف أعمدته وتماثيله القديمة."
            },
            {
                "tour_plan_id": luxor_aswan.id,
                "attraction_id": karnak_temple.id if karnak_temple else None,
                "day_number": 2,
                "description": "Explore the vast Karnak Temple Complex, one of the largest religious buildings ever constructed.",
                "description_ar": "استكشاف مجمع معبد الكرنك الضخم، أحد أكبر المباني الدينية التي تم بناؤها على الإطلاق."
            },
            {
                "tour_plan_id": luxor_aswan.id,
                "attraction_id": valley_kings.id if valley_kings else None,
                "day_number": 3,
                "description": "Discover the Valley of the Kings, the royal cemetery for Pharaohs.",
                "description_ar": "اكتشاف وادي الملوك، المقبرة الملكية للفراعنة."
            },
            {
                "tour_plan_id": luxor_aswan.id,
                "attraction_id": philae_temple.id if philae_temple else None,
                "day_number": 4,
                "description": "Visit the beautiful Philae Temple on its island setting.",
                "description_ar": "زيارة معبد فيلة الجميل في موقعه الجزيري."
            },
            {
                "tour_plan_id": luxor_aswan.id,
                "attraction_id": abu_simbel.id if abu_simbel else None,
                "day_number": 5,
                "description": "Take a day trip to the majestic Abu Simbel temples, one of Egypt's greatest archaeological treasures.",
                "description_ar": "رحلة ليوم واحد إلى معابد أبو سمبل المهيبة، أحد أعظم الكنوز الأثرية في مصر."
            }
        ]
        
        for dest_data in destinations_data:
            if dest_data["attraction_id"]:
                existing_dest = TourPlanDestination.query.filter_by(
                    tour_plan_id=dest_data["tour_plan_id"],
                    attraction_id=dest_data["attraction_id"],
                    day_number=dest_data["day_number"]
                ).first()
                
                if not existing_dest:
                    destination = TourPlanDestination(**dest_data)
                    db.session.add(destination)
    
    if cairo_pyramids:
        destinations_data = [
            {
                "tour_plan_id": cairo_pyramids.id,
                "attraction_id": egyptian_museum.id if egyptian_museum else None,
                "day_number": 1,
                "description": "Visit the Egyptian Museum to see the Tutankhamun collection and thousands of ancient artifacts.",
                "description_ar": "زيارة المتحف المصري لمشاهدة مجموعة توت عنخ آمون وآلاف القطع الأثرية القديمة."
            },
            {
                "tour_plan_id": cairo_pyramids.id,
                "attraction_id": khan_khalili.id if khan_khalili else None,
                "day_number": 2,
                "description": "Explore the historic Khan el-Khalili bazaar for traditional Egyptian souvenirs.",
                "description_ar": "استكشاف بازار خان الخليلي التاريخي للحصول على الهدايا التذكارية المصرية التقليدية."
            }
        ]
        
        for dest_data in destinations_data:
            if dest_data["attraction_id"]:
                existing_dest = TourPlanDestination.query.filter_by(
                    tour_plan_id=dest_data["tour_plan_id"],
                    attraction_id=dest_data["attraction_id"],
                    day_number=dest_data["day_number"]
                ).first()
                
                if not existing_dest:
                    destination = TourPlanDestination(**dest_data)
                    db.session.add(destination)
    
    if alexandria:
        destinations_data = [
            {
                "tour_plan_id": alexandria.id,
                "attraction_id": bibliotheca.id if bibliotheca else None,
                "day_number": 1,
                "description": "Visit the modern Bibliotheca Alexandrina, built to revive the ancient Library of Alexandria.",
                "description_ar": "زيارة مكتبة الإسكندرية الحديثة، التي بنيت لإحياء مكتبة الإسكندرية القديمة."
            },
            {
                "tour_plan_id": alexandria.id,
                "attraction_id": montaza.id if montaza else None,
                "day_number": 2,
                "description": "Explore the beautiful gardens and palace of Montaza.",
                "description_ar": "استكشاف الحدائق الجميلة وقصر المنتزه."
            }
        ]
        
        for dest_data in destinations_data:
            if dest_data["attraction_id"]:
                existing_dest = TourPlanDestination.query.filter_by(
                    tour_plan_id=dest_data["tour_plan_id"],
                    attraction_id=dest_data["attraction_id"],
                    day_number=dest_data["day_number"]
                ).first()
                
                if not existing_dest:
                    destination = TourPlanDestination(**dest_data)
                    db.session.add(destination)
    
    if nile_cruise:
        destinations_data = [
            {
                "tour_plan_id": nile_cruise.id,
                "attraction_id": luxor_temple.id if luxor_temple else None,
                "day_number": 1,
                "description": "Board the cruise ship in Luxor and visit Luxor Temple in the evening.",
                "description_ar": "الصعود إلى سفينة الرحلات البحرية في الأقصر وزيارة معبد الأقصر في المساء."
            },
            {
                "tour_plan_id": nile_cruise.id,
                "attraction_id": karnak_temple.id if karnak_temple else None,
                "day_number": 2,
                "description": "Visit the Karnak Temple Complex before sailing towards Edfu.",
                "description_ar": "زيارة مجمع معبد الكرنك قبل الإبحار نحو إدفو."
            },
            {
                "tour_plan_id": nile_cruise.id,
                "attraction_id": philae_temple.id if philae_temple else None,
                "day_number": 4,
                "description": "Arrive in Aswan and visit the beautiful Philae Temple.",
                "description_ar": "الوصول إلى أسوان وزيارة معبد فيلة الجميل."
            }
        ]
        
        for dest_data in destinations_data:
            if dest_data["attraction_id"]:
                existing_dest = TourPlanDestination.query.filter_by(
                    tour_plan_id=dest_data["tour_plan_id"],
                    attraction_id=dest_data["attraction_id"],
                    day_number=dest_data["day_number"]
                ).first()
                
                if not existing_dest:
                    destination = TourPlanDestination(**dest_data)
                    db.session.add(destination)
    
    db.session.commit()
    print("تمت إضافة وجهات الرحلات بنجاح!")

if __name__ == "__main__":
    with app.app_context():
        add_attractions()
        add_tour_plans()
        print("تمت إضافة البيانات السياحية بنجاح!")
