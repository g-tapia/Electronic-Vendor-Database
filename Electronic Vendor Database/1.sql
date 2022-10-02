create table member(
    m_id varchar(50) primary key,
    name varchar(20) not null,
    phone varchar(20) not null, 
    email varchar(50) UNIQUE,
    type int check(type in (1,2)), -- 1 = normal member, 2 = contract member
    user_status int default 1, -- we still want data even though user delete one's account. 1 = user, 2 = deleted user
    reg_date DATE NOT NULL, -- date that user create account
    billing_date DATE -- NULL if type == 1,
);

create table memberAddress(
    id BIGINT not null auto_increment primary key,
    m_id varchar(50),
    address1 varchar(50) not null,
    address2 varchar(50),
    state varchar(2) not null,
    zipcode varchar(15) not null,
    foreign key (m_id) references member(m_id),
    UNIQUE(m_id, address1)
);

create table memberCardInfo(
	id BIGINT not null auto_increment primary key, 
    m_id varchar(50),
    card_num varchar(20) not null UNIQUE,
    card_name varchar(30) not null,
    card_exp_month int constraint card01 check(card_exp_month between 1 and 12),
    card_exp_year int constraint card02 check(card_exp_year between 0 and 99),
    foreign key (m_id) references member(m_id),
    balance double not null,
    UNIQUE(m_id, card_num)
);

CREATE TABLE manufacturer(
	manufacturer_id varchar(20) primary key,
	manufacturer_name varchar(100),
	email varchar (30) not null,
	phone_num varchar(20) not null
);

CREATE TABLE category(
	category varchar(100) primary key
);

CREATE TABLE product (
    p_id varchar(10) primary key,
    category varchar(30) not null,
    p_name varchar(50) not null,
    wholesale_price double not null,
    instore_price double not null,
    manufacturer_id varchar(20),
    FOREIGN Key (manufacturer_id) REFERENCES manufacturer(manufacturer_id),
	FOREIGN Key (category) REFERENCES category(category)
);

create table warehouse(
	w_id varchar(10) primary key,
	address1 varchar(20) not null,
	state VARCHAR(2) not null,
	zipcode varchar(15) not null
);

create table store(
    s_id varchar(10) primary KEY,
    address VARCHAR(20) not null,
    state varchar(2) not null,
    zipcode varchar(15) not null
);


CREATE TABLE warehouseReorder(
	w_id varchar(10), 
	manufacturer_id varchar(10),
	p_id varchar(10),
	quantity int default 0, 
	reorderDate date not NULL,
	FOREIGN key (w_id) references warehouse(w_id),
	foreign key (manufacturer_id) references manufacturer(manufacturer_id),
	foreign key (p_id) references product(p_id),
	primary key (w_id, p_id, reorderDate)
);

Create Table storeReorder(
	s_id varchar(10),
	w_id varchar(10),
	p_id varchar(10),
	quantity int default 0,
	reorderDate date not null,
	foreign key (s_id) references store(s_id),
	foreign key (w_id) references warehouse(w_id),
	foreign key (p_id) references product(p_id),
	primary key (s_id, p_id, reorderDate)
);


create table storeINV(
	id BIGINT not null auto_increment primary key,
	s_id varchar(10),
	p_id varchar(10),
	quantity int default 0,
	threshold int default 0,
	FOREIGN key (s_id) references store(s_id),
	FOREIGN KEY (p_id) references product(p_id),
	UNIQUE (s_id, p_id)
);


create table warehouseINV(
	id BIGINT not null auto_increment primary key,
	w_id varchar(10),
	p_id varchar(10),
	quantity int default 0,
	threshold int default 0,
	foreign key (w_id) references warehouse(w_id),
	foreign key (p_id) references product(p_id),
	UNIQUE (w_id, p_id)
);


create table whCoverage( 
    w_id varchar(10),
    state varchar(10),
    FOREIGN key (w_id) references warehouse(w_id),
    primary key(w_id, state)
);

create table whStore(
    w_id varchar(10),
    s_id varchar(10),
    primary key(w_id, s_id),
    foreign key (w_id) references warehouse(w_id),
    foreign key (s_id) references store(s_id)
);

CREATE TABLE orderList(
	order_id BIGINT not null auto_increment,
	order_date date not null,
	primary key(order_id)
);


create table ShippingCompany(
	sc_id varchar(20) primary key,
	sc_name varchar(50)
);

create table onlineOrder(
	id BIGINT not null auto_increment primary key,
	order_id BIGINT not null,
	foreign key (order_id) references orderList(order_id),
	
	order_date date not null,	
	
	p_id varchar(10),
	FOREIGN KEY (p_id) REFERENCES product(p_id),
	
	quantity int not null,

	customer_type int CHECK(customer_type in (0, 1, 2)), 
	
	m_id varchar(50),

	FOREIGN key (m_id) references member(m_id),
	
	email varchar(30),
	card_info varchar(20) not null,
	
	address1 varchar(50) not null,
	address2 varchar(50),
	state varchar(2) not null,
	zip_code varchar(15) not null,
	
	phone_num BIGINT not null,
	
	recipient_name varchar(30) not null,
	recipient_phone BIGINT not null,
	sc_id varchar(20),
	FOREIGN key (sc_id) references ShippingCompany(sc_id),
	tracking_num varchar(50) not null
);

create table instoreOrder(
	order_id BIGINT not null,
	foreign key (order_id) references orderList(order_id),

	s_id varchar(10), 
	FOREIGN key (s_id) REFERENCES store(s_id),
	
	p_id varchar(10), 
	FOREIGN key (p_id) references product(p_id),
	
	quantity int not null,

	customer_type int CHECK(customer_type in (0,1,2)),
	m_id varchar(50),
	FOREIGN key(m_id) references member (m_id)
);

create table cart(
	id BIGINT not null auto_increment primary key,
	m_id varchar(50) not null,
	foreign key (m_id) references member(m_id),
	
	p_id varchar(10) not null,
	foreign key (p_id) references product(p_id),

	quantity int not null,
	UNIQUE(m_id, p_id)
);

create table storeAdmin(
	store_a_id varchar(50) primary key,
    s_id varchar(10),
    name varchar(20) not null,
    phone varchar(20) not null, 
    email varchar(50) UNIQUE,
    FOREIGN KEY (s_id) references store(s_id)
);

create table restockStore(
	s_id varchar(10),
	w_id varchar(10),
	p_id varchar(10),
	quantity BIGINT Check (quantity > 0),
	restock_date date not null,
	FOREIGN KEY (s_id) references store(s_id),
	FOREIGN key (w_id) references warehouse(w_id),
	Foreign key (p_id) references product(p_id)
);

create table restockWarehouse(
	w_id varchar(10),
	manufacturer_id varchar(10),
	p_id VARCHAR(10),
	quantity BIGINT Check (quantity > 0),
	restock_date date not null,
	FOREIGN KEY (w_id) references warehouse(w_id),
	FOREIGN key (manufacturer_id) references manufacturer(manufacturer_id),
	FOREIGN key (p_id) references product(p_id)
);

create table warehouseAdmin(
	wh_a_id varchar(50) primary key,
    w_id varchar(10),
    name varchar(20) not null,
    phone varchar(20) not null, 
    email varchar(50) UNIQUE,
    FOREIGN KEY (w_id) references warehouse(w_id)
);




delimiter //
Create Trigger warehouseInit
	after insert on product for each row
	Begin
		declare seq_id INT;
			set seq_id = (select count(*) from product);
		insert into warehouseINV values(seq_id, "w_1", new.p_id, 20, 50);
	end;
delimiter;




-- warehouse, stores, warehouse to store connection, manufacturers, categories, products, store products, admins ...

-- warehouse
INSERT INTO `db`.`warehouse`(`w_id`,`address1`,`state`,`zipcode`) VALUES ('w_1','Mars colony st. 201', 'XY', '100100');

-- stores
INSERT INTO `db`.`store`(`s_id`,`address`,`state`,`zipcode`) VALUES ('s_1','Jupiter OA', 'R2','229');
INSERT INTO `db`.`store`(`s_id`,`address`,`state`,`zipcode`) VALUES ('s_2','Jupiter IA', 'R1','103');
INSERT INTO `db`.`store`(`s_id`,`address`,`state`,`zipcode`) VALUES ('s_3','Jupiter Moon 17', 'G1','3');

-- wharehouse <-> store
INSERT INTO `db`.`whStore`(`w_id`, `s_id`) VALUES ('w_1','s_1');
INSERT INTO `db`.`whStore`(`w_id`, `s_id`) VALUES ('w_1','s_2');
INSERT INTO `db`.`whStore`(`w_id`, `s_id`) VALUES ('w_1','s_3');

-- manufacturers
INSERT INTO `db`.`manufacturer`(`manufacturer_id`,`manufacturer_name`,`email`,`phone_num`) VALUES ('man_01','Samsung','samsung@gmail.com','123456789');
INSERT INTO `db`.`manufacturer`(`manufacturer_id`,`manufacturer_name`,`email`,`phone_num`) VALUES ('man_02','Apple','apple@gmail.com','923428789');
INSERT INTO `db`.`manufacturer`(`manufacturer_id`,`manufacturer_name`,`email`,`phone_num`) VALUES ('man_03','Dell','dell@gmail.com','234567389');
INSERT INTO `db`.`manufacturer`(`manufacturer_id`,`manufacturer_name`,`email`,`phone_num`) VALUES ('man_04','Lenovo','lenovo@gmail.com','393456789');
INSERT INTO `db`.`manufacturer`(`manufacturer_id`,`manufacturer_name`,`email`,`phone_num`) VALUES ('man_05','Logitech','logitech@gmail.com','113456789');
INSERT INTO `db`.`manufacturer`(`manufacturer_id`,`manufacturer_name`,`email`,`phone_num`) VALUES ('man_06','Razer','razer@gmail.com','723456789');
INSERT INTO `db`.`manufacturer`(`manufacturer_id`,`manufacturer_name`,`email`,`phone_num`) VALUES ('man_07','Google','google@gmail.com','703456789');
INSERT INTO `db`.`manufacturer`(`manufacturer_id`,`manufacturer_name`,`email`,`phone_num`) VALUES ('man_08','Sony','sony@gmail.com','273456789');
INSERT INTO `db`.`manufacturer`(`manufacturer_id`,`manufacturer_name`,`email`,`phone_num`) VALUES ('man_09','Canon','canon@gmail.com','993456789');

-- categories
INSERT INTO `db`.`category`(`category`) VALUES ('computer');
INSERT INTO `db`.`category`(`category`) VALUES ('phone');
INSERT INTO `db`.`category`(`category`) VALUES ('tablet');
INSERT INTO `db`.`category`(`category`) VALUES ('accessory');
INSERT INTO `db`.`category`(`category`) VALUES ('camera');

-- products

INSERT INTO `db`.`product` (`p_id`, `category`, `p_name`, `wholesale_price`, `instore_price`, `manufacturer_id`) VALUES ('p_2', 'phone', 'galaxy s 22', 1000, 1300, 'man_01');
INSERT INTO `db`.`product` (`p_id`, `category`, `p_name`, `wholesale_price`, `instore_price`, `manufacturer_id`) VALUES ('p_3', 'phone', 'galaxy z flip', 1200, 1400, 'man_01');
INSERT INTO `db`.`product` (`p_id`, `category`, `p_name`, `wholesale_price`, `instore_price`, `manufacturer_id`) VALUES ('p_4', 'tablet', 'galaxy tab', 1300, 1450, 'man_01');
INSERT INTO `db`.`product` (`p_id`, `category`, `p_name`, `wholesale_price`, `instore_price`, `manufacturer_id`) VALUES ('p_5', 'computer', 'macbook air', 800, 1000, 'man_02');
INSERT INTO `db`.`product` (`p_id`, `category`, `p_name`, `wholesale_price`, `instore_price`, `manufacturer_id`) VALUES ('p_6', 'computer', 'macbook pro', 1500, 1700, 'man_02');
INSERT INTO `db`.`product` (`p_id`, `category`, `p_name`, `wholesale_price`, `instore_price`, `manufacturer_id`) VALUES ('p_7', 'computer', 'macbook studio', 2500, 2700, 'man_02');
INSERT INTO `db`.`product` (`p_id`, `category`, `p_name`, `wholesale_price`, `instore_price`, `manufacturer_id`) VALUES ('p_8', 'phone', 'Iphone14', 1300, 1400, 'man_02');
INSERT INTO `db`.`product` (`p_id`, `category`, `p_name`, `wholesale_price`, `instore_price`, `manufacturer_id`) VALUES ('p_9', 'tablet', 'Ipad', 1500, 1700, 'man_02');
INSERT INTO `db`.`product` (`p_id`, `category`, `p_name`, `wholesale_price`, `instore_price`, `manufacturer_id`) VALUES ('p_10', 'computer', 'dell book', 1100, 1300, 'man_03');
INSERT INTO `db`.`product` (`p_id`, `category`, `p_name`, `wholesale_price`, `instore_price`, `manufacturer_id`) VALUES ('p_11', 'computer', 'dell book pro', 1600, 1800, 'man_03');
INSERT INTO `db`.`product` (`p_id`, `category`, `p_name`, `wholesale_price`, `instore_price`, `manufacturer_id`) VALUES ('p_12', 'computer', 'Lenovo Carbon', 1700, 1900, 'man_04');
INSERT INTO `db`.`product` (`p_id`, `category`, `p_name`, `wholesale_price`, `instore_price`, `manufacturer_id`) VALUES ('p_13', 'computer', 'Lenovo Think pad', 1400, 2600, 'man_04');
INSERT INTO `db`.`product` (`p_id`, `category`, `p_name`, `wholesale_price`, `instore_price`, `manufacturer_id`) VALUES ('p_14', 'accessory', 'Logitech keyboard', 200, 250, 'man_05');
INSERT INTO `db`.`product` (`p_id`, `category`, `p_name`, `wholesale_price`, `instore_price`, `manufacturer_id`) VALUES ('p_15', 'accessory', 'Logitech keyboard pro', 400, 450, 'man_05');
INSERT INTO `db`.`product` (`p_id`, `category`, `p_name`, `wholesale_price`, `instore_price`, `manufacturer_id`) VALUES ('p_16', 'accessory', 'Logitech mouse', 50, 100, 'man_05');
INSERT INTO `db`.`product` (`p_id`, `category`, `p_name`, `wholesale_price`, `instore_price`, `manufacturer_id`) VALUES ('p_17', 'computer', 'Razer blade 13', 1500, 1700, 'man_06');
INSERT INTO `db`.`product` (`p_id`, `category`, `p_name`, `wholesale_price`, `instore_price`, `manufacturer_id`) VALUES ('p_18', 'computer', 'Razer blade 15', 1700, 1900, 'man_06');
INSERT INTO `db`.`product` (`p_id`, `category`, `p_name`, `wholesale_price`, `instore_price`, `manufacturer_id`) VALUES ('p_19', 'phone', 'google pixel 6', 1200, 1400, 'man_07');
INSERT INTO `db`.`product` (`p_id`, `category`, `p_name`, `wholesale_price`, `instore_price`, `manufacturer_id`) VALUES ('p_20', 'phone', 'google pixel 4a', 700, 900, 'man_07');
INSERT INTO `db`.`product` (`p_id`, `category`, `p_name`, `wholesale_price`, `instore_price`, `manufacturer_id`) VALUES ('p_21', 'phone', 'xperia xi', 1300, 1400, 'man_08');
INSERT INTO `db`.`product` (`p_id`, `category`, `p_name`, `wholesale_price`, `instore_price`, `manufacturer_id`) VALUES ('p_22', 'camera', 'sony xdr cam', 1500, 1700, 'man_08');
INSERT INTO `db`.`product` (`p_id`, `category`, `p_name`, `wholesale_price`, `instore_price`, `manufacturer_id`) VALUES ('p_23', 'camera', 'sony dslr', 2999, 3200, 'man_08');
INSERT INTO `db`.`product` (`p_id`, `category`, `p_name`, `wholesale_price`, `instore_price`, `manufacturer_id`) VALUES ('p_24', 'camera', 'canon pro', 3000, 3300, 'man_09');
INSERT INTO `db`.`product` (`p_id`, `category`, `p_name`, `wholesale_price`, `instore_price`, `manufacturer_id`)
 VALUES ('p_25', 'camera', 'canon beginner', 1200, 1400, 'man_09');

-- store products
-- store s_1 (mostly computers and accessories)

INSERT INTO `db`.`storeINV`(`s_id`,`p_id`,`quantity`,`threshold`) VALUES ('s_1','p_5',5,10);
INSERT INTO `db`.`storeINV`(`s_id`,`p_id`,`quantity`,`threshold`) VALUES ('s_1','p_6',7,10);
INSERT INTO `db`.`storeINV`(`s_id`,`p_id`,`quantity`,`threshold`) VALUES ('s_1','p_7',3,10);
INSERT INTO `db`.`storeINV`(`s_id`,`p_id`,`quantity`,`threshold`) VALUES ('s_1','p_10',1,10);
INSERT INTO `db`.`storeINV`(`s_id`,`p_id`,`quantity`,`threshold`) VALUES ('s_1','p_11',9,10);
INSERT INTO `db`.`storeINV`(`s_id`,`p_id`,`quantity`,`threshold`) VALUES ('s_1','p_12',6,10);
INSERT INTO `db`.`storeINV`(`s_id`,`p_id`,`quantity`,`threshold`) VALUES ('s_1','p_14',2,15);
INSERT INTO `db`.`storeINV`(`s_id`,`p_id`,`quantity`,`threshold`) VALUES ('s_1','p_15',9,15);
INSERT INTO `db`.`storeINV`(`s_id`,`p_id`,`quantity`,`threshold`) VALUES ('s_1','p_16',12,10);
INSERT INTO `db`.`storeINV`(`s_id`,`p_id`,`quantity`,`threshold`) VALUES ('s_1','p_3',2,5);


-- store s_2 (mostly phones and tablets)
INSERT INTO `db`.`storeINV`(`s_id`,`p_id`,`quantity`,`threshold`) VALUES ('s_2','p_2',9,15);
INSERT INTO `db`.`storeINV`(`s_id`,`p_id`,`quantity`,`threshold`) VALUES ('s_2','p_3',2,15);
INSERT INTO `db`.`storeINV`(`s_id`,`p_id`,`quantity`,`threshold`) VALUES ('s_2','p_19',14,15);
INSERT INTO `db`.`storeINV`(`s_id`,`p_id`,`quantity`,`threshold`) VALUES ('s_2','p_20',10,15);
INSERT INTO `db`.`storeINV`(`s_id`,`p_id`,`quantity`,`threshold`) VALUES ('s_2','p_21',3,15);
INSERT INTO `db`.`storeINV`(`s_id`,`p_id`,`quantity`,`threshold`) VALUES ('s_2','p_4',15,20);
INSERT INTO `db`.`storeINV`(`s_id`,`p_id`,`quantity`,`threshold`) VALUES ('s_2','p_9',13,20);
INSERT INTO `db`.`storeINV`(`s_id`,`p_id`,`quantity`,`threshold`) VALUES ('s_2','p_22',2,5);
INSERT INTO `db`.`storeINV`(`s_id`,`p_id`,`quantity`,`threshold`) VALUES ('s_2','p_23',3,5);

-- store s_3 (just cameras)
INSERT INTO `db`.`storeINV`(`s_id`,`p_id`,`quantity`,`threshold`) VALUES ('s_3','p_22',10,20);
INSERT INTO `db`.`storeINV`(`s_id`,`p_id`,`quantity`,`threshold`) VALUES ('s_3','p_23',15,20);
INSERT INTO `db`.`storeINV`(`s_id`,`p_id`,`quantity`,`threshold`) VALUES ('s_3','p_24',17,20);
INSERT INTO `db`.`storeINV`(`s_id`,`p_id`,`quantity`,`threshold`) VALUES ('s_3','p_25',9,20);

-- TODO store admins, maybe through django admin page only.
