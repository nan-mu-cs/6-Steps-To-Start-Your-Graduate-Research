# 6 Steps To Start Your Graduate Research

## Purpose

## Demo

## Installation
We only used given dataset for MySQL, MongoDB and Neo4j database.

Install python dependencies:
```
pip install -r requirements.txt
```

Mysql credential is stored in mysql_credential.py file which we on purposely not upload to github. To connect your local mysql instance, create a mysql_credential.py, with the following content:
```
MYSQL_CREDENTIAL = {
    "user": "root",
    "password": "password"
}
```
Replace the user and password with your MySQL instance's credentials.

## Usage

To start the app, run the following command:
```
python app.py
```

## Design

## Implementation

## Database Techniques

We used materialized view, indexing and constraint 3 database techniques in this project. The SQL statement used to adopt the techniques are stored in `database.sql`

#### Materialized View
We use Materialized View to get (keyword, number of citations, year) so we could get trending keywords over the years fast.
We use the following SQL statement to create Materialized View:
```
CREATE VIEW Trending_Keywords AS
SELECT C.name, D.year, D.num_publications FROM keyword as C 
JOIN ( SELECT A.keyword_id keyword_id, B.year , COUNT(distinct publication_id) num_publications 
FROM publication_keyword as A JOIN publication as B ON A.publication_id = B.id group by A.keyword_id, B.year) as D 
ON C.id = D.keyword_id;
```

#### Index
We created index for name column in keyword table, so we can search by keyword name fast. Here is the SQL statement:
```
CREATE INDEX keyword_name_idx ON keyword(name);
```

#### Constraints
We create 2 check constraints:
* To check we put correct email format for faculty email when we update/insert faculty records. We also sanitize existing faculty email: 
    ```
    UPDATE faculty SET  email = '' WHERE email IS NOT NULL AND email NOT LIKE '%@%' AND email != '';
    ALTER TABLE faculty
    ADD CHECK (email IS NULL OR email = '' OR email LIKE '%@%'  OR email LIKE '%at%');
    ```
* Check to prevent user accidentally put email address in phone column. As we go over the table, we cound many records have used email as phone number. We also sanitize existing faculty phone:
    ```
    UPDATE faculty SET phone = '' WHERE phone IS NOT NULL AND phone LIKE '%@%' AND phone != '';
    ALTER TABLE faculty
    ADD CHECK (phone NOT LIKE '%@%');
    ```


## Extra-Credit Capabilities

## Contributions
This project is done by Nan Mu (nanmu2@) myself. I spent ~40 hours for it.