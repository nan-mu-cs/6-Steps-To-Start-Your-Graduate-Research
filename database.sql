-- /usr/local/mysql/bin/mysql -u root -p

CREATE VIEW Trending_Keywords AS
SELECT C.name, D.year, D.num_publications FROM keyword as C 
JOIN ( SELECT A.keyword_id keyword_id, B.year , COUNT(distinct publication_id) num_publications 
FROM publication_keyword as A JOIN publication as B ON A.publication_id = B.id group by A.keyword_id, B.year) as D 
ON C.id = D.keyword_id;



CREATE INDEX keyword_name_idx ON keyword(name);


UPDATE faculty SET  email = '' WHERE email IS NOT NULL AND email NOT LIKE '%@%' AND email != '';
ALTER TABLE faculty
ADD CHECK (email IS NULL OR email = '' OR email LIKE '%@%'  OR email LIKE '%at%');

UPDATE faculty SET phone = '' WHERE phone IS NOT NULL AND phone LIKE '%@%' AND phone != '';
ALTER TABLE faculty
ADD CHECK (phone NOT LIKE '%@%');
