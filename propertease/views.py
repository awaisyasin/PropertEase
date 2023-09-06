from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import JsonResponse
from accounts.models import CustomUser
from django.contrib.auth.decorators import login_required
from .models import Property, Review, Thread, Comment, PropertyCategory, Message, Follow
from .forms import PropertyForm, ReviewForm, ThreadForm, CommentForm, MessageForm

# Create your views here.

def home_view(request):
    property_type = request.GET.get('property_type')
    price = request.GET.get('price')
    bedrooms = request.GET.get('bedrooms')
    bathrooms = request.GET.get('bathrooms')
    square_footage = request.GET.get('square_footage')

    properties = Property.objects.all()

    if property_type:
        properties = properties.filter(property_type=property_type)
    if price:
        properties = properties.filter(price__lte=price)
    if bedrooms:
        properties = properties.filter(bedrooms=bedrooms)
    if bathrooms:
        properties = properties.filter(bathrooms=bathrooms)
    if square_footage:
        properties = properties.filter(square_footage__gte=square_footage)
    types = PropertyCategory.objects.all()
    return render(request, "propertease/home.html", {"properties": properties, "types": types})


@login_required
def property_form_view(request):
    if request.method == "POST":
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property_instance = form.save(commit=False)
            property_instance.owner = request.user
            property_instance.save()
            return redirect("propertease:home")
    else:
        form = PropertyForm()
    return render(request, "propertease/property-form.html", {"form": form})


def profile_view(request, profile_id):
    profile = CustomUser.objects.get(id=profile_id)
    following = False
    if request.user.is_authenticated:
        if Follow.objects.filter(followee=profile, follower=request.user).exists():
            following = True
    return render(request, "propertease/profile.html", {"profile": profile,"following": following})


def property_detail_view(request, profile_id, property_id):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            property = Property.objects.get(id=property_id)
            review.property = property
            review.save()
            return redirect(request.path + "#comment-box")
    else:
        property = Property.objects.get(id=property_id)
        review_form = ReviewForm()
        reviews = Review.objects.filter(property__id=property_id).order_by("-timestamp")
        return render(request, "propertease/property-detail.html", {"property": property, "review_form": review_form, "reviews": reviews})


def forum_view(request):
    threads = Thread.objects.all().order_by("-created_at")
    return render(request, "propertease/forum.html", {"threads": threads})


@login_required
def thread_form_view(request):
    if request.method == "POST":
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.author = request.user
            thread.save()
            return redirect("propertease:forum")
    form = ThreadForm()
    return render(request, "propertease/thread-form.html", {"form": form})


def thread_detail_view(request, thread_id):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.thread = Thread.objects.get(id=thread_id)
            comment.save()
            return redirect(request.path + "#comment-box")
    thread = Thread.objects.get(id=thread_id)
    comments = Comment.objects.filter(thread=thread_id).order_by("-created_at")
    comment_form = CommentForm()
    return render(request, "propertease/thread-detail.html", {"thread": thread, "comments": comments, "comment_form": comment_form})


def chat_endpoint_view(request, profile_id):
    logged_in_user = request.POST.get('logged_in_user')
    person_to_contact = request.POST.get('person_to_contact')
    response_data = {
        'profile_id': profile_id,
        'logged_in_user': logged_in_user,
        'person_to_contact': person_to_contact,
    }
    return JsonResponse(response_data)


def chat_redirect_view(request, profile_id):
    logged_in_user = request.GET.get('logged_in_user')
    person_to_contact = request.GET.get('person_to_contact')
    if request.method == "POST":
        form = Message(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.user1 = CustomUser.objects.get(username=logged_in_user)
            message.user2 = CustomUser.objects.get(username=person_to_contact)
            message.save()
            return redirect(request.path)
    sender = CustomUser.objects.get(username=logged_in_user)
    receiver = CustomUser.objects.get(username=person_to_contact)
    messages = Message.objects.filter(Q(user1=sender, user2=receiver) | Q(user1=receiver, user2=sender)).order_by("created_at")
    form = MessageForm()
    return render(request, "propertease/chat.html", {"loggedInUser": logged_in_user, "personToContact": person_to_contact, "form": form, "messages": messages})


def save_message_view(request, profile_id, user2_username):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.profile_id = profile_id
            message.user1 = request.user
            try:
                message.user2 = CustomUser.objects.get(username=user2_username)
            except CustomUser.DoesNotExist:
                return JsonResponse({'error': 'User2 does not exist'})
            message.save()
            message_html = f'''
                <div class="message-box">
                    <b>{message.content}</b>
                    <footer>at {message.created_at} by {message.user1}</footer>
                </div>
                <br>
            '''
            return JsonResponse({'message_html': message_html})
        else:
            return JsonResponse({'error': 'Invalid form data'})
    else:
        return JsonResponse({'error': 'Invalid request method'})


@login_required
def follow_user_view(request, follower_id, followee_id):
    try:
        follower = CustomUser.objects.get(id=follower_id)
        followee = CustomUser.objects.get(id=followee_id)
    except CustomUser.DoesNotExist:
        return JsonResponse({'error': 'Invalid user IDs'})
    # Check if the relationship already exists
    if Follow.objects.filter(follower=follower, followee=followee).exists():
        return JsonResponse({'error': 'Already following'})
    # Create a new Follow object
    follow = Follow(follower=follower, followee=followee)
    follow.save()
    return JsonResponse({'success': 'User followed'})