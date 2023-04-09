-- /usr/local/mysql/bin/mysql -u root -p

CREATE VIEW Trending_Keywords AS
SELECT C.name, D.year, D.num_publications FROM keyword as C 
JOIN ( SELECT A.keyword_id keyword_id, B.year , COUNT(distinct publication_id) num_publications 
FROM publication_keyword as A JOIN publication as B ON A.publication_id = B.id group by A.keyword_id, B.year) as D 
ON C.id = D.keyword_id;



CREATE INDEX keyword_name_idx ON keyword(name);
