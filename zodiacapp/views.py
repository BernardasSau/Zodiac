from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from .models import UserProfile, RelationshipStatus, Comment
from django.contrib.auth.forms import UserCreationForm
import requests
from bs4 import BeautifulSoup
from .forms import CommentForm, UserProfileForm, NatalChartForm
from django.core.mail import send_mail
from .forms import ContactForm
from django.conf import settings
from django.contrib import messages
import logging
from .forms import RelationshipStatusForm


@login_required
def compatible_users(request):
    """
    Atvaizduoti suderinamus vartotojus pagal prisijungusio ženklą.
    Pasinaudodamas pateiktu žodynu vartotojui parenkami nariai, kurių ženklai yra suderinami su juo,
    išskyrus jį patį.
    request: užklausos objektas.
    returns: suderinamų vartotojų sąrašą.
    """
    user_profile = get_object_or_404(UserProfile, user=request.user)
    compatible_signs = {
        'Avinas': ['Liūtas', 'Skorpionas', 'Šaulys'],
        'Jautis': ['Mergelė', 'Ožiaragis', 'Žuvys'],
        'Dvyniai': ['Svarstyklės', 'Vandenis', 'Šaulys'],
        'Vėžys': ['Jautis', 'Žuvys', 'Mergelė'],
        'Liūtas': ['Dvyniai', 'Šaulys', 'Avinas'],
        'Mergelė': ['Skorpionas', 'Ožiaragis', 'Jautis'],
        'Svarstyklės': ['Vandenis', 'Dvyniai', 'Liūtas'],
        'Skorpionas': ['Žuvys', 'Ožiaragis', 'Vėžys'],
        'Šaulys': ['Liūtas', 'Avinas', 'Vandenis'],
        'Ožiaragis': ['Jautis', 'Mergelė', 'Skorpionas'],
        'Vandenis': ['Svarstyklės', 'Dvyniai', 'Šaulys'],
        'Žuvys': ['Vėžys', 'Jautis', 'Skorpionas'],
    }
    user_sign = user_profile.zodiac
    compatible_signs_for_user = compatible_signs.get(user_sign, [])

    compatible_user_profiles = UserProfile.objects.filter(zodiac__in=compatible_signs_for_user).exclude(
        user=request.user)
    paginator = Paginator(compatible_user_profiles, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'compatible_users.html', {'page_obj': page_obj})


def index(request):
    """
    Rodomas pagrindinis puslapis su vartotojų ir vienišų vartotojų statistika.
    request: užklausos objektas.
    Returns: Sugeneruotas index.html šablonas su konteksto duomenimis.
    """
    num_users = User.objects.count()
    num_single_users = RelationshipStatus.objects.filter(status='Vienišas').count()

    context = {
        'num_users': num_users,
        'num_single_users': num_single_users,
    }

    return render(request, 'index.html', context)


def user_list(request):
    """
    Rodomas visų vartotojų sąrašas ir užtikrinama, kad vartotojas turėtų profilį.
    request: užklausos objektas.
    return: Sugeneruotas user.html šablonas su narių atvaizdavimu.
    """
    user_list1 = User.objects.all()
    paginator = Paginator(user_list1, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'user.html', {'page_obj': page_obj})


def matchmaking(request):
    """Funkcija ateičiai"""
    return render(request, 'matchmaking.html')


@login_required
def profile(request):
    """
    Rodomas vartotojo profilis ir leidžiama atnaujinti profilį.
    request: užklausos objektas.
    return: Sugeneruotas profile.html šablonas su kontekstu.
    """
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)

    context = {
        'form': form,
    }

    return render(request, 'profile.html', context)


@login_required
def profile_view(request):
    """
    Rodomas vartotojo profilio puslapis ir horoskopas pagal pasirinktą zodiako ženklą.
    request: užklausos objektas.
    returns: Sugeneruotas profile.html šablonas su horoskopu ar klaidos pranešimu.
    """
    if request.method == 'POST':
        desired_sign = request.POST.get('zodiac_sign', '').upper()
        if desired_sign:
            response = requests.get("https://ve.lt/horoskopai/dienos-horoskopai-12-zodiako-zenklu")
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            h3_tag = soup.find('h3', string=desired_sign + ".")

            if h3_tag:
                horoscope_text = h3_tag.text.strip() + ":\n"
                next_tag = h3_tag.find_next_sibling()
                while next_tag and next_tag.name != 'h3':
                    p_text = next_tag.text.strip()
                    p_text_with_newlines = p_text.replace('. ', '.\n')
                    horoscope_text += "- " + p_text_with_newlines + "\n"
                    next_tag = next_tag.find_next_sibling()

                return render(request, 'profile.html', {'horoscope_text': horoscope_text})
            else:
                error_message = f"Horoskopas {desired_sign} ženklui nerastas."
                return render(request, 'profile.html', {'error_message': error_message})
        else:
            error_message = "Prašome pasirinkti žodiako ženklą."
            return render(request, 'profile.html', {'error_message': error_message})
    else:
        return render(request, 'profile.html')


@login_required
def profile_detail(request, user_id):
    """
    Rodomas pasirinkto vartotojo profilis ir leidžiama profilyje palikti komentarą.
    request: užklausos objektas.
    user_id: Vartotojo ID, kurio profilis peržiūrimas.
    return: Sugeneruotas profile_detail.html šablonas su vartotojo profilio, komentarų ir formos atvaizdavimu.
    """
    user_profile = get_object_or_404(UserProfile, user_id=user_id)
    comments = Comment.objects.filter(user_id=user_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
            return redirect('profile-detail', user_id=user_id)
    else:
        form = CommentForm()

    return render(request, 'profile_detail.html',
                  {'user_profile': user_profile, 'comments': comments, 'form': form})


def signup(request):
    """
    Registracijos funkcija, sukuria naują vartotoją ir vartotojo profilį.
    request: užklausos objektas.
    return: Sugeneruotas signup.html šablonas su formos kontekstu ir nukreipimas į
    pagrindinį puslapį po sėkmingos registracijos.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            return redirect('/main/')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


@login_required
def edit_profile_view(request):
    """
    Leidžia vartotojui redaguoti savo profilį ir santykių statusą.
    request: užklausos objektas.
    returns: Sugeneruotas edit_profile.html šablonas su profilio ir statuso formos kontekstu.
    """
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    relationship_status, created = RelationshipStatus.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        status_form = RelationshipStatusForm(request.POST, instance=relationship_status)

        if profile_form.is_valid() and status_form.is_valid():
            profile_form.save()
            status_form.save()
            return redirect('profile')
    else:
        profile_form = UserProfileForm(instance=user_profile)
        status_form = RelationshipStatusForm(instance=relationship_status)

    return render(request, 'edit_profile.html', {
        'profile_form': profile_form,
        'status_form': status_form
    })


@login_required
def comments_view(request):
    """
    Rodomas komentarų puslapis ir leidžiama skelbti naujus komentarus.
    request: HTTP užklausos objektas.
    returns: Sugeneruotas comments.html šablonas su komentarų atvaizdavimu.
    """
    comments = Comment.objects.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.save()
            return redirect('comments')
    else:
        form = CommentForm()

    return render(request, 'comments.html', {'comments': comments, 'form': form})


logger = logging.getLogger(__name__)


def contact(request):
    """
    Apdoroja kontaktinę informaciją ir siunčia el. laišką.
    request:užklausos objektas.
    Return: Sugeneruotas contact.html šablonas su formos kontekstu arba nukreipimas į thank_you
    puslapį po sėkmingo el. laiško išsiuntimo.
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            try:

                send_mail(
                    subject,
                    f'From: {name} <{email}>\n\n{message}',
                    settings.DEFAULT_FROM_EMAIL,
                    ['b.saulius@hotmail.com'],
                    fail_silently=False
                )
                messages.success(request, 'Your email has been sent successfully!')
                return redirect('thank_you')
            except Exception as e:
                logger.error(f'Failed to send email: {e}')
                messages.error(request, 'Failed to send email. Please try again later.')
                return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})


def thank_you_view(request):
    """
    Rodomas ačiū puslapis po sėkmingo formos pateikimo.
    request: užklausos objektas.
    returns: Rodomas thank_you.html šablonas.
    """
    return render(request, 'thank_you.html')


def generate_natal_chart(request):
    """
    Generuoja gimimo diagramą pagal vartotojo pateiktą informaciją ir rodo rezultatą.
    Jei pateikta forma tinkama, tada siunčiama užklausą į API.
    Returns: Sugeneruota gimimo diagrama arba klaidos pranešimas.
    """
    if request.method == 'POST':
        form = NatalChartForm(request.POST)
        if form.is_valid():
            url = "https://astroapi-4.divineapi.com/western-api/v1/natal-wheel-chart"

            api_key = '29530de21430b7540ec3f65135f7323c'
            auth_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL2FzdHJvYXBpLTEuZGl2aW5lYXBpLmNvbS9hcGkvYXV0aC1hcGktdXNlciIsImlhdCI6MTcxNzQwODkzMCwibmJmIjoxNzE3NDA4OTMwLCJqdGkiOiJKUUtBSFhaTkJhT1V3aDJGIiwic3ViIjoiMTkzMCIsInBydiI6ImU2ZTY0YmIwYjYxMjZkNzNjNmI5N2FmYzNiNDY0ZDk4NWY0NmM5ZDcifQ.buBlE_6JMyn7GEnOf__3y6tqlYkypCf_urLwBZ0UELI'

            payload = {
                'api_key': api_key,
                'full_name': form.cleaned_data['full_name'],
                'day': form.cleaned_data['day'],
                'month': form.cleaned_data['month'],
                'year': form.cleaned_data['year'],
                'hour': form.cleaned_data['hour'],
                'min': form.cleaned_data['min'],
                'sec': form.cleaned_data['sec'],
                'gender': form.cleaned_data['gender'],
                'place': form.cleaned_data['place'],
                'lat': form.cleaned_data['lat'],
                'lon': form.cleaned_data['lon'],
                'tzone': form.cleaned_data['tzone']
            }

            headers = {
                'Authorization': f'Bearer {auth_token}'
            }

            response = requests.post(url, headers=headers, data=payload)

            if response.status_code == 200:
                svg_data = response.json().get('data', {}).get('svg', '')
                return render(request, 'natal_chart.html', {'svg_data': svg_data})
            else:
                error_message = response.json().get('error', 'Failed to generate natal chart')
                return render(request, 'error.html', {'error_message': error_message})
    else:
        form = NatalChartForm()
    return render(request, 'generate_natal_chart.html', {'form': form})
