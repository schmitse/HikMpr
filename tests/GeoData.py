from PIL import Image
import piexif

def exif_to_tag(exif_dict, codec='latin-1'):#ISO-8859-1'):
    """ returns the GPS related attributes from EXIF """
    info_dict = {}
    thumbnail = exif_dict.pop('thumbnail')
    info_dict['thumbnail'] = thumbnail.decode(codec)
    for ifd in exif_dict:
        info_dict[ifd] = {}
        for tag in exif_dict[ifd]:
            try:
                element = exif_dict[ifd][tag].decode(codec)
            except AttributeError:
                element = exif_dict[ifd][tag]
            info_dict[ifd][piexif.TAGS[ifd][tag]["name"]] = element
    return info_dict['GPS']


def test(name):
    image = Image.open(name)

    exif_dict = piexif.load(image.info.get('exif'))
    info_dict = exif_to_tag(exif_dict)

    # for key in info_dict:
    #     print(f'{key}: {info_dict[key]}')
    #     print(f'{key}')
    return info_dict


def trafo_tuple(tup):
    assert len(tup)==2, f'Incompatible tuple shape: {tup}'
    return tup[0]/tup[1]


def print_gps(info):

    lat_deg = trafo_tuple(info['GPSLatitude'][0])
    lat_min = trafo_tuple(info['GPSLatitude'][1])
    lat_sec = trafo_tuple(info['GPSLatitude'][2])
    lat_ref = info['GPSLatitudeRef']
    
    lon_deg = trafo_tuple(info['GPSLongitude'][0])
    lon_min = trafo_tuple(info['GPSLongitude'][1])
    lon_sec = trafo_tuple(info['GPSLongitude'][2])
    lon_ref = info['GPSLongitudeRef']
    
    print()
    print(f"Latitude: {lat_deg}* {lat_min}' {lat_sec}'' {lat_ref}")
    print(f'Latitude: {lat_deg + lat_min/60 + lat_sec/3600}')
    print(f"Longitude: {lon_deg}* {lon_min}' {lon_sec}'' {lon_ref}")
    print(f'Longitude: {lon_deg + lon_min/60 + lon_sec/3600}')
    
    return None
        
if __name__=='__main__':
    # image_name1 = 'tests/TestPic2.JPG'
    image_name2 = 'tests/DJI_0015.JPG'

    #info = test(image_name1)
    #print_gps(info)
    info = test(image_name2)
    print_gps(info)
