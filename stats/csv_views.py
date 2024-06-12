import csv
from django.http import HttpResponse
from django.db.models import Count
from Roles.models import Role

# def export_dummy_csv(request):
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="dummy.csv"'

#     # Write CSV content
#     writer = csv.writer(response)
#     writer.writerow(['Name', 'Age', 'Country'])
#     writer.writerow(['John', 30, 'USA'])
#     writer.writerow(['Alice', 25, 'Canada'])
#     writer.writerow(['Bob', 35, 'UK'])

#     return response



def export_all_artists_album_favorites(request):
    artist_role = Role.objects.get(pk=2)
    artists = artist_role.user.all()
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="artists_album_favorites.csv"'

    genders = set()
    artist_likes = {}  
    for artist in artists:
        albums = artist.album_set.all()
        artist_likes[artist] = sum(album.favourite_by.count() for album in albums)  # Calculate total likes for each artist
        for album in albums:
            favourites_by_gender = album.favourite_by.values('user__gender').annotate(count=Count('user__gender')).order_by('user__gender')
            genders.update(favourite['user__gender'] for favourite in favourites_by_gender)

    # Sort artists based on likes in descending order
    sorted_artists = sorted(artist_likes.items(), key=lambda x: x[1], reverse=True)

    csv_header = ['Artist ID', 'Artist Email', 'Album ID', 'Album Title', 'Total Favourite Count', 'Popular']
    for gender in genders:
        csv_header.append(f'{gender.capitalize()} Favourite Count')

    writer = csv.writer(response)
    writer.writerow(csv_header)

    rank = 1
    for artist, _ in sorted_artists:
        for album in artist.album_set.all():
            gender_counts = {gender: 0 for gender in genders}
            total_favourite_count = album.favourite_by.count()
            favourites_by_gender = album.favourite_by.values('user__gender').annotate(count=Count('user__gender')).order_by('user__gender')
            for favourite in favourites_by_gender:
                gender_counts[favourite['user__gender']] = favourite['count']
            csv_row = [
                artist.id,
                artist.email,
                album.id,
                album.title,
                total_favourite_count,
                rank  
            ]
            for gender in genders:
                csv_row.append(gender_counts[gender])

            writer.writerow(csv_row)

        rank += 1  
    return response
