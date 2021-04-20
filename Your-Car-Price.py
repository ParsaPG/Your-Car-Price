import requests
from sklearn import tree
from bs4 import BeautifulSoup


Brand = input('Chose your brand : ')
MODEL = input('Chose your model : ')
n_y = int(input('When is your production year of your car ? : '))
n_w = int(input('How many kilometers your car worked ? : '))

x = []
y = []

for page in range(1, 7):
    r = requests.get('https://bama.ir/car/%s/%s/all-trims?page=%i' % (Brand, MODEL, page))
    if r.url == 'https://bama.ir/car':
        break
    s = BeautifulSoup(r.text, 'html.parser')
    val = s.find_all('div', attrs={'class':'listdata'})
    for i in val:
        model = i.find('span', attrs={'class':'ad-title-span'}).text.split('،')
        model[0] = model[0].strip()
        model[1] = model[1].strip()
        year = i.find('span', attrs={'class':'price year-label hidden-xs'}).text.strip().split('،')[0]
        year = int(year)
        work = i.find('p', attrs={'class':'price hidden-xs'}).text.strip().split(' ')
        if work[0] == '-':
            continue
        work = work[1]

        if work == 'صفر':
            work = 0
        work2 = ''
        if type(work) != int:
            work = work.split(',')
            for j in work:
                work2+=j
        else:
            work2 = work
        work2 = int(work2)
        price = i.find('p', attrs={'class':'cost'}).text.strip().split(' ')
        if price[0] == "توافقی":
            continue
        price2 = ''
        if type(price[0]) != int:
            price = price[0].split(',')
            for j in price:
                price2+=j
        else:
            price2 = price[0]
        price2 = int(price2)
        x.append((year, work2))
        y.append(price2)
        print("Brand : " , Brand)
        print("Model : " , model[1])
        print("Year : " , year)
        print("Work : " , work2)
        print("Price : " , price2)
        print('-----------------------------------')
clf = tree.DecisionTreeClassifier()
clf = clf.fit(x, y)
in_data = [[n_y, n_w]]
ans = clf.predict(in_data)
print("The price of your car is ", ans[0])
