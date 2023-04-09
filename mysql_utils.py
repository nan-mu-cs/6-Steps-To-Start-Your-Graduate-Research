import pymysql
from mysql_credential import MYSQL_CREDENTIAL
from threading import Lock

mutex = Lock()

mysql_db = pymysql.connect(host='localhost',
                user=MYSQL_CREDENTIAL['user'],
                password=MYSQL_CREDENTIAL['password'],
                database='academicworld',
                charset='utf8mb4',
                port=3306)

def get_popular_keywords(year, number):
    with mysql_db.cursor() as cursor, mutex:
        sql = """
            SELECT name, sum(num_publications) total 
            FROM trending_keywords 
            WHERE year > {year} 
            GROUP BY name 
            ORDER BY total DESC 
            LIMIT {number};
        """.format(year=year, number=number)
        cursor.execute(sql)
        return cursor.fetchall()
    

def get_top_professors_for_keyword(keyword):
    with mysql_db.cursor() as cursor, mutex:
        sql = '''
        SELECT F.name, F.phone, F.email, F.photo_url 
        FROM (
            SELECT A.name,A.id,SUM(score * num_citations)KRC, A.email, A.phone, A.photo_url
            FROM faculty AS A JOIN (
                SELECT B.faculty_id,C.score,D.num_citations 
                FROM faculty_publication AS B JOIN publication_keyword AS C ON B.publication_id = C.publication_id 
                    JOIN publication AS D ON C.publication_id = D.id JOIN keyword AS E on C.keyword_id = E.id
                WHERE E.name = '{keyword}') AS F ON A.id = F.faculty_id 
                GROUP BY A.id ORDER BY KRC desc limit 10) AS F'''.format(keyword=keyword)
        cursor.execute(sql)
        return cursor.fetchall()

def get_top_s_for_keyword(keyword):
    with mysql_db.cursor() as cursor, mutex:
        sql = '''SELECT A.title, A.venue,A.year, A.num_citations
                FROM publication AS A JOIN publication_keyword AS B ON A.id = B.publication_id 
                    JOIN keyword as C ON B.keyword_id = C.id 
                WHERE C.name = '{keyword}' 
                ORDER BY score * num_citations desc 
                limit 10'''.format(keyword=keyword)
        cursor.execute(sql)
        return cursor.fetchall()
