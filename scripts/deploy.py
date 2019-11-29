import csv
from django.utils.text import slugify
from django.utils.text import slugify
from videolog.models import (VideoCategory, VideoKeywords, VideoPeople, VideoEntry)
from django.core.files import File

# Procesa datos de catalogo en variables.
# ...
csvfile=open('catalogo.csv', 'r')
reader = csv.DictReader(csvfile)
video_entries = []
people_tags = []
keywords = []
categories = []


for row in reader:
    # toma las categorias.
    row_cat = row['category'].split('/')
    for cat in row_cat:
        cat = cat.strip()
        if not cat in categories:
            cats_slugs = []
            for c in categories:
                cats_slugs.append(slugify(c))
            if not slugify(cat) in cats_slugs:
                categories.append(cat)
    row_people = row['people'].split(',')
    for people in row_people:
        people = people.strip()
        if not people in people_tags:
            people_slugs = []
            for p in people_tags:
                people_slugs.append(slugify(p))
            if not slugify(people) in people_slugs:
                people_tags.append(people)
    row_kw = row['keywords'].split(',')
    for kw in row_kw:
        kw = kw.strip()
        if not kw in keywords:
            kw_slugs = []
            for k in keywords:
                kw_slugs.append(slugify(k))
            if not slugify(kw) in kw_slugs:
                keywords.append(kw)
    video_entries.append({
            'title' : row['title'],
            'video_code': row['video_code'],
            'category': row_cat,
            'register_date': row['register_date'],
            'people' : row_people,
            'location': row['location'],
            'duration': row['duration'],
            'productor': row['productor'],
            'register_author': row['register_author'],
            'keywords': row_kw,
            'description': row['description'],
            'status': row['status'],
            'desc_date': row['desc_date'],
        })

csvfile.close()

# Insertar categorias.
#...

for cat in categories:
    VideoCategory.objects.create(title=cat, slug=slugify(cat) )

for people in people_tags:
    VideoPeople.objects.create(title=people, slug=slugify(people) )

for kw in keywords:
    VideoKeywords.objects.create(title=kw, slug=slugify(kw) )

# Insertar videos
# ,,

id_cont = 0
for ve in video_entries:
    id_cont += 1
    id_cats = []
    id_kws = []
    id_pops = []
    for cat in ve['category']:
        id_cat = VideoCategory.objects.filter(slug=slugify(cat) )
        if len(id_cat) > 0 :
            id_cats.append(id_cat[0].id)
    print(id_cats)
    for kw in ve['keywords']:
        id_kw = VideoKeywords.objects.filter(slug=slugify(kw) )
        if len(id_kw) > 0 :
            id_kws.append(id_kw[0].id)
        else:
            print("no se encuentró la kw")
    print(id_kws)
    for pp in ve['people']:
        id_pp = VideoPeople.objects.filter(slug=slugify(pp) )
        if len(id_pp) > 0 :
            id_pops.append(id_pp[0].id)
        else:
            print("no se encuentró people")
    print(id_pops)
    # register date format:
    register_date = '-'.join(ve['register_date'].split('-')[::-1])
    if 'preguntar' or 'PREGUNTAR' in register_date:
        register_date = None
    # insertar videos
    VideoEntry.objects.create(
            # data:
            #id=id_cont,
            title=ve['title'],
            video_code = ve['video_code'],
            register_date = register_date,
            location = ve['location'],
            duration = ve['duration'],
            productor = ve['productor'],
            register_author = ve['register_author'],
            description = ve['description'],
            status = ve['status'],
            is_published = True,
            # foreing:
            #category = id_cats,
            #keywords = id_kws,
            #people = id_pops,
        )
    relations = VideoEntry.objects.filter(video_code=ve['video_code'])[0]
    relations.category = id_cats
    relations.keywords = id_kws
    relations.people = id_pops
    relations.save
    print(ve['video_code'])
    try:
        track_chapters = File(
            open('/srv/backup/VTT/'+ve['video_code']+'.vtt','r')
            )
    except:
        print('sin archivo VTT.')
        pass
    else:
        VideoEntry.objects.filter(video_code=ve['video_code'])[0].track_chapters.save(
            ve['video_code']+'.vtt', track_chapters, save=True,
            )
        print('vtt ok!')
    track_chapters.close()
    video_thumb = File(
            open('/srv/backup/thumbs/'+ve['video_code']+'.jpg','rb')
        )
    VideoEntry.objects.filter(video_code=ve['video_code'])[0].video_thumb.save(
            ve['video_code']+'.jpg', video_thumb, save=True,
        )
    print('thumb ok!')
    video_thumb.close()
    video_file = File(
            open('/srv/backup/CD-MDV/'+ve['video_code']+'.mp4','rb')
        )
    VideoEntry.objects.filter(video_code=ve['video_code'])[0].video_file.save(
            ve['video_code']+'.mp4', video_file, save=True,
        )
    print('video ok!')
    video_file.close()


