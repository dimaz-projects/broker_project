from django.shortcuts import render
from django.shortcuts import redirect
from django.core.mail import EmailMessage
from django.core.mail.backends.smtp import EmailBackend
import datetime
import requests
from bs4 import BeautifulSoup
import feedparser
from .models import clients,useful_sites, notes, companies_sites


def main(request):
    #backend = EmailBackend(host='smtp.mail.ru', port=587, username='fabiocoentao', 
    #                   password='pass1234', use_tls=True)
    #email = EmailMessage(subject='Тест сообщения', body='Текст сообщения', from_email='fabiocoentao@mail.ru', to=['actowaratas@mail.ru'], 
    #         connection=backend)
    #email.send()
    
    return render(request, 'main.html')

def analyse(request):
    return render(request, 'analyse.html')

def secur_ch(request):
    return render(request, 'secur_ch.html')


def news(request):
    choice = request.POST.get('secur_name')
    if choice=='Сбербанк':
        tmp='https://www.finam.ru/profile/moex-akcii/sberbank/news/'
    elif choice=='Роснефть':
        tmp='https://www.finam.ru/profile/moex-akcii/rosneft/news/'
    elif choice=='Газпром':
        tmp='https://www.finam.ru/profile/moex-akcii/gazprom/news/'
    elif choice=='Лукойл':
        tmp='https://www.finam.ru/profile/moex-akcii/lukoil/news/'
    elif choice=='Аэрофлот':
        tmp='https://www.finam.ru/profile/moex-akcii/aeroflot/news/'
    
    r = requests.get(tmp).text
    soup = BeautifulSoup(r, 'html.parser')
    news_list = soup.find('table', class_='news-list')
  #  news_list_items=news_list.find_all('div', class_='subject')
    news_list_items=news_list.find_all('tr', class_='news')
    all_news=[]
    for i in news_list_items:
        str_news=str(i.prettify())
        str_news=str_news.replace('href="/', 'href="https://www.finam.ru/')
        
        all_news.append(str_news)

    return render(request, 'secur_choice.html', {'all_news':all_news})


def tech_analyse(request):
    choice = request.POST.get('secur_name')
    tmp=''
    if choice=='Сбербанк':
        tmp='https://www.finam.ru/profile/moex-akcii/sberbank/tehanalys-live/'
    elif choice=='Роснефть':
        tmp='https://www.finam.ru/profile/moex-akcii/rosneft/tehanalys-live/'
    elif choice=='Газпром':
        tmp='https://www.finam.ru/profile/moex-akcii/gazprom/tehanalys-live/'
    elif choice=='Лукойл':
        tmp='https://www.finam.ru/profile/moex-akcii/lukoil/tehanalys-live/'
    elif choice=='Аэрофлот':
        tmp='https://www.finam.ru/profile/moex-akcii/aeroflot/tehanalys-live/'
    return render(request, 'tech_analyse.html', {'site_link':tmp})


def comp_news(request):
    d=feedparser.parse('https://www.finam.ru/analysis/conews/rsspoint')
    d=d.entries

    incr=0
    for post in d:
        date = "%02d.%02d.%d %02d:%02d" % (post.published_parsed.tm_mday,\
                                    post.published_parsed.tm_mon, \
                                    post.published_parsed.tm_year, \
                                    post.published_parsed.tm_hour, \
                                    post.published_parsed.tm_min  )
        d[incr].update({'published': date})
        incr=incr+1
    
    return render(request, 'companies_news.html', {'news_set':d})

def exp_comments(request):
    d=feedparser.parse('https://www.finam.ru/analysis/nslent/rsspoint')
    d=d.entries

    incr=0
    for post in d:
        date = "%02d.%02d.%d %02d:%02d" % (post.published_parsed.tm_mday,\
                                    post.published_parsed.tm_mon, \
                                    post.published_parsed.tm_year, \
                                    post.published_parsed.tm_hour, \
                                    post.published_parsed.tm_min  )
        d[incr].update({'published': date})
        incr=incr+1
    
    return render(request, 'experts_comments.html', {'comments_set':d})


def secur_price(request):

    r = requests.get('https://www.finam.ru/quotes/stocks/russia/').text
    soup = BeautifulSoup(r, 'html.parser')

    prices_list = soup.find('table',class_='pages2-QuoteOnline-components-QuoteTable-___QuoteTable__table___RPe2c')
    prices_list_items=prices_list.find_all('tr')

    all_prices=[]
    for i in prices_list_items:
        body=''
        k=0
        items_td=i.find_all('td')
        for j in items_td:
            if k >1:
                body=body+str(j)
            elif k==1:
                items_td_a=j.find_all('a')
                body=body+'<td nowrap>'+str(items_td_a[0])+'</td>'
            k=k+1
        body=body.replace('href="/', 'href="https://finam.ru/')
        itog='<tr>'+body+'</tr>'
        all_prices.append(itog)

    return render(request, 'secur_price.html', {'prices_set':all_prices})



def clients_window(request):
    return render(request, 'clients_window.html')

def clients_add(request):
    name_cl=request.POST.get('client_name')
    birthday_cl=request.POST.get('client_birthday')
    print(" BIRTHDAY:   ", birthday_cl)
    number=request.POST.get('client_number')
    email_cl=request.POST.get('client_email')
    contract=request.POST.get('client_contract')
    success=''
    
    if name_cl != None:
        new_client=clients(name=name_cl, birthday=birthday_cl,
                           phone_number=number,email=email_cl,contract_date=contract)
        new_client.save()
        success='Клиент успешно добавлен'
    return render(request, 'clients_add.html', {'success':success})

def clients_view(request):
    clients_list=clients.objects.all()
    clients_list=clients_list.order_by("id")
    success=''
    if request.method == 'POST':
        receiv_id=request.POST.get('choice_client_message')
        receiv = clients.objects.get(id=receiv_id)
        subj=request.POST.get('message_subj')
        message_text=request.POST.get('message')

        try:
            email = EmailMessage(subject=subj, body=message_text,from_email=from_broker_mail,
                                 to=[receiv.email],connection=backend)
            email.send()
            success='Сообщение успешно отправлено'
        except:
            success='Возникла проблема при отправке сообщения. Проверьте данные для авторизации.'

    
    return render(request, 'clients_view.html', {'clients_list': clients_list, 'success':success})

def clients_delete(request):
    clients_list=clients.objects.all()
    client_id=request.POST.get('choice_client')
    choice_action=request.POST.get('choice_action')
    success=''
    
    print(request.POST)
    if client_id !=None and choice_action=='delete':
        client = clients.objects.get(id=client_id)
        client.delete()
        success='Клиент успешно удален'
    elif client_id !=None and choice_action=='modify':
        global global_id
        #client = clients.objects.get(id=client_id)
        global_id=client_id
        return redirect('cl_modify' )
        
    
    return render(request, 'clients_delete.html', {'clients_list': clients_list,'success':success})



def clients_modify(request):
    client=clients.objects.get(id=global_id)
    success=''
    
    if request.method == 'POST':
        client.name=request.POST.get('client_name')
        client.birthday=request.POST.get('client_birthday')
        client.phone_number=request.POST.get('client_number')
        client.email=request.POST.get('client_email')
        client.contract_date=request.POST.get('client_contract')
        client.save()
        success='Клиент успешно изменен'
    return render(request, 'clients_modify.html', {'client': client, 'success':success})


def useful_site(request):
    useful_list=useful_sites.objects.all()
    if len(useful_list)==0:
        return redirect('usef_add' )
    success=''
    if request.method == 'POST':
        site_id=request.POST.get('choice_site')
        choice_action=request.POST.get('choice_action')
    
        print(request.POST)
        if site_id !=None and choice_action=='delete':
            site = useful_sites.objects.get(id=site_id)
            site.delete()
            success='Сайт успешно удален'
        elif site_id !=None and choice_action=='modify':
            global global_id
            #client = clients.objects.get(id=client_id)
            global_id=site_id
            return redirect('usef_modify' )
    return render(request, 'useful_data.html', {'useful_list': useful_list,'success':success})

def useful_add(request):
    site_name=request.POST.get('site_name')
    description=request.POST.get('description')
    link=request.POST.get('link')
    success=''
    
    if link != None:
        new_site=useful_sites(site_name=site_name,description=description,link=link)
        new_site.save()
        success='Сайт успешно добавлен'
    return render(request, 'useful_add.html', {'success':success})

def useful_modify(request):
    site=useful_sites.objects.get(id=global_id)
    success=''
    
    if request.method == 'POST':
        site.site_name=request.POST.get('site_name')
        site.description=request.POST.get('description')
        site.link=request.POST.get('link')
        site.save()
        success='Сайт успешно изменен'
    return render(request, 'useful_modify.html', {'site': site,'success':success})
   
def my_notes(request):
    my_notes_list=notes.objects.all()
    clients_list=clients.objects.all()
    clients_list=clients_list.order_by("id")
    if len(my_notes_list)==0:
        return redirect('notes_add')
    success=''
    if request.method == 'POST':
        note_id=request.POST.get('note_id')
        choice_action=request.POST.get('choice_action')
        receiv_id=request.POST.get('choice_client_message')
        print(request.POST)
        if note_id !=None and choice_action=='delete':
            note = notes.objects.get(id=note_id)
            note.delete()
            success='Заметка успешно удалена'
        elif note_id !=None and choice_action=='modify':
            global global_id
            #client = clients.objects.get(id=client_id)
            global_id=note_id
            return redirect('notes_modify' )
        elif note_id !=None and receiv_id !=None and choice_action=='send':
            receiv = clients.objects.get(id=receiv_id)
            mes=notes.objects.get(id=note_id)
            try:
                email = EmailMessage(subject=mes.topic, body=mes.description,from_email=from_broker_mail,
                                 to=[receiv.email],connection=backend)
                email.send()
                success='Сообщение успешно отправлено'
            except:
                success='Возникла проблема при отправке сообщения. Проверьте данные для авторизации.'

    return render(request, 'my_notes.html', {'clients_list': clients_list,'notes_list': my_notes_list,'success':success})


def notes_add(request):
    note_topic=request.POST.get('note_topic')
    description=request.POST.get('description')
    success=''
    
    if description != None:
        now = datetime.datetime.now()
        now=now.strftime("%Y-%m-%d %H:%M")
        new_note=notes(topic=note_topic,description=description,date=now)
        new_note.save()
        success='Заметка успешно добавлена'
    return render(request, 'my_notes_add.html', {'success':success})


def autoriz(request):
    success=''
    if 'auth' in globals():
        if auth==True:
            success='Ваши данные записаны в систему. Не забудьте стереть их.'
    if request.method == 'POST':
        global backend
        global auth
        if request.POST.get('choice') == 'Сохранить':
            mail=request.POST.get('choice_mail')
            login=request.POST.get('login')
            passwrd=request.POST.get('password')
            global from_broker_mail
            from_broker_mail=login+'@'+mail[5:]
            backend = EmailBackend(host=mail, port=587, username=login,
                                   password=passwrd, use_tls=True)
            success='Данные сохранены'
            auth=True
        else:
            backend=''
            success="Данные стерты"
            auth=False
    return render(request, 'autoriz.html', {'success':success})


def comp_sites_list(request):
    sites_list=companies_sites.objects.all()
    if len(sites_list)==0:
        return redirect('site_add' )
    success=''
    if request.method == 'POST':
        site_id=request.POST.get('choice_site')
        choice_action=request.POST.get('choice_action')
    
        print(request.POST)
        if site_id !=None and choice_action=='delete':
            site = companies_sites.objects.get(id=site_id)
            site.delete()
            success='Сайт успешно удален'
        elif site_id !=None and choice_action=='modify':
            global global_id
            #client = clients.objects.get(id=client_id)
            global_id=site_id
            return redirect('site_modify' )
    return render(request, 'sites_list.html', {'sites_list': sites_list,'success':success})


def sites_add(request):
    site_name=request.POST.get('company_name')
    link=request.POST.get('link')
    report_link=request.POST.get('report_link')
    success=''
    if link != None:
        new_site=companies_sites(company_name=site_name,link=link,report_link=report_link)
        new_site.save()
        success='Сайт успешно добавлен'
    return render(request, 'sites_add.html', {'success':success})
