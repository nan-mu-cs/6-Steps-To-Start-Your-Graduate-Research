import pymongo

client = pymongo.MongoClient('localhost', 27017)

mongodb = client["academicworld"]
publications = mongodb["publications"]
faculty = mongodb["faculty"]


def get_keyword_trend(keyword):
    pipeline = [
        {"$unwind":"$keywords"},
        {"$match": {"keywords.name": keyword}},
        {"$group":{"_id":"$year", "pub_cnt":{"$sum":1}}},
        {"$sort":{"_id": -1}},{"$limit":10}
    ]
    return list(publications.aggregate(pipeline))


def get_top_university_for_keyword(keyword):
    pipeline = [
        {"$unwind":"$keywords"},
        {"$match": {"keywords.name": keyword}},
        {"$group":{"_id": {"name": "$affiliation.name", "photo": "$affiliation.photoUrl"}, "faculty_cnt":{"$sum":1}}},
        {"$sort":{"faculty_cnt": -1}},{"$limit":5}
    ]
    return list(faculty.aggregate(pipeline))