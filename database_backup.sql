--
-- PostgreSQL database dump
--

-- Dumped from database version 16.8
-- Dumped by pg_dump version 16.5

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: activity; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.activity (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    name_ar character varying(100),
    description text,
    description_ar text,
    image_url character varying(200),
    price character varying(100),
    duration character varying(50),
    attraction_id integer NOT NULL
);


ALTER TABLE public.activity OWNER TO neondb_owner;

--
-- Name: activity_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.activity_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.activity_id_seq OWNER TO neondb_owner;

--
-- Name: activity_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.activity_id_seq OWNED BY public.activity.id;


--
-- Name: attraction; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.attraction (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    name_ar character varying(100),
    description text NOT NULL,
    description_ar text,
    image_url character varying(200),
    address character varying(200),
    latitude double precision,
    longitude double precision,
    ticket_price character varying(100),
    opening_hours character varying(100),
    website character varying(200),
    featured boolean,
    region_id integer NOT NULL
);


ALTER TABLE public.attraction OWNER TO neondb_owner;

--
-- Name: attraction_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.attraction_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.attraction_id_seq OWNER TO neondb_owner;

--
-- Name: attraction_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.attraction_id_seq OWNED BY public.attraction.id;


--
-- Name: chat_group; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.chat_group (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    description text,
    created_at timestamp without time zone,
    guide_id integer NOT NULL,
    language character varying(50) NOT NULL
);


ALTER TABLE public.chat_group OWNER TO neondb_owner;

--
-- Name: chat_group_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.chat_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.chat_group_id_seq OWNER TO neondb_owner;

--
-- Name: chat_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.chat_group_id_seq OWNED BY public.chat_group.id;


--
-- Name: chat_group_member; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.chat_group_member (
    id integer NOT NULL,
    user_id integer NOT NULL,
    chat_group_id integer NOT NULL,
    joined_at timestamp without time zone
);


ALTER TABLE public.chat_group_member OWNER TO neondb_owner;

--
-- Name: chat_group_member_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.chat_group_member_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.chat_group_member_id_seq OWNER TO neondb_owner;

--
-- Name: chat_group_member_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.chat_group_member_id_seq OWNED BY public.chat_group_member.id;


--
-- Name: chat_message; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.chat_message (
    id integer NOT NULL,
    content text NOT NULL,
    "timestamp" timestamp without time zone,
    user_id integer NOT NULL,
    chat_group_id integer NOT NULL
);


ALTER TABLE public.chat_message OWNER TO neondb_owner;

--
-- Name: chat_message_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.chat_message_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.chat_message_id_seq OWNER TO neondb_owner;

--
-- Name: chat_message_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.chat_message_id_seq OWNED BY public.chat_message.id;


--
-- Name: guide; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.guide (
    id integer NOT NULL,
    user_id integer NOT NULL,
    years_experience integer,
    specialization character varying(200),
    certification character varying(200),
    available boolean
);


ALTER TABLE public.guide OWNER TO neondb_owner;

--
-- Name: guide_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.guide_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.guide_id_seq OWNER TO neondb_owner;

--
-- Name: guide_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.guide_id_seq OWNED BY public.guide.id;


--
-- Name: language_practice; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.language_practice (
    id integer NOT NULL,
    student_id integer NOT NULL,
    guide_id integer,
    language character varying(50) NOT NULL,
    proficiency_level character varying(50) NOT NULL,
    availability character varying(200),
    interests character varying(200)
);


ALTER TABLE public.language_practice OWNER TO neondb_owner;

--
-- Name: language_practice_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.language_practice_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.language_practice_id_seq OWNER TO neondb_owner;

--
-- Name: language_practice_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.language_practice_id_seq OWNED BY public.language_practice.id;


--
-- Name: region; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.region (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    name_ar character varying(100),
    description text,
    description_ar text
);


ALTER TABLE public.region OWNER TO neondb_owner;

--
-- Name: region_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.region_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.region_id_seq OWNER TO neondb_owner;

--
-- Name: region_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.region_id_seq OWNED BY public.region.id;


--
-- Name: restaurant; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.restaurant (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    name_ar character varying(100),
    description text,
    description_ar text,
    image_url character varying(200),
    cuisine_type character varying(100),
    price_range character varying(50),
    contact character varying(100),
    latitude double precision,
    longitude double precision,
    attraction_id integer NOT NULL
);


ALTER TABLE public.restaurant OWNER TO neondb_owner;

--
-- Name: restaurant_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.restaurant_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.restaurant_id_seq OWNER TO neondb_owner;

--
-- Name: restaurant_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.restaurant_id_seq OWNED BY public.restaurant.id;


--
-- Name: review; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.review (
    id integer NOT NULL,
    title character varying(100) NOT NULL,
    content text NOT NULL,
    rating integer NOT NULL,
    date_posted timestamp without time zone,
    user_id integer NOT NULL,
    attraction_id integer NOT NULL
);


ALTER TABLE public.review OWNER TO neondb_owner;

--
-- Name: review_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.review_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.review_id_seq OWNER TO neondb_owner;

--
-- Name: review_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.review_id_seq OWNED BY public.review.id;


--
-- Name: tour_booking; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.tour_booking (
    id integer NOT NULL,
    tourist_id integer NOT NULL,
    tour_plan_id integer NOT NULL,
    guide_id integer,
    start_date date NOT NULL,
    end_date date NOT NULL,
    status character varying(20),
    booking_date timestamp without time zone
);


ALTER TABLE public.tour_booking OWNER TO neondb_owner;

--
-- Name: tour_booking_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.tour_booking_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tour_booking_id_seq OWNER TO neondb_owner;

--
-- Name: tour_booking_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.tour_booking_id_seq OWNED BY public.tour_booking.id;


--
-- Name: tour_photo; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.tour_photo (
    id integer NOT NULL,
    progress_id integer NOT NULL,
    image_url character varying(200) NOT NULL,
    caption character varying(200),
    uploaded_at timestamp without time zone
);


ALTER TABLE public.tour_photo OWNER TO neondb_owner;

--
-- Name: tour_photo_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.tour_photo_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tour_photo_id_seq OWNER TO neondb_owner;

--
-- Name: tour_photo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.tour_photo_id_seq OWNED BY public.tour_photo.id;


--
-- Name: tour_plan; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.tour_plan (
    id integer NOT NULL,
    title character varying(200) NOT NULL,
    title_ar character varying(200),
    description text NOT NULL,
    description_ar text,
    duration integer NOT NULL,
    price double precision NOT NULL,
    created_at timestamp without time zone,
    image_url character varying(200)
);


ALTER TABLE public.tour_plan OWNER TO neondb_owner;

--
-- Name: tour_plan_destination; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.tour_plan_destination (
    id integer NOT NULL,
    tour_plan_id integer NOT NULL,
    attraction_id integer NOT NULL,
    day_number integer NOT NULL,
    description text,
    description_ar text
);


ALTER TABLE public.tour_plan_destination OWNER TO neondb_owner;

--
-- Name: tour_plan_destination_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.tour_plan_destination_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tour_plan_destination_id_seq OWNER TO neondb_owner;

--
-- Name: tour_plan_destination_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.tour_plan_destination_id_seq OWNED BY public.tour_plan_destination.id;


--
-- Name: tour_plan_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.tour_plan_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tour_plan_id_seq OWNER TO neondb_owner;

--
-- Name: tour_plan_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.tour_plan_id_seq OWNED BY public.tour_plan.id;


--
-- Name: tour_progress; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.tour_progress (
    id integer NOT NULL,
    booking_id integer NOT NULL,
    destination_id integer NOT NULL,
    completed boolean,
    completion_date timestamp without time zone,
    notes text
);


ALTER TABLE public.tour_progress OWNER TO neondb_owner;

--
-- Name: tour_progress_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.tour_progress_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tour_progress_id_seq OWNER TO neondb_owner;

--
-- Name: tour_progress_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.tour_progress_id_seq OWNED BY public.tour_progress.id;


--
-- Name: user; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public."user" (
    id integer NOT NULL,
    username character varying(64) NOT NULL,
    email character varying(120) NOT NULL,
    password_hash character varying(256) NOT NULL,
    is_guide boolean,
    is_student boolean,
    is_tourist boolean,
    is_admin boolean,
    phone character varying(20),
    country character varying(100),
    governorate character varying(100),
    city character varying(100),
    profile_pic character varying(200),
    education_level character varying(100),
    university character varying(200),
    languages character varying(200),
    bio text,
    date_joined timestamp without time zone,
    profile_completed boolean
);


ALTER TABLE public."user" OWNER TO neondb_owner;

--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_id_seq OWNER TO neondb_owner;

--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;


--
-- Name: activity id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.activity ALTER COLUMN id SET DEFAULT nextval('public.activity_id_seq'::regclass);


--
-- Name: attraction id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.attraction ALTER COLUMN id SET DEFAULT nextval('public.attraction_id_seq'::regclass);


--
-- Name: chat_group id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.chat_group ALTER COLUMN id SET DEFAULT nextval('public.chat_group_id_seq'::regclass);


--
-- Name: chat_group_member id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.chat_group_member ALTER COLUMN id SET DEFAULT nextval('public.chat_group_member_id_seq'::regclass);


--
-- Name: chat_message id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.chat_message ALTER COLUMN id SET DEFAULT nextval('public.chat_message_id_seq'::regclass);


--
-- Name: guide id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.guide ALTER COLUMN id SET DEFAULT nextval('public.guide_id_seq'::regclass);


--
-- Name: language_practice id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.language_practice ALTER COLUMN id SET DEFAULT nextval('public.language_practice_id_seq'::regclass);


--
-- Name: region id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.region ALTER COLUMN id SET DEFAULT nextval('public.region_id_seq'::regclass);


--
-- Name: restaurant id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.restaurant ALTER COLUMN id SET DEFAULT nextval('public.restaurant_id_seq'::regclass);


--
-- Name: review id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.review ALTER COLUMN id SET DEFAULT nextval('public.review_id_seq'::regclass);


--
-- Name: tour_booking id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.tour_booking ALTER COLUMN id SET DEFAULT nextval('public.tour_booking_id_seq'::regclass);


--
-- Name: tour_photo id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.tour_photo ALTER COLUMN id SET DEFAULT nextval('public.tour_photo_id_seq'::regclass);


--
-- Name: tour_plan id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.tour_plan ALTER COLUMN id SET DEFAULT nextval('public.tour_plan_id_seq'::regclass);


--
-- Name: tour_plan_destination id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.tour_plan_destination ALTER COLUMN id SET DEFAULT nextval('public.tour_plan_destination_id_seq'::regclass);


--
-- Name: tour_progress id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.tour_progress ALTER COLUMN id SET DEFAULT nextval('public.tour_progress_id_seq'::regclass);


--
-- Name: user id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);


--
-- Data for Name: activity; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.activity (id, name, name_ar, description, description_ar, image_url, price, duration, attraction_id) FROM stdin;
1	Camel Ride at the Pyramids	ركوب الجمال عند الأهرامات	Experience a traditional camel ride around the Giza Pyramids and Sphinx.	جرب ركوب الجمال التقليدي حول أهرامات الجيزة وأبو الهول.	https://media-cdn.tripadvisor.com/media/photo-s/1a/64/7e/49/cairo-day-tour-visiting.jpg	300-500 EGP	1 hour	1
2	Sound and Light Show at Karnak	عرض الصوت والضوء في الكرنك	An evening spectacle bringing ancient history to life through narration and illumination.	عرض مسائي يحيي التاريخ القديم من خلال السرد والإضاءة.	https://media-cdn.tripadvisor.com/media/photo-s/01/f7/04/65/sound-light-show-karnak.jpg	300 EGP for foreigners, 150 EGP for Egyptians	1.5 hours	2
3	Lake Nasser Cruise	رحلة بحرية في بحيرة ناصر	Sail on Lake Nasser to see Abu Simbel from a different perspective.	أبحر في بحيرة ناصر لرؤية أبو سمبل من منظور مختلف.	https://media-cdn.tripadvisor.com/media/photo-s/18/8a/bd/a5/lake-nasser-cruise.jpg	800-1500 EGP	3 hours	3
4	Bibliotheca Alexandrina Tour	جولة في مكتبة الإسكندرية	Guided tour explaining the architecture and collections of the modern library.	جولة مصحوبة بمرشد تشرح العمارة ومجموعات المكتبة الحديثة.	https://media-cdn.tripadvisor.com/media/photo-s/06/58/0c/69/bibliotheca-alexandrina.jpg	100 EGP	1 hour	4
5	Siwa Sand Bath	حمام الرمل السيوي	Experience the traditional Siwan therapy of being buried in hot desert sand.	جرب العلاج السيوي التقليدي بالدفن في رمال الصحراء الساخنة.	https://media-cdn.tripadvisor.com/media/photo-s/0d/62/44/7f/sand-baths.jpg	200-300 EGP	30 minutes	5
6	Museum Guided Tour	جولة مصحوبة بمرشد في المتحف	Expert-led tour through the highlights of the Grand Egyptian Museum collection.	جولة بقيادة خبير تستعرض أهم مقتنيات المتحف المصري الكبير.	https://media-cdn.tripadvisor.com/media/photo-s/1a/61/f6/96/egyptian-museum.jpg	250 EGP	2 hours	6
\.


--
-- Data for Name: attraction; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.attraction (id, name, name_ar, description, description_ar, image_url, address, latitude, longitude, ticket_price, opening_hours, website, featured, region_id) FROM stdin;
1	Pyramids of Giza	أهرامات الجيزة	The only remaining wonder of the ancient world, the Pyramids of Giza are one of Egypt's most iconic attractions.	العجيبة الوحيدة المتبقية من عجائب العالم القديم، أهرامات الجيزة هي واحدة من أكثر المعالم السياحية شهرة في مصر.	https://www.planetware.com/wpimages/2020/02/egypt-in-pictures-beautiful-places-to-photograph-pyramids-of-giza.jpg	Al Haram, Giza Governorate	29.9792	31.1342	240 EGP for foreigners, 60 EGP for Egyptians	8:00 AM - 5:00 PM	http://www.sca-egypt.org/	t	1
2	Karnak Temple	معبد الكرنك	A vast temple complex dedicated to the Theban triad of Amun, Mut, and Khonsu.	مجمع معبد واسع مخصص للثالوث الطيبي آمون وموت وخونسو.	https://www.planetware.com/wpimages/2020/02/egypt-in-pictures-beautiful-places-to-photograph-karnak-temple.jpg	Karnak, Luxor Governorate	25.7188	32.6571	180 EGP for foreigners, 50 EGP for Egyptians	6:00 AM - 5:30 PM	http://www.sca-egypt.org/	t	2
3	Abu Simbel Temples	معابد أبو سمبل	Two massive rock temples carved out of the mountainside by King Ramesses II.	معبدان ضخمان منحوتان في جانب الجبل من قبل الملك رمسيس الثاني.	https://www.planetware.com/wpimages/2020/02/egypt-in-pictures-beautiful-places-to-photograph-abu-simbel.jpg	Abu Simbel, Aswan Governorate	22.3372	31.6258	240 EGP for foreigners, 60 EGP for Egyptians	6:00 AM - 5:00 PM	http://www.sca-egypt.org/	t	3
4	Bibliotheca Alexandrina	مكتبة الإسكندرية	A major library and cultural center located on the shore of the Mediterranean Sea.	مكتبة رئيسية ومركز ثقافي يقع على شاطئ البحر المتوسط.	https://www.planetware.com/wpimages/2020/02/egypt-in-pictures-beautiful-places-to-photograph-bibliotheca-alexandrina.jpg	Shatby, Alexandria Governorate	31.2089	29.9092	70 EGP for foreigners, 20 EGP for Egyptians	10:00 AM - 7:00 PM, Closed on Fridays	https://www.bibalex.org/	t	4
5	Temple of the Oracle	معبد الوحي	An ancient temple dedicated to the god Amun, visited by Alexander the Great.	معبد قديم مخصص للإله آمون، زاره الإسكندر الأكبر.	https://www.planetware.com/wpimages/2020/02/egypt-in-pictures-beautiful-places-to-photograph-siwa-oasis.jpg	Siwa Oasis, Matrouh Governorate	29.2041	25.516	80 EGP for foreigners, 25 EGP for Egyptians	8:00 AM - 5:00 PM	http://www.sca-egypt.org/	f	5
6	The Grand Egyptian Museum	المتحف المصري الكبير	The largest archaeological museum in the world dedicated to ancient Egyptian civilization.	أكبر متحف أثري في العالم مخصص للحضارة المصرية القديمة.	https://www.planetware.com/wpimages/2022/04/egypt-cairo-top-attractions-egyptian-museum.jpg	Al Remaya Square, Giza Governorate	29.9945	31.1165	400 EGP for foreigners, 100 EGP for Egyptians	9:00 AM - 7:00 PM	https://gem.gov.eg/	t	1
\.


--
-- Data for Name: chat_group; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.chat_group (id, name, description, created_at, guide_id, language) FROM stdin;
1	English Practice Group	Group for practicing English conversation with focus on travel vocabulary	2025-02-28 16:54:02.942787	3	English
2	Spanish Learning Circle	A friendly group to learn Spanish basics for travel	2025-03-10 16:54:02.94296	4	Spanish
\.


--
-- Data for Name: chat_group_member; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.chat_group_member (id, user_id, chat_group_id, joined_at) FROM stdin;
1	5	1	2025-03-01 16:54:03.219372
2	6	2	2025-03-12 16:54:03.219484
\.


--
-- Data for Name: chat_message; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.chat_message (id, content, "timestamp", user_id, chat_group_id) FROM stdin;
1	Welcome to our English practice group! Let's introduce ourselves.	2025-03-01 16:54:03.294763	3	1
2	Hello everyone, I'm Ahmed. I'm excited to improve my English!	2025-03-01 15:54:03.294915	5	1
3	¡Bienvenidos al grupo de español! Vamos a aprender juntos.	2025-03-12 16:54:03.294951	4	2
4	Hola, soy Nora. ¡Estoy feliz de estar aquí!	2025-03-12 14:54:03.294974	6	2
\.


--
-- Data for Name: guide; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.guide (id, user_id, years_experience, specialization, certification, available) FROM stdin;
1	1	\N	\N	\N	t
2	3	10	الآثار الفرعونية والإسلامية	معتمد من وزارة السياحة	t
3	4	7	تاريخ مصر القديم	شهادة الإرشاد السياحي الدولية	t
\.


--
-- Data for Name: language_practice; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.language_practice (id, student_id, guide_id, language, proficiency_level, availability, interests) FROM stdin;
1	5	3	English	Intermediate	Weekends, evenings	History, archaeology, culture
2	6	4	Spanish	Beginner	Weekday afternoons	Art, literature, cuisine
\.


--
-- Data for Name: region; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.region (id, name, name_ar, description, description_ar) FROM stdin;
1	القاهرة	القاهرة	The capital of Egypt and a blend of ancient history and modern life	عاصمة مصر ومزيج من التاريخ القديم والحياة العصرية
2	الأقصر	الأقصر	Known for its ancient Egyptian temples and artifacts	معروفة بمعابدها الفرعونية القديمة وآثارها
3	أسوان	أسوان	Famous for its natural beauty and Nubian culture	مشهورة بجمالها الطبيعي وثقافتها النوبية
4	الإسكندرية	الإسكندرية	Coastal city with a rich Greco-Roman heritage	مدينة ساحلية ذات تراث يوناني روماني غني
5	سيوة	سيوة	An isolated oasis with unique traditions and landscapes	واحة معزولة بتقاليد ومناظر طبيعية فريدة
\.


--
-- Data for Name: restaurant; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.restaurant (id, name, name_ar, description, description_ar, image_url, cuisine_type, price_range, contact, latitude, longitude, attraction_id) FROM stdin;
1	Pyramids View Restaurant	مطعم إطلالة الأهرامات	Enjoy traditional Egyptian cuisine with a spectacular view of the Pyramids.	استمتع بالمأكولات المصرية التقليدية مع إطلالة رائعة على الأهرامات.	https://media-cdn.tripadvisor.com/media/photo-s/0d/53/95/ce/view-from-the-restaurant.jpg	Egyptian	$$$	+20 2 33773222	29.9773	31.1325	1
2	Luxor Nubian Restaurant	مطعم الأقصر النوبي	Authentic Nubian dishes served in a traditional setting.	أطباق نوبية أصيلة تقدم في جو تقليدي.	https://media-cdn.tripadvisor.com/media/photo-s/1a/90/53/9a/nubian-restaurant.jpg	Nubian	$$	+20 95 2373612	25.7188	32.655	2
3	Abu Simbel Rest House	استراحة أبو سمبل	Enjoy local and international cuisine after visiting the temples.	استمتع بالمأكولات المحلية والعالمية بعد زيارة المعابد.	https://media-cdn.tripadvisor.com/media/photo-s/10/f3/40/a1/abu-simbel-rest-house.jpg	International, Egyptian	$$	+20 97 3310475	22.336	31.6252	3
4	Greek Club Alexandria	النادي اليوناني بالإسكندرية	Historical restaurant offering Mediterranean cuisine with sea views.	مطعم تاريخي يقدم المأكولات المتوسطية مع إطلالة على البحر.	https://media-cdn.tripadvisor.com/media/photo-s/11/11/4d/99/the-greek-club.jpg	Mediterranean, Greek	$$$	+20 3 4865990	31.2099	29.906	4
5	Abdu Siwa Restaurant	مطعم عبده سيوة	Traditional Siwan cuisine using local ingredients and recipes.	مأكولات سيوية تقليدية باستخدام المكونات والوصفات المحلية.	https://media-cdn.tripadvisor.com/media/photo-s/0e/85/69/6e/view-from-abdu-restaurant.jpg	Siwan, Egyptian	$	+20 46 4602688	29.203	25.5167	5
6	9 Pyramids Lounge	استراحة التسع أهرامات	Modern restaurant offering Egyptian and international cuisine with panoramic views of the pyramids.	مطعم عصري يقدم المأكولات المصرية والعالمية مع إطلالات بانورامية على الأهرامات.	https://media-cdn.tripadvisor.com/media/photo-s/1b/32/1d/c7/9-pyramids-lounge.jpg	International, Egyptian	$$$$	+20 2 33773222	29.977	31.129	6
\.


--
-- Data for Name: review; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.review (id, title, content, rating, date_posted, user_id, attraction_id) FROM stdin;
1	Breathtaking Experience	Seeing the pyramids in person was a dream come true. The scale and precision of these ancient structures is mind-boggling. Our guide was knowledgeable and made the history come alive.	5	2025-03-20 16:54:02.658696	7	1
2	Amazing Ancient Wonder	Karnak Temple is enormous and filled with incredible carvings and hieroglyphs. I would recommend visiting early in the morning to avoid crowds and heat.	5	2025-03-22 16:54:02.658814	7	2
3	Worth the Journey	Abu Simbel is remote but absolutely worth the trip. The temple facades are impressive, and the story of how they were moved to avoid flooding adds to their significance.	4	2025-03-23 16:54:02.658848	8	3
4	Modern Architectural Marvel	The Bibliotheca Alexandrina is a beautiful modern building with fascinating exhibitions. The main reading room is gorgeous, and the views of the Mediterranean are spectacular.	4	2025-03-24 16:54:02.658873	8	4
5	Mystical Desert Temple	Visiting the Temple of the Oracle in Siwa was like stepping back in time. The remote location and desert landscape create a mystical atmosphere.	4	2025-03-25 16:54:02.658896	7	5
6	Incredible Collection	The Grand Egyptian Museum houses an incredible collection of artifacts. The Tutankhamun galleries alone are worth the visit. Plan to spend at least 3-4 hours here.	5	2025-03-27 16:54:02.658939	8	6
\.


--
-- Data for Name: tour_booking; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.tour_booking (id, tourist_id, tour_plan_id, guide_id, start_date, end_date, status, booking_date) FROM stdin;
1	7	1	3	2025-04-14	2025-04-17	confirmed	2025-03-25 16:54:03.792435
2	8	2	4	2025-04-19	2025-04-24	pending	2025-03-27 16:54:03.79268
3	7	2	4	2025-03-15	2025-03-20	completed	2025-02-28 16:54:03.933433
\.


--
-- Data for Name: tour_photo; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.tour_photo (id, progress_id, image_url, caption, uploaded_at) FROM stdin;
1	1	https://www.egypttoursportal.com/images/2021/06/Karnak-Temple-Egypt-Tours-Portal.jpg	Amazing view of the Great Hypostyle Hall at Karnak	2025-03-16 16:54:04.453443
2	2	https://www.egypttoursportal.com/images/2021/06/Abu-Simbel-Temples-Egypt-Tours-Portal.jpg	Sunrise at Abu Simbel Temple	2025-03-18 16:54:04.53266
\.


--
-- Data for Name: tour_plan; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.tour_plan (id, title, title_ar, description, description_ar, duration, price, created_at, image_url) FROM stdin;
1	Cairo Heritage Tour	جولة تراث القاهرة	A 3-day exploration of Cairo's most iconic historical sites and museums.	استكشاف لمدة 3 أيام لأشهر المواقع التاريخية والمتاحف في القاهرة.	3	3000	2025-01-29 16:54:03.435759	https://www.egypttoursportal.com/images/2021/06/Cairo-City-Egypt-Tours-Portal.jpg
2	Upper Egypt Adventure	مغامرة صعيد مصر	A 5-day journey through Luxor and Aswan to discover ancient Egyptian temples and monuments.	رحلة لمدة 5 أيام عبر الأقصر وأسوان لاكتشاف المعابد والآثار المصرية القديمة.	5	5500	2025-02-13 16:54:03.435924	https://www.egypttoursportal.com/images/2021/06/Aswan-City-Egypt-Tours-Portal.jpg
\.


--
-- Data for Name: tour_plan_destination; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.tour_plan_destination (id, tour_plan_id, attraction_id, day_number, description, description_ar) FROM stdin;
1	1	1	1	Start with the iconic Pyramids of Giza and the Sphinx.	ابدأ بأهرامات الجيزة الشهيرة وأبو الهول.
2	1	6	2	Explore the treasures of ancient Egypt at the Grand Egyptian Museum.	استكشف كنوز مصر القديمة في المتحف المصري الكبير.
3	2	2	1	Visit the massive Karnak Temple complex in Luxor.	زيارة مجمع معبد الكرنك الضخم في الأقصر.
4	2	3	3	Witness the magnificent Abu Simbel temples.	شاهد معابد أبو سمبل الرائعة.
\.


--
-- Data for Name: tour_progress; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.tour_progress (id, booking_id, destination_id, completed, completion_date, notes) FROM stdin;
1	3	3	t	2025-03-16 16:54:04.207679	Visited the Karnak Temple. Tourist was amazed by the hypostyle hall.
2	3	4	t	2025-03-18 16:54:04.282559	Successfully visited Abu Simbel. The sound and light show was particularly impressive.
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public."user" (id, username, email, password_hash, is_guide, is_student, is_tourist, is_admin, phone, country, governorate, city, profile_pic, education_level, university, languages, bio, date_joined, profile_completed) FROM stdin;
1	mohamed	hanizezo5@gmail.com	scrypt:32768:8:1$N2iCh1i8J6a9Eqhd$00e5cba1ecfd4075226c79adbd7ffb37e7d7a3177977a6c5a099e99adeeeebd3af2567109e1bc076bd9f23f6ca0dc6aebad6abc6fb36d62e0234ff570194cb5a	t	f	f	f	01145425207	Egypt	الشرقية	hehia	\N	master	obour	\N	\N	2025-03-30 16:15:17.545908	t
2	admin	admin@example.com	scrypt:32768:8:1$ildpUBCXuZLm5hMP$3843a76803035dfcfbdbbc6449984824f38a59b6b8d84360338ac289c83b7cab6151d56644caec2b0d4f1cb107123810fba4a268035f9efe0c3e7e46da356b82	f	f	f	t	+201234567890	مصر	\N	\N	\N	\N	\N	\N	\N	2025-03-30 16:54:00.854479	t
3	محمد_المرشد	guide1@example.com	scrypt:32768:8:1$7vNDJrI08lDwjavq$f5ce2db1931c28b5caf247cd3d00c173e7f61729078b6a66caecf50864cc9222bb1887a41db22930dd27069385fa87d885c463ffad5f811fb1593f1f0cf02364	t	f	f	f	+201123456789	مصر	القاهرة	القاهرة	https://xsgames.co/randomusers/assets/avatars/male/1.jpg	bachelor	جامعة القاهرة	العربية, الإنجليزية, الفرنسية	مرشد سياحي بخبرة 10 سنوات في المناطق الأثرية المصرية	2024-11-30 16:54:00.980063	t
4	سارة_المرشدة	guide2@example.com	scrypt:32768:8:1$ilHTWuHYTK4TQQkm$e8c68548a9fe59b97cfdaf1d93c79fce0846f69f6e405200d19c6ec284fe02a81ac53deb053f2e631c32dcf9722bafa8b701ae38f47fe7938c85ca881f07ef3e	t	f	f	f	+201187654321	مصر	الجيزة	الجيزة	https://xsgames.co/randomusers/assets/avatars/female/1.jpg	master	جامعة عين شمس	العربية, الإنجليزية, الإيطالية	متخصصة في تاريخ مصر القديمة والآثار الفرعونية	2024-12-30 16:54:01.05951	t
5	أحمد_طالب	student1@example.com	scrypt:32768:8:1$hov5Y2kSpHGq3jhl$17bf03ea045e391eea7ac12a886f87476d1352aa6bdb8bdede1c2b0eb43061026b9853de3b659b48946f714688c46a393c658bc696c6804bd8e6704e039f5b62	f	t	f	f	+201012345678	مصر	الإسكندرية	الإسكندرية	https://xsgames.co/randomusers/assets/avatars/male/2.jpg	bachelor	جامعة الإسكندرية	العربية, يتعلم الإنجليزية	طالب جامعي مهتم بتعلم اللغات والثقافات المختلفة	2025-01-29 16:54:01.140408	t
6	نورا_طالبة	student2@example.com	scrypt:32768:8:1$0GxUhyC0QHaoy3Gt$1f9d721c7955033917c41ce7e11a52d0fab792bae0d714fdacfc7b24490db9173914cd4231db17d11fe7efa41e9e8807ae920c044a2ab7572c8bcc0765fa1090	f	t	f	f	+201098765432	مصر	القاهرة	المعادي	https://xsgames.co/randomusers/assets/avatars/female/2.jpg	bachelor	الجامعة الأمريكية بالقاهرة	العربية, تتعلم الإسبانية	طالبة تبحث عن فرص لممارسة اللغات الجديدة	2025-02-13 16:54:01.224363	t
7	john_tourist	tourist1@example.com	scrypt:32768:8:1$idbJA54A3aSt66cZ$649b4c4bdb4ee49edbd56a2c6fc2a7181dd6a4946ac998c5b6f47c97cce8778a1f3776e8927a3e03f46330c4a2f10a12cda2511c2661f2cebbac82b4ebaa3483	f	f	t	f	+12025550165	الولايات المتحدة	\N	\N	https://xsgames.co/randomusers/assets/avatars/male/3.jpg	\N	\N	الإنجليزية, الألمانية	سائح من الولايات المتحدة مهتم بالآثار المصرية	2025-03-10 16:54:01.303922	t
8	elena_tourist	tourist2@example.com	scrypt:32768:8:1$yYL7OQKRNRDxHEmG$ae1fb88c96f8c5e70a639c89152c2f59a90ce05988d6e41320ed7b4f659d479a62de3dac127b328ceeba3f03d98262cb1a90530768485fb89ea56ebed370abfa	f	f	t	f	+390612345678	إيطاليا	\N	\N	https://xsgames.co/randomusers/assets/avatars/female/3.jpg	\N	\N	الإيطالية, الإنجليزية	سائحة من إيطاليا تزور مصر للمرة الأولى	2025-03-15 16:54:01.385642	t
\.


--
-- Name: activity_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.activity_id_seq', 6, true);


--
-- Name: attraction_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.attraction_id_seq', 6, true);


--
-- Name: chat_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.chat_group_id_seq', 2, true);


--
-- Name: chat_group_member_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.chat_group_member_id_seq', 2, true);


--
-- Name: chat_message_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.chat_message_id_seq', 4, true);


--
-- Name: guide_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.guide_id_seq', 3, true);


--
-- Name: language_practice_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.language_practice_id_seq', 2, true);


--
-- Name: region_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.region_id_seq', 5, true);


--
-- Name: restaurant_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.restaurant_id_seq', 6, true);


--
-- Name: review_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.review_id_seq', 6, true);


--
-- Name: tour_booking_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.tour_booking_id_seq', 3, true);


--
-- Name: tour_photo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.tour_photo_id_seq', 2, true);


--
-- Name: tour_plan_destination_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.tour_plan_destination_id_seq', 4, true);


--
-- Name: tour_plan_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.tour_plan_id_seq', 2, true);


--
-- Name: tour_progress_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.tour_progress_id_seq', 2, true);


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.user_id_seq', 8, true);


--
-- Name: activity activity_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.activity
    ADD CONSTRAINT activity_pkey PRIMARY KEY (id);


--
-- Name: attraction attraction_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.attraction
    ADD CONSTRAINT attraction_pkey PRIMARY KEY (id);


--
-- Name: chat_group_member chat_group_member_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.chat_group_member
    ADD CONSTRAINT chat_group_member_pkey PRIMARY KEY (id);


--
-- Name: chat_group_member chat_group_member_user_id_chat_group_id_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.chat_group_member
    ADD CONSTRAINT chat_group_member_user_id_chat_group_id_key UNIQUE (user_id, chat_group_id);


--
-- Name: chat_group chat_group_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.chat_group
    ADD CONSTRAINT chat_group_pkey PRIMARY KEY (id);


--
-- Name: chat_message chat_message_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.chat_message
    ADD CONSTRAINT chat_message_pkey PRIMARY KEY (id);


--
-- Name: guide guide_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.guide
    ADD CONSTRAINT guide_pkey PRIMARY KEY (id);


--
-- Name: language_practice language_practice_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.language_practice
    ADD CONSTRAINT language_practice_pkey PRIMARY KEY (id);


--
-- Name: region region_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.region
    ADD CONSTRAINT region_pkey PRIMARY KEY (id);


--
-- Name: restaurant restaurant_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.restaurant
    ADD CONSTRAINT restaurant_pkey PRIMARY KEY (id);


--
-- Name: review review_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.review
    ADD CONSTRAINT review_pkey PRIMARY KEY (id);


--
-- Name: tour_booking tour_booking_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.tour_booking
    ADD CONSTRAINT tour_booking_pkey PRIMARY KEY (id);


--
-- Name: tour_photo tour_photo_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.tour_photo
    ADD CONSTRAINT tour_photo_pkey PRIMARY KEY (id);


--
-- Name: tour_plan_destination tour_plan_destination_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.tour_plan_destination
    ADD CONSTRAINT tour_plan_destination_pkey PRIMARY KEY (id);


--
-- Name: tour_plan_destination tour_plan_destination_tour_plan_id_attraction_id_day_number_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.tour_plan_destination
    ADD CONSTRAINT tour_plan_destination_tour_plan_id_attraction_id_day_number_key UNIQUE (tour_plan_id, attraction_id, day_number);


--
-- Name: tour_plan tour_plan_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.tour_plan
    ADD CONSTRAINT tour_plan_pkey PRIMARY KEY (id);


--
-- Name: tour_progress tour_progress_booking_id_destination_id_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.tour_progress
    ADD CONSTRAINT tour_progress_booking_id_destination_id_key UNIQUE (booking_id, destination_id);


--
-- Name: tour_progress tour_progress_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.tour_progress
    ADD CONSTRAINT tour_progress_pkey PRIMARY KEY (id);


--
-- Name: user user_email_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_email_key UNIQUE (email);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: user user_username_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_username_key UNIQUE (username);


--
-- Name: activity activity_attraction_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.activity
    ADD CONSTRAINT activity_attraction_id_fkey FOREIGN KEY (attraction_id) REFERENCES public.attraction(id);


--
-- Name: attraction attraction_region_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.attraction
    ADD CONSTRAINT attraction_region_id_fkey FOREIGN KEY (region_id) REFERENCES public.region(id);


--
-- Name: chat_group chat_group_guide_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.chat_group
    ADD CONSTRAINT chat_group_guide_id_fkey FOREIGN KEY (guide_id) REFERENCES public."user"(id);


--
-- Name: chat_group_member chat_group_member_chat_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.chat_group_member
    ADD CONSTRAINT chat_group_member_chat_group_id_fkey FOREIGN KEY (chat_group_id) REFERENCES public.chat_group(id);


--
-- Name: chat_group_member chat_group_member_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.chat_group_member
    ADD CONSTRAINT chat_group_member_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: chat_message chat_message_chat_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.chat_message
    ADD CONSTRAINT chat_message_chat_group_id_fkey FOREIGN KEY (chat_group_id) REFERENCES public.chat_group(id);


--
-- Name: chat_message chat_message_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.chat_message
    ADD CONSTRAINT chat_message_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: guide guide_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.guide
    ADD CONSTRAINT guide_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: language_practice language_practice_guide_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.language_practice
    ADD CONSTRAINT language_practice_guide_id_fkey FOREIGN KEY (guide_id) REFERENCES public."user"(id);


--
-- Name: language_practice language_practice_student_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.language_practice
    ADD CONSTRAINT language_practice_student_id_fkey FOREIGN KEY (student_id) REFERENCES public."user"(id);


--
-- Name: restaurant restaurant_attraction_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.restaurant
    ADD CONSTRAINT restaurant_attraction_id_fkey FOREIGN KEY (attraction_id) REFERENCES public.attraction(id);


--
-- Name: review review_attraction_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.review
    ADD CONSTRAINT review_attraction_id_fkey FOREIGN KEY (attraction_id) REFERENCES public.attraction(id);


--
-- Name: review review_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.review
    ADD CONSTRAINT review_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: tour_booking tour_booking_guide_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.tour_booking
    ADD CONSTRAINT tour_booking_guide_id_fkey FOREIGN KEY (guide_id) REFERENCES public."user"(id);


--
-- Name: tour_booking tour_booking_tour_plan_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.tour_booking
    ADD CONSTRAINT tour_booking_tour_plan_id_fkey FOREIGN KEY (tour_plan_id) REFERENCES public.tour_plan(id);


--
-- Name: tour_booking tour_booking_tourist_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.tour_booking
    ADD CONSTRAINT tour_booking_tourist_id_fkey FOREIGN KEY (tourist_id) REFERENCES public."user"(id);


--
-- Name: tour_photo tour_photo_progress_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.tour_photo
    ADD CONSTRAINT tour_photo_progress_id_fkey FOREIGN KEY (progress_id) REFERENCES public.tour_progress(id);


--
-- Name: tour_plan_destination tour_plan_destination_attraction_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.tour_plan_destination
    ADD CONSTRAINT tour_plan_destination_attraction_id_fkey FOREIGN KEY (attraction_id) REFERENCES public.attraction(id);


--
-- Name: tour_plan_destination tour_plan_destination_tour_plan_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.tour_plan_destination
    ADD CONSTRAINT tour_plan_destination_tour_plan_id_fkey FOREIGN KEY (tour_plan_id) REFERENCES public.tour_plan(id);


--
-- Name: tour_progress tour_progress_booking_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.tour_progress
    ADD CONSTRAINT tour_progress_booking_id_fkey FOREIGN KEY (booking_id) REFERENCES public.tour_booking(id);


--
-- Name: tour_progress tour_progress_destination_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.tour_progress
    ADD CONSTRAINT tour_progress_destination_id_fkey FOREIGN KEY (destination_id) REFERENCES public.tour_plan_destination(id);


--
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: public; Owner: cloud_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE cloud_admin IN SCHEMA public GRANT ALL ON SEQUENCES TO neon_superuser WITH GRANT OPTION;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: public; Owner: cloud_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE cloud_admin IN SCHEMA public GRANT ALL ON TABLES TO neon_superuser WITH GRANT OPTION;


--
-- PostgreSQL database dump complete
--

