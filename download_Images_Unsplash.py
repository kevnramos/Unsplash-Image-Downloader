import requests

path = 'Paste/your/path/here/'

unsplash_Access_Key = 'PasteYourUnsplashAPIKeyHere'


keyword = input('Enter search term: ')
numPics = int(input('Enter number of pictures you want downloaded: '))
LorP = input('Do you want (l)andscape, (p)ortrait, or (a)ny orientation pictures? ("l" or "p" or "a")?: ').lower()


def isLandscape(imgData):
    if imgData['width']>imgData['height']:
        return True
    return False

def isPortrait(imgData):
    if imgData['width']<imgData['height']:
        return True
    return False


def apiData(pgNumber):
    baseUrl = 'https://api.unsplash.com/search/photos?query='
    endingUrl = f'&page={pgNumber}&per_page=30&client_id={unsplash_Access_Key}'

    totalUrl = baseUrl+keyword+endingUrl

    r = requests.get(totalUrl, stream = True)
    data = r.json()

    return data


def dowloadImages(LorP):
    count = 0
    for pages in range(0,100):  #range is 100 incase there arent enough images in a given page to meet requirements of desired number of pictures
        
        if count == numPics: #if desired number of pictures are downloaded, break loop
            break
        
        data = apiData(pages+1)
        
        for i in range(0,30):
            if count == numPics:   #if desired number of pictures are downloaded, breaks loop
                break

            imgUrl = data['results'][i]

            try:   
                if LorP == 'l':
                    if not isLandscape(imgUrl):
                        i+=1
                        imgUrl = data['results'][i]
                        continue
                if LorP == 'p':
                    if not isPortrait(imgUrl):
                        i+=1
                        imgUrl = data['results'][i]
                        continue                    
            
                imgUrl = data['results'][i]['links']['download']
                k = requests.get(imgUrl)

                imgName = data['results'][i]['description']
                if imgName !=None and len(imgName)>67:       #if original image name is too long we use alternate description
                    imgName = data['results'][i]['alt_description']
                if imgName == None:                         #if original image name has no name we use alternate description
                    imgName = data['results'][i]['alt_description']
                if imgName == None:                        #if image alternate description is none, we use part of the url to name the picture
                    imgName = imgUrl.split('=')[-1]

                imgLocation = path + imgName + '.jpg'    #use this to write the image name into our folder as a .jpg file
                

                with open(imgLocation,'wb') as f:
                    f.write(k.content)
                print(f"Downloaded {imgName}.jpg")

                count+=1

            except:           #used exception here incase list index was out of range on this page. Breaks loop and continues search on following page
                break

    print(f'\nDownloads complete!\n{count} images downloaded')


dowloadImages(LorP)
