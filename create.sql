DROP TABLE IF EXISTS public.orders;
DROP TABLE IF EXISTS public.users;
DROP TABLE IF EXISTS public.products;


CREATE TABLE IF NOT EXISTS public.products
(
    id serial PRIMARY KEY,
    name character varying(255) NOT NULL,
    cat character varying(255) NOT NULL,
    description character varying,
    price bigint NOT NULL,
    photo character varying
);


CREATE TABLE IF NOT EXISTS public.users
(
    id serial PRIMARY KEY,
    tgid bigint NOT NULL,
    username character varying(255),
    cart text DEFAULT ''
);


CREATE TABLE IF NOT EXISTS public.orders
(
    id serial PRIMARY KEY,
    userid int NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    cart text NOT NULL,
    address text NOT NULL,
	price bigint not null
);


INSERT INTO public.products (name, cat, description, price, photo)
VALUES 
('Стиральная машина LG AI DD', 'Крупная техника', 'Стиральная машина с интеллектуальным определением типа ткани', 52000, 'c:\Users\Public\Pictures\lg_washer.jpg'),
('Холодильник Haier No Frost', 'Крупная техника', 'Двухкамерный холодильник с системой сухой заморозки', 68000, 'c:\Users\Public\Pictures\haier_fridge.png'),
('Робот-пылесос Roborock S8', 'Техника для уборки', 'Робот с функцией влажной уборки и мощным всасыванием', 55000, 'c:\Users\Public\Pictures\roborock_s8.jpg'),
('Микроволновая печь Samsung', 'Кухонная техника', 'Сенсорное управление и биокерамическое покрытие', 9500, 'c:\Users\Public\Pictures\samsung_mw.jpg'),
('Гриль контактный Tefal Optigrill+', 'Кухонная техника', 'Автоматическое определение степени прожарки стейка', 18000, 'c:\Users\Public\Pictures\tefal_grill.png'),
('Вертикальный отпариватель Philips', 'Уход за одеждой', 'Мощная подача пара для любых видов тканей', 14500, 'c:\Users\Public\Pictures\philips_steamer.jpg'),
('Фен Dyson Supersonic', 'Красота и здоровье', 'Профессиональный фен с цифровым управлением двигателем', 48000, 'c:\Users\Public\Pictures\dyson_hair.jpg'),
('Очиститель воздуха Blueair', 'Климатическая техника', 'Многоступенчатая фильтрация от аллергенов и пыли', 29000, 'c:\Users\Public\Pictures\blueair_cleaner.png'),
('Блендер погружной Braun MultiQuick', 'Кухонная техника', 'Набор с измельчителем и венчиком в комплекте', 7200, 'c:\Users\Public\Pictures\braun_blender.jpg'),
('Электрогриль DeLonghi MultiGrill', 'Кухонная техника', 'Съемные панели и точная настройка температуры', 24000, 'c:\Users\Public\Pictures\delonghi_grill.jpg');

