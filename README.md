# Electronic Vendor Database Application

Below is the Electronic Vendor Database application our team worked on. This application is built using Python and Django and it serves to manage an online electronic vendor's operations ranging from inventory management, online and in-store sales, warehouse and store restocking, to member management and more.

## Designing the Database

The design of this database started with an extensive review of articles and literature in my class book related to efficient database design. I spent a considerable amount of time understanding the business requirements of an online electronic vendor, breaking down these requirements into manageable entities, and working on how these entities would interact with each other.

After this initial research, I decided to adopt a relational database design, considering its advantages like data integrity, data consistency, and flexibility in querying data. I carefully designed the entities (tables) in a way that ensures normalization to reduce data redundancy and improve data integrity. 

## Database Schema

The database consists of multiple tables including `member`, `memberAddress`, `memberCardInfo`, `manufacturer`, `category`, `product`, `warehouse`, `store`, and many more, each designed to store specific types of data. Relations are well-defined among these tables, with foreign keys ensuring referential integrity.

I also implemented constraints like `UNIQUE`, `CHECK` and `DEFAULT` to ensure the data is valid and consistent. For instance, the `member` table has a `type` column that checks if the value is either 1 or 2, representing normal and contract members respectively. Triggers are also defined to auto manage inventory in the warehouse when a new product is added.

You'll find comprehensive SQL scripts in the project repository, providing detailed insights into the database schema, relationships, constraints, and triggers. Here's an example of the `member` table creation:

```sql
create table member(
    m_id varchar(50) primary key,
    name varchar(20) not null,
    phone varchar(20) not null, 
    email varchar(50) UNIQUE,
    type int check(type in (1,2)), 
    user_status int default 1, 
    reg_date DATE NOT NULL, 
    billing_date DATE 
);
```

## Implementation

Most of my efforts have been channeled towards backend development, ensuring the efficiency, security, and scalability of the application. However, I also worked on frontend development.

## Testing and Usage

The project repository contains data scripts for the initial loading of the database tables, such as:

```sql
INSERT INTO `db`.`store`(`s_id`,`address`,`state`,`zipcode`) VALUES ('s_1','Jupiter OA', 'R2','229');
```

In order to test the functionality of this application, you may need to execute these scripts first. Following that, you may interact with the application either by using the Django interface, or by interacting with the REST API that has been designed for this purpose.

## Feedback

While I've tested this application rigorously, I encourage you to provide any feedback you might have. I'm always open to improvement and would love to hear your suggestions on how this application could be made better. Thank you for taking the time to review my project!
