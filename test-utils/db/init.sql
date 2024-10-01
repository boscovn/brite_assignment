--
-- PostgreSQL database dump
--

-- Dumped from database version 12.20 (Debian 12.20-1.pgdg120+1)
-- Dumped by pg_dump version 12.20 (Debian 12.20-1.pgdg120+1)

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
-- Name: movies; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.movies (
    id integer NOT NULL,
    title character varying(100) NOT NULL,
    year integer NOT NULL,
    imdb_id character varying(20) NOT NULL,
    runtime character varying(20),
    genre character varying(100),
    director character varying(100)
);


ALTER TABLE public.movies OWNER TO postgres;

--
-- Name: movies_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.movies_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.movies_id_seq OWNER TO postgres;

--
-- Name: movies_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.movies_id_seq OWNED BY public.movies.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(80) NOT NULL,
    password_hash character varying(80) NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: movies id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movies ALTER COLUMN id SET DEFAULT nextval('public.movies_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: movies; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.movies (id, title, year, imdb_id, runtime, genre, director) FROM stdin;
1	They Live	1988	tt0096256	94 min	Action, Horror, Sci-Fi	John Carpenter
2	When They See Us	2019	tt7137906	296 min	Biography, Crime, Drama	Ava DuVernay
3	The Harder They Fall	2021	tt10696784	139 min	Action, Drama, Western	Jeymes Samuel
4	See How They Run	2022	tt13640696	98 min	Comedy, Crime, Mystery	Tom George
5	They Cloned Tyrone	2023	tt9873892	122 min	Comedy, Mystery, Sci-Fi	Juel Taylor
6	They Shall Not Grow Old	2018	tt7905466	99 min	Documentary, History, War	Peter Jackson
7	They Call Me Trinity	1970	tt0067355	115 min	Comedy, Western	Enzo Barboni
8	They Came Together	2014	tt2398249	83 min	Comedy, Romance	David Wain
9	In China They Eat Dogs	1999	tt0180748	91 min	Action, Comedy, Crime	Lasse Spang Olsen
10	They Shoot Horses, Don't They?	1969	tt0065088	129 min	Drama	Sydney Pollack
11	First They Killed My Father	2017	tt4882376	136 min	Biography, Drama, History	Angelina Jolie
12	They Call Me Jeeg Robot	2015	tt3775086	112 min	Action, Comedy, Drama	Gabriele Mainetti
13	They	2002	tt0283632	89 min	Horror, Mystery, Thriller	Robert Harmon
14	Sometimes They Come Back	1991	tt0102960	97 min	Drama, Horror, Thriller	Tom McLoughlin
15	They/Them	2022	tt14502344	104 min	Drama, Horror, Mystery	John Logan
16	They Live by Night	1948	tt0040872	95 min	Crime, Film-Noir, Romance	Nicholas Ray
17	They Were Expendable	1945	tt0038160	135 min	Drama, War	John Ford, Robert Montgomery
18	The Harder They Fall	1956	tt0049291	109 min	Drama, Film-Noir, Sport	Mark Robson
19	They Drive by Night	1940	tt0033149	95 min	Crime, Drama, Film-Noir	Raoul Walsh
20	They Look Like People	2015	tt4105970	80 min	Drama, Horror, Mystery	Perry Blackshear
21	I Hope They Serve Beer in Hell	2009	tt1220628	105 min	Comedy	Bob Gosse
22	Why Didn't They Ask Evans?	2022	tt14829590	31S min	Mystery, Thriller	N/A
23	The Harder They Come	1972	tt0070155	120 min	Crime, Drama, Music	Perry Henzell
24	They Died with Their Boots On	1941	tt0034277	140 min	War, Western	Raoul Walsh
25	When They Cry	2006	tt0845738	24 min	Animation, Drama, Horror	N/A
26	What They Had	2018	tt6662736	101 min	Drama	Elizabeth Chomko
27	They Call Me Mister Tibbs!	1970	tt0066450	108 min	Crime, Drama, Mystery	Gordon Douglas
28	They Wait	2007	tt0869152	99 min	Horror, Mystery, Thriller	Ernie Barbarash
29	They Might Be Giants	1971	tt0067848	91 min	Comedy, Mystery, Romance	Anthony Harvey
30	They Fought for Their Country	1975	tt0073488	158 min	Drama, War	Sergey Bondarchuk
31	Sometimes They Come Back... Again	1996	tt0117692	98 min	Horror	Adam Grossman
32	They Call Me Renegade	1987	tt0095975	92 min	Action, Adventure, Comedy	Enzo Barboni
33	They All Laughed	1981	tt0083189	115 min	Comedy, Romance	Peter Bogdanovich
34	They Won't Believe Me	1947	tt0039896	95 min	Drama, Film-Noir, Romance	Irving Pichel
35	They Came Back	2004	tt0378661	102 min	Drama, Fantasy	Robin Campillo
36	When They Cry: Kai	2007	tt1068433	25 min	Animation, Drama, Horror	N/A
37	They Made Me a Criminal	1939	tt0032022	92 min	Crime, Drama, Film-Noir	Busby Berkeley
38	Feminists: What Were They Thinking?	2018	tt5419676	86 min	Documentary	Johanna Demetrakas
39	They Came to Cordura	1959	tt0053351	123 min	Adventure, Drama, History	Robert Rossen
40	Oprah Winfrey Presents: When They See Us Now	2019	tt10484298	61 min	Documentary	Mark Ritchie
41	What Have They Done to Your Daughters?	1974	tt0072007	96 min	Action, Crime, Horror	Massimo Dallamano
42	They Called Him Mostly Harmless	2024	tt31049718	89 min	Documentary, Crime, Mystery	Patricia E. Gillespie
43	They Nest	2000	tt0221633	92 min	Sci-Fi, Horror	Ellory Elkayem
44	Big Girls Don't Cry... They Get Even	1991	tt0101444	96 min	Comedy	Joan Micklin Silver
45	They Came from Beyond Space	1967	tt0062360	85 min	Adventure, Sci-Fi	Freddie Francis
46	Sometimes They Come Back... for More	1998	tt0171768	89 min	Horror, Mystery, Thriller	Daniel Zelik Berk
47	The Night They Knocked	2019	tt7588822	80 min	Drama, Horror, Thriller	Sean Roberts
48	The Man They Could Not Hang	1939	tt0031614	64 min	Crime, Horror, Sci-Fi	Nick Grinde
49	They Won't Forget	1937	tt0029658	95 min	Drama, Film-Noir, Mystery	Mervyn LeRoy
50	Miss Marple: They Do It with Mirrors	1991	tt0103078	100 min	Crime, Drama, Mystery	Norman Stone
51	They Call Me Bruce	1982	tt0084786	87 min	Action, Comedy	Elliott Hong
52	The Night They Raided Minsky's	1968	tt0063348	99 min	Comedy	William Friedkin
53	They Don't Wear Black Tie	1981	tt0082317	120 min	Drama	Leon Hirszman
54	Ladies They Talk About	1933	tt0024238	69 min	Drama	Howard Bretherton, William Keighley
55	As They Made Us	2022	tt10949028	100 min	Drama	Mayim Bialik
56	They Found Hell	2015	tt5113926	87 min	Adventure, Fantasy, Horror	Nick Lyon
57	The Night They Saved Christmas	1984	tt0087797	92 min	Drama, Family, Fantasy	Jackie Cooper
58	How Do They Do It?	2006	tt0862583	51 min	Documentary	N/A
59	They Call Us Misfits	1968	tt0062900	100 min	Documentary	Stefan Jarl, Jan Lindqvist
60	They Call Me Magic	2022	tt17736322	N/A	Documentary, Biography, Sport	N/A
61	They Remain	2018	tt4991112	102 min	Thriller	Philip Gelatt
62	Until They Sail	1957	tt0051141	94 min	Drama, Romance, War	Robert Wise
63	Ron White: They Call Me Tater Salad	2004	tt0431370	56 min	Documentary, Comedy	Michael Drumm
64	They Were Five	1936	tt0027342	100 min	Drama	Julien Duvivier
65	Men Do What They Can	2012	tt2036408	108 min	Comedy	Marc Rothemund
66	They Met in Bombay	1941	tt0034281	92 min	Adventure, Comedy, Crime	Clarence Brown
67	They Caught the Ferry	1948	tt0040275	11 min	Short, Drama, Horror	Carl Theodor Dreyer
68	See How They Fall	1994	tt0110958	90 min	Crime, Drama	Jacques Audiard
69	They Live Inside Us	2020	tt8327630	103 min	Horror	Michael Ballif
70	Keemat: They Are Back	1998	tt0286752	162 min	Action, Comedy, Drama	Sameer Malkan
71	They Think It's All Over	1995	tt0112193	N/A	Comedy, Game-Show, Sport	N/A
72	They Only Kill Their Masters	1972	tt0069371	97 min	Mystery, Romance, Thriller	James Goldstone
73	They Go Boom!	1929	tt0020489	21 min	Comedy, Short	James Parrott
74	They Reach	2020	tt6483422	87 min	Adventure, Horror	Sylas Dall
75	How They Get There	1997	tt0351080	3 min	Short, Comedy	Spike Jonze
76	They Live in the Grey	2022	tt10631148	123 min	Horror, Thriller	Abel Vang, Burlee Vang
77	The Avengers: United They Stand	1999	tt0203247	30 min	Animation, Action, Adventure	N/A
78	Problem Children Are Coming from Another World, Aren't They?	2013	tt2575690	N/A	Animation, Action, Comedy	N/A
79	They Have Escaped	2014	tt2967988	102 min	Drama, Mystery	J.-P. Valkeapää
80	Why Didn't They Ask Evans?	1980	tt0081752	180 min	Crime, Mystery, Romance	John Davies, Tony Wharmby
81	They Saved Hitler's Brain	1968	tt0265870	91 min	Action, Adventure, Sci-Fi	David Bradley
82	Michael Jackson: They Don't Care About Us	1996	tt6664122	5 min	Short, Music	Spike Lee
83	The Day They Robbed the Bank of England	1960	tt0053752	85 min	Crime, Drama, Thriller	John Guillermin
84	There They Go-Go-Go!	1956	tt0049842	7 min	Animation, Family, Short	Chuck Jones
85	Higurashi: When They Cry - GOU	2020	tt12367868	N/A	Animation, Drama, Horror	N/A
86	They Crawl	2001	tt0299712	93 min	Horror, Sci-Fi, Thriller	John Allardice
87	They Who Dare	1954	tt0046421	107 min	Drama, History, War	Lewis Milestone
88	When They Cry: Rei	2009	tt6061174	30 min	Animation, Comedy, Horror	N/A
89	It Started with a Kiss: They Kiss Again	2007	tt1856983	90 min	Comedy, Drama, Romance	N/A
90	They All Kissed the Bride	1942	tt0035428	85 min	Comedy, Romance	Alexander Hall
91	They Are All Dead	2014	tt2515214	93 min	Comedy, Drama, Family	Beatriz Sanchís
92	They Call It Sin	1932	tt0023581	69 min	Drama	Thornton Freeland
93	They Wait in the Dark	2022	tt14107778	85 min	Drama, Horror, Thriller	Patrick Rea
94	They Got Me Covered	1943	tt0036427	95 min	Comedy	David Butler
95	And They Say I Am the Crazy One	2019	tt10520386	86 min	Comedy, Drama	Julia Rezende
96	They Came to Rob Las Vegas	1968	tt0063684	124 min	Crime, Drama	Antonio Isasi-Isasmendi
97	They Rode West	1954	tt0047575	84 min	Drama, Western	Phil Karlson
98	They Shot the Piano Player	2023	tt11242654	104 min	Animation, Drama, History	Javier Mariscal, Fernando Trueba
99	Murder, They Hope	2021	tt14609542	N/A	Comedy, Mystery	N/A
100	They Call Us Monsters	2016	tt5730882	82 min	Documentary	Ben Lear
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, username, password_hash) FROM stdin;
1	admin	$2b$12$r4LwquLq7/EsZEugpTnw9.sYipgENJKfUKaNADFwjSIfdWykKztM6
\.


--
-- Name: movies_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.movies_id_seq', 100, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 1, true);


--
-- Name: movies movies_imdb_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movies
    ADD CONSTRAINT movies_imdb_id_key UNIQUE (imdb_id);


--
-- Name: movies movies_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movies
    ADD CONSTRAINT movies_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- PostgreSQL database dump complete
--

